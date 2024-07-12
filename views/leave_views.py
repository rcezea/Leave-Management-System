#!/usr/bin/env python3
"""
leave_vies.py
Leave processing views
"""
from mongoengine import DoesNotExist, ValidationError

from views import app_views
from flask import jsonify, request, abort
from models.leave import LeaveManager
from views.user_views import auth, role_required
import json


manager = LeaveManager(auth)


# Employee Endpoints
# Endpoint: POST /leave/apply
# Description: Submit a new leave application.
@app_views.route('/leave/apply', methods=["POST"], strict_slashes=False)
@role_required('employee')
def apply():
    """ Submit a new leave application """
    try:
        user = auth.__current_user
        form_data = request.form
        kwargs = {key: form_data[key] for key in form_data}
        kwargs.update(userid=user.id)
        leave = manager.create_leave_application(user.email,
                                                 **kwargs)
        if leave:
            return (jsonify({"message": "Application submitted successfuly"}),
                    201)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
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
@app_views.route('/leave/status', methods=["GET"], strict_slashes=False)
@role_required('employee')
def status():
    """ View leave application status """
    try:
        user = auth.__current_user
        applications = manager.get_all_applications_by_user(user.id)
        applications_list = [convert_dates(app) for app in applications]
        return jsonify({"leave_applications": applications_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Cancel Leave Application
# Endpoint: DELETE /leave/cancel/<leave_id>
# Description: Cancel a pending leave application.
@app_views.route('/leave/cancel/<leave_id>', methods=["DELETE"],
                 strict_slashes=False)
@role_required('employee')
def cancel_leave(leave_id):
    """ Cancel a pending leave application """
    try:
        user = auth.__current_user
        if manager.delete_leave(user, leave_id):
            return jsonify({"message": "Application "
                                       "deleted successfully"}), 200
        return jsonify({"error": f"Error deleting leave "
                                 f"application {leave_id}"}), 500
    except Exception as e:
        return jsonify({'error': f'Error deleting leave '
                                 f'application {leave_id}: {str(e)}'}), 500


# View Leave Balance
# Endpoint: GET /leave/balance
# View the remaining leave balance for the current user
@app_views.route('/leave/balance', methods=["GET"], strict_slashes=False)
@role_required('employee')
def leave_balance():
    """ View the remaining leave balance for the current user """
    try:
        user = auth.__current_user
        balance = manager.get_leave_balance(user.id)
        return jsonify({"leave_balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
