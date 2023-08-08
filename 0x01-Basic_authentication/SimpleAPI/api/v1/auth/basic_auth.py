#!/usr/bin/env python3
"""Simple API basic authentication class"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class inheriting from auth class"""

    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract based64 authorization header"""
        auth_h = authorization_header
        if auth_h is None or type(auth_h) != str or auth_h[0:6] != "Basic ":
            return None
        return auth_h[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode strung from authorization header"""
        bAuth = base64_authorization_header
        if bAuth is None or type(bAuth) != str:
            return None
        try:
            decode = base64.b64decode(bAuth).decode('utf-8')
            return decode
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract user credentials from authorization header"""
        dAuth = decoded_base64_authorization_header
        if dAuth is None or type(dAuth) != str or ":" not in dAuth:
            return (None, None)
        info = dAuth.split(":")
        if len(info) > 2:
            pwd = (":").join(info[1:])
            info[1] = pwd
        return (info[0], info[1])

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Get user object from credentials"""
        uEm = user_email
        uPw = user_pwd
        if uEm is None or type(uEm) != str or uPw is None or type(uPw) != str:
            return None
        if len(User.all()) != 0:
            users = User.search({"email": uEm})
        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(uPw) is True:
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user function"""
        auth = self.authorization_header(request)
        encoded_info = self.extract_base64_authorization_header(auth)
        decoded_info = self.decode_base64_authorization_header(encoded_info)
        user_credentials = self.extract_user_credentials(decoded_info)
        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
        return user
