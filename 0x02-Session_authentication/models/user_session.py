#!/usr/bin/env python3
"""Create a user session class"""

from models.base import Base


class UserSession(Base):
    """class to store session ids"""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
