# coding: utf-8

from hashlib import sha256


def hash_password(password):
    return sha256(password).hexdigest()


def verify_password(password, hash_password):
    hash = sha256(password).hexdigest()
    if hash == hash_password:
        return True
    else:
        return False
