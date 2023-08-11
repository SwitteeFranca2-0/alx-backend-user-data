#!/usr/bin/env python3
"""Encrypt password in database"""
import bcrypt


def hash_password(password: str) -> bytes:
    pwd = bytes(password, 'utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
        return True
    return False
