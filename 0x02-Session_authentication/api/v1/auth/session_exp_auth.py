#!/usr/bin/env python3
"""Simple API session authentication class"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiry authentication"""
    session_dictionary = {}

    def __init__(self) -> None:
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload the inherited function"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.utcnow()}
        SessionExpAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """"Overloading the inherited function"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        s_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return s_dict.get('user_id')
        if 'created_at' not in s_dict:
            return None
        time_now = datetime.now()
        time_duration = timedelta(seconds=self.session_duration)
        time_of_exp = s_dict['created_at'] + time_duration
        if time_of_exp < time_now:
            return None
        return s_dict.get('user_id')
