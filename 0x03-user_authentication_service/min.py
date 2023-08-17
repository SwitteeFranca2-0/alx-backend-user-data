#!/usr/bin/env python3
"""Athenticatio"""
from auth import Auth
from db import DB
from user import User
auth = Auth()
db = DB()

email = 'switt@fran.com'
pwd = 'Fran23'

user = auth.register_user(email, pwd)
token = auth.get_reset_password_token(email)
print(token)
print(token)
print(user.reset_token)
user = auth._db.find_user_by(reset_token=token)
print(user.email)
auth.update_password(token, 'nostra')
print(user.hashed_password)