#!/usr/bin/env python3
"""Simple API session authentication class"""

from models.user import User
from uuid import uuid4
from api.v1.views import app2_views
from flask import request, jsonify, abort
from os import getenv as env


@app2_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """get seesion login information"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is "" or email is None:
        return jsonify({"error": "email missing"}), 400
    if password is "" or password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    for user in users:
        if user.is_valid_password(password) is True:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(env('SESSION_NAME'), session_id)
            return res
    return jsonify({ "error": "wrong password" }), 401
    
@app2_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout from session"""
    from api.v1.app import auth
    bool_res = auth.destroy_session(request)
    if bool_res is False:
        return False, abort(404)
    return jsonify({}), 200