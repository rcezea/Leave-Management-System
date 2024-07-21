#!/usr/bin/env python3
"""
views.__init__
Blueprint Initialization
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from views import admin_views
from views.leave_views import *
from views.user_views import *
from views.error_handlers import *


@app_views.route('/')
def hello_world():
    return render_template('auth/authentication.html')
