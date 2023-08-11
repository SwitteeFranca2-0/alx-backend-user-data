#!/usr/bin/env python3
"""Simple API session authentication class"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from uuid import uuid4
from flask import request, jsonify, session

class SessionDBAuth(Auth):
    """Class to sort out storing session db"""
    