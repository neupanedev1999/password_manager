from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

def encrypt_password(password, key):
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return iv + encrypted_password

def decrypt_password(encrypted_password, key):
    iv = encrypted_password[:16]  # The first 16 bytes are the IV
    encrypted_password = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_password) + decryptor.finalize()
