#!/usr/bin/env python3
"""Simple API session authentication class"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Class to sort out storing session db"""

    def create_session(self, user_id=None):
        """create a usersession instamce"""
        session_id = super().create_session(user_id)
        dict_obj = {'session_id': session_id, 'user_id': user_id}
        user_session = UserSession(**dict_obj)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Request user id for a session"""
        if session_id is None:
            return None
        try:
            obj = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(obj) == 0:
            return None
        time_now = datetime.now()
        time_duration = timedelta(seconds=self.session_duration)
        time_of_exp = obj[0].created_at + time_duration
        if time_of_exp < time_now:
            return None
        return obj[0].user_id

    def destroy_session(self, request=None):
        """destroy the session of a session id"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            obj = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        obj[0].remove()
