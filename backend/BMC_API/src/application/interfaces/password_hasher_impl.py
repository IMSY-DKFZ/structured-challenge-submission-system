# backend/BMC_API/src/application/interfaces/password_hasher_impl.py

import bcrypt

from BMC_API.src.domain.interfaces.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode(
            "utf-8"
        )

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if not isinstance(plain_password, bytes):
            plain_password = plain_password.encode("utf-8")
        if not isinstance(hashed_password, bytes):
            hashed_password = hashed_password.encode("utf-8")
        return bcrypt.checkpw(plain_password, hashed_password)
