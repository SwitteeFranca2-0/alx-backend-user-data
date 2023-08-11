#!/usr/bin/env python3
"""Athentication class"""

from typing import List, TypeVar
import os


class Auth:
    """Authentication class"""

    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication function"""
        if path and path[-1] != "/":
            path += "/"
        if excluded_paths is not None and path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header function"""
        if request and 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This returns none"""
        return None

    def session_cookie(self, request=None):
        """get the session id from the session cookie yoki"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if session_name == '_my_session_id':
            return request.cookies.get('_my_session_id')
