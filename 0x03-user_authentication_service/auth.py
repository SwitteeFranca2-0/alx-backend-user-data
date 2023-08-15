#!/usr/bin/env python3
"""Auth for hashed pasword"""

import bcrypt
from db import DB
from user import User
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(pwd: str) -> bytes:
        """Converting a string to hashed password"""
        b_pwd = bytes(pwd, 'utf-8')
        return bcrypt.hashpw(b_pwd, bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Register user in authentication database"""
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user is not None:
            raise ValueError('User {} alreadyexists'.format(email))
        user = User(email=email, hashed_password=self._hash_password(password))
        try:
            session.add(user)
            session.commit()
        except Exception:
            session.rollback()
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login is valid"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(bytes(password, 'utf-8'), user.hashed_password)

    def _generate_uuid(self) -> str:
        """generate uuid from the module"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """create a session"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Function to get user from session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """DEstroy a session"""
        if user_id is not None:
            try:
                user = self._db.find_user_by(user_id=user_id)
            except Exception:
                return None
            self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get the password reset token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password of a user"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed = self._hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
        return None
