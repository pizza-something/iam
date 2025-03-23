from dataclasses import dataclass
from typing import Any

from effect import just

from iam.application.ports.accounts import Accounts
from iam.application.ports.clock import Clock
from iam.application.ports.event_queue import (
    AccountCreatedEvent,
    EventQueue,
)
from iam.application.ports.expiring_token_encoding import (
    ExpiringTokenEncoding,
)
from iam.application.ports.map import MapTo
from iam.application.ports.transaction import TransactionOf
from iam.entities.access.account import AccountName
from iam.entities.access.password import Password, PasswordHashing
from iam.entities.access.token import AccessToken, RefreshToken
from iam.entities.access.user import signed_up_user_when


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
    encoded_access_token: EncodedAccessTokenT
    encoded_refresh_token: EncodedRefreshTokenT


@dataclass(kw_only=True, frozen=True, slots=True)
class SignUp[
    EncodedAccessTokenT = Any,
    EncodedRefreshTokenT = Any,
    AccountsT: Accounts = Accounts,
]:
    clock: Clock
    access_token_encoding: ExpiringTokenEncoding[
        AccessToken, EncodedAccessTokenT
    ]
    refresh_token_encoding: ExpiringTokenEncoding[
        RefreshToken, EncodedRefreshTokenT
    ]
    accounts: AccountsT
    event_queue: EventQueue
    map_to: MapTo[tuple[AccountsT]]
    transaction_of: TransactionOf[tuple[AccountsT]]
    password_hashing: PasswordHashing

    async def __call__(
        self,
        account_name_text: str,
        password_text: str,
    ) -> Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
        """
        :raises iam.entities.access.account.EmptyAccountNameError:
        :raises iam.entities.access.password.ShortPasswordError:
        :raises iam.application.ports.map.NotUniqueAccountNameError:
        """

        current_time = await self.clock.get_current_time()

        account_name = AccountName(text=account_name_text)
        password = Password(text=password_text)

        signed_up_user = signed_up_user_when(
            current_time=current_time,
            password_hashing=self.password_hashing,
            account_name=account_name,
            password=password,
        )

        async with self.transaction_of((self.accounts, )):
            await self.map_to((self.accounts, ), signed_up_user)

            for account in signed_up_user.new_values:
                event = AccountCreatedEvent(account=account)
                await self.event_queue.push(event)

        encoded_access_token = await self.access_token_encoding.encoded(
            just(signed_up_user).session.access_token
        )
        encoded_refresh_token = await self.refresh_token_encoding.encoded(
            just(signed_up_user).session.refresh_token
        )
        return Output(
            encoded_access_token=encoded_access_token,
            encoded_refresh_token=encoded_refresh_token,
        )
