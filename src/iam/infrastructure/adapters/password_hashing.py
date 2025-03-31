from dataclasses import dataclass

import bcrypt

from iam.entities.access.password import Password, PasswordHash, PasswordHashing


@dataclass(frozen=True, kw_only=True, slots=True)
class BcryptPasswordHashing(PasswordHashing):
    def hash_of(self, password: Password) -> PasswordHash:
        encoded_hash = bcrypt.hashpw(password.text.encode(), bcrypt.gensalt())

        return PasswordHash(text=encoded_hash.decode())

    def is_hash_valid(
        self,
        password_hash: PasswordHash,
        *,
        password: Password,
    ) -> bool:
        return bcrypt.checkpw(
            password.text.encode(),
            password_hash.text.encode(),
        )
