#!/usr/bin/env python3
"""
leave_vies.py
Leave processing views
"""
from views import app_views
from flask import jsonify, request, abort
from models.leave import LeaveManager
from views.user_views import auth
import json

manager = LeaveManager(auth)


# Employee Endpoints
# Endpoint: POST /leave/apply
# Description: Submit a new leave application.
@app_views.route('/leave/apply', methods=["POST"], strict_slashes=False)
def apply():
    """ Submit a new leave application """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            start = request.form.get("start")
            end = request.form.get("end")
            type = request.form.get("type")
            reason = request.form.get("reason")
            leave = manager.create_leave_application(user.email,
                                                     start=start,
                                                     end=end,
                                                     type=type,
                                                     reason=reason,
                                                     status=False)
            if leave:
                return jsonify({"message": "Application submitted successfuly"}), 201
    abort(401)


def convert_dates(application):
    application_dict = json.loads(application.to_json())
    application_dict['start'] = application.start.isoformat()
    application_dict['end'] = application.end.isoformat()
    del application_dict['userid']
    return application_dict


# View Leave Status
# Endpoint: GET /leave/status
# Description: View the status of all leave applications submitted by the user.
@app_views.route('/leave/status/', methods=["GET"], strict_slashes=False)
def status():
    """ View leave application status """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            applications = manager.get_all_applications_by_user(user.id)
            applications_list = [convert_dates(app) for app in applications]
            return jsonify({"leave_applications": applications_list})
    abort(401)


# Cancel Leave Application
# Endpoint: DELETE /leave/cancel/<leave_id>
# Description: Cancel a pending leave application.
@app_views.route('/leave/cancel/<leave_id>', methods=["DELETE"], strict_slashes=False)
def cancel_leave(leave_id):
    """ Cancel a pending leave application """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            if manager.delete_leave_id(user, leave_id):
                return jsonify({"message": "Application deleted successfully"}), 200
            return jsonify({"error": "Cannot delete approved / deleted applications"}), 403
    abort(401)


# View Leave Balance
# Endpoint: GET /leave/balance
# View the remaining leave balance for the current user
@app_views.route('/leave/balance', methods=["GET"], strict_slashes=False)
def leave_balance():
    """ View remaining leave balance """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            remaining_leave = manager.get_leave_balance(user.id)
            if remaining_leave is not None:
                return jsonify({"remaining_leave_days": remaining_leave}), 200
            return jsonify({"error": "Failed to retrieve leave balance"}), 500
    abort(401)
