#!/usr/bin/env python3
"""Athentication class"""

from flask import request
from typing import List, TypeVar


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
