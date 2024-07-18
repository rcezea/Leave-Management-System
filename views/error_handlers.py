#!/usr/bin/env python3
"""
error_handlers.py
Error handling views
"""
from views import app_views
from flask import abort, request, render_template
from views.user_views import auth


# Global error handlers

# Error handling for 404 Not Found errors
@app_views.errorhandler(404)
def not_found_error(error):
    error = str(error).split(':')
    return render_template('auth/error.html', error=error)


# Error handling for 401 Unauthorized errors
@app_views.errorhandler(401)
def unauthorized_error(error):
    error = str(error).split(':')
    return render_template('auth/error.html', error=error)


# Error handling for 403 Forbidden errors
@app_views.errorhandler(403)
def forbidden_error(error):
    error = str(error).split(':')
    return render_template('auth/error.html', error=error)


# Error handling for 400 Bad Request errors
@app_views.errorhandler(400)
def bad_request_error(error):
    error = str(error).split(':')
    return render_template('auth/error.html', error=error)


@app_views.before_request
def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        excluded_paths = [
            '/auth/login',
            '/auth/register',
        ]
        if auth.require_auth(request.path, excluded_paths):
            if not (auth.authorization_header(request) or
                    auth.session_cookie(request)):
                abort(401)
            auth.__current_user = auth.current_user(request)
            if auth.__current_user is None:
                abort(401)


@app_views.after_request
def stateless(response):
    auth.__current_user = None
    return response
