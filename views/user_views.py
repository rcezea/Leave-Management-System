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
@app_views.route('/auth/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ User logout """
    try:
        session_id = request.cookies.get("session_id")
        auth.destroy_session(session_id)
        resp = jsonify({"message": "Logged out successfully"})
        resp.set_cookie("session_id", '',  # Delete the cookie
                        expires=0, httponly=True, secure=True)
        auth.__current_user = None
        return redirect('/')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get User Profile
# Endpoint: GET /user/profile
# Description: GET user profile information.
@app_views.route('/user/profile', methods=['GET'], strict_slashes=False)
def user():
    """ implement a profile """
    user = auth.__current_user
    try:
        if not user:
            abort(401)
        if user.role == 'admin':
            return redirect('/admin/dashboard')
        pending = 0
        rejected = 0
        approved = 0
        if request.method == 'GET':
            applications = \
                [convert_dates(app) for app in user.applications] \
                    if user.applications else []
            total = len(applications)
            for item in applications:
                if item["status"] == 'pending':
                    pending += 1
                elif item["status"] == 'approved':
                    approved += 1
                elif item["status"] == 'rejected':
                    rejected += 1
            employee = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "password": "*************",
                "applications": applications,
                "pending": pending,
                "rejected": rejected,
                "approved": approved,
                "total": total,
            }
            # Render a different dashboard based on the role
            return render_template('dashboard/employee_dashboard.html', employee=employee)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def convert_dates(application):
    application_dict = json.loads(application.to_json())
    application_dict['start'] = application.start.isoformat()
    application_dict['end'] = application.end.isoformat()
    del application_dict['userid']
    return application_dict


# Update User Profile
# Endpoint: GET /user/profile renders the change password page
# Endpoint: PUT /user/profile updates the user's password
# Description: Update user profile information.
@app_views.route('/user/update', methods=['GET', 'PUT'], strict_slashes=False)
def update():
    user = auth.__current_user
    try:
        if request.method == "GET":
            employee = {
                "firstname": user.firstname,
                "lastname": user.lastname,
            }
            return render_template('dashboard/change_password.html', employee=employee)
        form_data = request.form
        kwargs = {key: form_data[key] for key in form_data}
        if auth.update_user(user.email, **kwargs):
            return jsonify({"message": "User updated successfully"}), 202
        return jsonify({"error": "User update failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
