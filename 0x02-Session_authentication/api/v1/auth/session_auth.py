#!/usr/bin/env python3
"""Simple API session authentication class"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session authentication inheriting from auth"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create a session"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get user_id given the session id"""
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """get the current iser of a particular request"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroys session created"""
        if request is None:
            return False
        try:
            session_id = self.session_cookie(request)
        except Exception:
            return False
        try:
            user_id = self.user_id_for_session_id(session_id)
        except Exception as e:
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True
