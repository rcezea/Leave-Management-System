#!/usr/bin/env python3
"""
error_handlers.py
Error handling views
"""
from views import app_views
from flask import abort, request, jsonify
from views.user_views import auth


# Global error handlers

# Error handling for 404 Not Found errors
@app_views.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


# Error handling for 401 Unauthorized errors
@app_views.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized"}), 401


# Error handling for 403 Forbidden errors
@app_views.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "Forbidden"}), 403


# Error handling for 400 Bad Request errors
@app_views.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request"}), 400


@app_views.before_request
def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        excluded_paths = [
            '/unauthorized/',
            '/forbidden/',
            '/auth/login/',
            '/auth/register/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            if not (auth.authorization_header(request) or
                    auth.session_cookie(request)):
                print("Aborting1")
                abort(401)
            if auth.current_user(request) is None:
                print("Aborting2")
                abort(403)
