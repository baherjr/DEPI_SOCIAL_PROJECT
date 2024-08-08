import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt.hex() + hashed_password
