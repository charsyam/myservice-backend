from argon2 import PasswordHasher
from core.utils.crypto.rsa import RSA


ph = PasswordHasher()


def decrypt_password(private_key, encrypted_password):
    return RSA.decrypt(private_key, encrypted_password)


def password_hasher(password):
    return ph.hash(password)


def password_verify(password1, password2):
    ph.verify(password1, password2)
