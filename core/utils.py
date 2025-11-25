import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(passwd: str | bytes) -> str:
    return password_hash.hash(passwd)

def verify_password(plain: str | bytes, hashed: str | bytes) -> bool:
    return password_hash.verify(plain, hashed)

