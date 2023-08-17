#!/usr/bin/env python3
"""App flask script """

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def int():
    """Initialling routing"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ADd user to the database"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Log in function"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """log out of session"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('int'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Get the profile in a request"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    email = request.form.get('email')
    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Update password"""
    email = request.form.get('email')
    token = request.form.get('reset_token')
    new_pwd = request.form.get('new_password')
    try:
        AUTH.update_password(token, new_pwd)
    except Exception:
        abort(403)
    return jsonify({'email': email, 'meassage': 'Password updated'}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
