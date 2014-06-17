# coding: utf-8

from hashlib import sha256


def hash_pass(password):
    return sha256(password).hexdigest()


def verify_password(password, password_hash):
    hashed_password = sha256(password).hexdigest()
    if hashed_password ==  password_hash:

        return True
    else:
        return False
