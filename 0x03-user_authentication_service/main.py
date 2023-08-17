#!/usr/bin/env python3
"""
Main file
"""
import requests

base = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """Function querying th register user route"""
    payload = {'email': email, 'password': password}
    r = requests.post(base+'/users', data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    r = requests.post(base+'/users', data=payload)
    assert r.status_code == 400
    assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Function to test log in with wrong password"""
    payload = {'email': email, 'password': password}
    r = requests.post(base+'/sessions', data=payload)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Function to query the log in nroute"""
    payload = {'email': email, 'password': password}
    r = requests.post(base+'/sessions', data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """Profile unlogged"""
    r = requests.get(base+'/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """Prfile logged querying"""
    cookies = {'session_id': session_id}
    r = requests.get(base+'/profile', cookies=cookies)
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Profile logging out query"""
    cookies = {'session_id': session_id}
    r = requests.delete(base+'/sessions', cookies=cookies)
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset password token"""
    r = requests.post(base+'/reset_password', data={'email': email})
    assert r.status_code == 200
    assert 'email' in r.json()
    assert r.json().get('email') == email
    assert 'reset_token' in r.json()
    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password requests"""
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    r = requests.put(base+'/reset_password', data=payload)
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
