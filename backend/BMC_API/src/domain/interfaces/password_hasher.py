# backend/BMC_API/src/domain/interfaces/password_hasher.py

from typing import Protocol


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...

    def verify(self, plain_password: str, hashed_password: str) -> bool: ...
