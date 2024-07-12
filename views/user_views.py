#!/usr/bin/env python3
"""
user_views.py
Employee (User) views
"""
import base64
import json
from functools import wraps

from flask import jsonify, request, abort, make_response, redirect, render_template
from views import app_views
from authentication.auth import Auth

auth = Auth()


def role_required(role):
    """ Role-based access decorator """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_id = request.cookies.get("session_id")
            if not session_id:
                abort(401)  # Unauthorized if no session_id found

            user = auth.get_user_from_session_id(session_id)
            if not user:
                abort(401)  # Unauthorized if no user found

            if user.role != role:
                abort(403)  # Forbidden if role does not match

            return f(*args, **kwargs)  # Call the original function

        return decorated_function

    return decorator


# User Registration
# Endpoint: POST /auth/register
# Description: Register a new user (employee or admin).
@app_views.route('/auth/register', methods=['POST'], strict_slashes=False)
def register():
    """ User registration """
    email = request.form.get("email")
    form_data = request.form
    kwargs = {key: form_data[key] for key in form_data}
    try:
        auth.register_user(**kwargs)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Login
# Endpoint: POST /auth/login
# Description: Authenticate and log in a user.
@app_views.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """ route user login """
    authHeader = auth.authorization_header(request)
    if authHeader:
        authHeader = authHeader.split(" ")[1]
        authHeader = base64.b64decode(authHeader).decode('utf-8')
        authHeader = authHeader.split(":")
    print(authHeader)
    email = request.form.get("email") or authHeader[0]
    password = request.form.get("password") or authHeader[1]
    try:
        if auth.valid_login(email, password):
            session_id = auth.create_session(email)
            resp = make_response(jsonify({"message": "Login successful"}), 200)
            resp.set_cookie(
                "session_id", session_id, httponly=True, secure=True)
            return resp
        abort(401)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Logout
# Endpoint: POST /auth/logout
# Description: Log out the current user.
@app_views.route('/auth/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ User logout """
    try:
        session_id = request.cookies.get("session_id")
        auth.destroy_session(session_id)
        resp = redirect('/')
        resp.set_cookie("session_id", '',  # Delete the cookie
                        expires=0, httponly=True, secure=True)
        auth.__current_user = None
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update User Profile
# Endpoint: PUT /user/profile
# Description: Update user profile information.
@app_views.route('/user/profile', methods=['GET', 'PUT'], strict_slashes=False)
@role_required('employee')
def user():
    """ implement a profile """
    try:
        user = auth.__current_user
        if not user:
            abort(401)
        if request.method == 'GET':
            applications = \
                [convert_dates(app) for app in user.applications] \
                if user.applications else []
            employee = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "password": "*************",
                "applications": applications
            }
            return render_template('auth/index1.html', user=employee), 200
        elif request.method == 'PUT':
            form_data = request.form
            kwargs = {key: form_data[key] for key in form_data}
            if auth.update_user(user.email, **kwargs):
                return jsonify({"message": "User updated successfully"}), 202
            return jsonify({"error": "User update failed"}), 400
        abort(400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def convert_dates(application):
    application_dict = json.loads(application.to_json())
    application_dict['start'] = application.start.isoformat()
    application_dict['end'] = application.end.isoformat()
    del application_dict['userid']
    return application_dict
