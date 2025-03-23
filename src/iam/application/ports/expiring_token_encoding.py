from abc import ABC, abstractmethod

from iam.entities.access.token import ExpiringToken


class ExpiringTokenEncoding[TokenT: ExpiringToken, EncodedTokenT](ABC):
    @abstractmethod
    async def encoded(self, token: TokenT, /) -> EncodedTokenT: ...

    @abstractmethod
    async def decoded(
        self, encoded_token: EncodedTokenT, /
    ) -> TokenT | None: ...
