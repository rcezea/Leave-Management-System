#!/usr/bin/env python3
"""
user_views.py
Employee (User) views
"""

from flask import jsonify, request, abort, make_response, redirect
from views import app_views
from authentication.auth import Auth

auth = Auth()


# User Registration
# Endpoint: POST /auth/register
# Description: Register a new user (employee or admin).
@app_views.route('/auth/register', methods=['POST'], strict_slashes=False)
def register():
    """ User registration """
    email = request.form.get("email")
    password = request.form.get("password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    role = request.form.get("role") or None
    try:
        auth.register_user(email, password, firstname, lastname, role)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400


# User Login
# Endpoint: POST /auth/login
# Description: Authenticate and log in a user.
@app_views.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """ route user login """
    email = request.form.get("email")
    password = request.form.get("password")
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        resp = make_response(jsonify({"message": "Login successful"}), 200)
        resp.set_cookie("session_id", session_id, httponly=True, secure=True)
        return resp
    abort(401)


# User Logout
# Endpoint: POST /auth/logout
# Description: Log out the current user.
@app_views.route('/auth/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ User logout """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user.email)
        resp = redirect('/')
        resp.set_cookie("session_id", '', expires=0, httponly=True, secure=True)  # Delete the cookie
        return resp
    abort(403)


# Update User Profile
# Endpoint: PUT /user/profile
# Description: Update user profile information.
@app_views.route('/user/profile', methods=['GET', 'PUT'], strict_slashes=False)
def user():
    """ implement a profile """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(401)
    if request.method == 'GET':
        employee = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": "*************",
            "session_id": user.session_id,
        }
        return jsonify({"Employee": employee}), 200
    elif request.method == 'PUT':
        form_data = request.form
        kwargs = {key: form_data[key] for key in form_data}
        if auth.update_user(user.email, **kwargs):
            return jsonify({"message": "User updated successfully"}), 202
        return jsonify({"error": "User update failed"}), 400
    abort(400)
