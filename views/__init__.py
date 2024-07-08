#!/usr/bin/env python3
"""
views.__init__
Blueprint Initialization
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from views.admin_views import *
from views.leave_views import *
from views.user_views import *
from views.error_handlers import *
