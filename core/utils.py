
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(passwd: str | bytes) -> str:
    """Hash password with the recommended algorithm"""
    return password_hash.hash(passwd)

def verify_password(plain: str | bytes, hashed: str | bytes) -> bool:
    """Verifies if the hashed password is equal to the plain password"""
    return password_hash.verify(plain, hashed)

