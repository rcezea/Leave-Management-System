#!/usr/bin/env python3
"""
admin_views.py
Manager/Administrator Endpoints
"""
import json
from functools import wraps

from views import app_views
from flask import jsonify, request, abort
from views.user_views import auth
from views.leave_views import manager


# admin decorator
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


def convert_json(application, user=False):
    """ Convert leave application to JSON """
    application_dict = json.loads(application.to_json())
    application_dict['start'] = application.start.isoformat()
    application_dict['end'] = application.end.isoformat()
    if user:
        del application_dict['userid']
    return application_dict


# View Leave Applications
# Endpoint: GET /admin/leave-applications
# Description: View all leave applications submitted by employees.
@app_views.route('/admin/leave-applications', methods=['GET'], strict_slashes=False)
@role_required('admin')
def admin_get_all_applications():
    """ View all leave applications """
    try:
        all_applications = manager.admin_get_all_applications()
        applications_list = [convert_json(app) for app in all_applications]
        return jsonify({"Applications": applications_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Approve Leave
# Endpoint: PUT /admin/approve-leave/<leave_id>
# Description: Approve a leave application.
@app_views.route('/admin/approve-leave/<leave_id>', methods=['PUT'], strict_slashes=False)
@role_required('admin')
def approve_leave(leave_id):
    """ Approve leave application """
    try:
        if manager.approve_leave_application(leave_id):
            return jsonify({"message": "Leave application approved"}), 200
        abort(400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Reject Leave
# Endpoint: PUT /admin/reject-leave/<leave_id>
# Description: Reject a leave application.
@app_views.route('/admin/reject-leave/<leave_id>', methods=['PUT'], strict_slashes=False)
@role_required('admin')
def reject_leave(leave_id):
    """ Reject leave application """
    try:
        if manager.reject_leave_application(leave_id):
            return jsonify({"message": "Leave application rejected"}), 200
        abort(400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# View Employee Leave History
# Endpoint: GET /admin/employee-leave-history/<employee_id>
# Description: View the leave history of a specific employee.
@app_views.route('/admin/employee-leave-history/<employee_id>', methods=['GET'], strict_slashes=False)
@role_required('admin')
def admin_get_all_by_user(employee_id):
    """ View leave history of an employee """
    try:
        last, first, email, all_applications = manager.admin_get_all_user_applications(employee_id)
        applications_list = [convert_json(app, True) for app in all_applications]
        administrator = {
            "name": last + " " + first,
            "email": email
        }
        applications_list.insert(0, administrator)
        return jsonify({"Applications": applications_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Admin Dashboard
# Endpoint: GET /admin/dashboard
# Description: View admin-specific dashboard data and statistics.
@app_views.route('/admin/dashboard', methods=['GET'], strict_slashes=False)
@role_required('admin')
def admin():
    """ View admin dashboard """
    try:
        session_id = request.cookies.get("session_id")
        user = auth.get_user_from_session_id(session_id)
        if not user:
            abort(401)

        employee = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": "*************",
            "session_id": user.session_id,
        }
        total, pending, approved = manager.get_stats()
        stats = {
            "total_leaves": total,
            "pending_leaves": pending,
            "approved_leaves": approved,
        }
        return jsonify({
            "Admin": employee,
            "Statistics": stats
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Admin Create Leave Type
# Endpoint: POST /admin/leave-type
# Description: Create a new type of leave (e.g., paternity leave).

# Admin Update Leave Type
# Endpoint: PUT /admin/leave-type/<type_id>
# Description: Update an existing leave type.

# Admin Delete Leave Type
# Endpoint: DELETE /admin/leave-type/<type_id>
# Description: Delete an existing leave type.
