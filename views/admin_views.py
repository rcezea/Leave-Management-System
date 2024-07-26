#!/usr/bin/env python3
"""
admin_views.py
Manager/Administrator Endpoints
"""
import ast
import json
from datetime import datetime, date

from views import app_views
from flask import jsonify, abort, render_template
from views.user_views import auth, role_required
from views.leave_views import manager


def convert_json(application, user=False):
    """ Convert leave application to JSON """
    application_dict = json.loads(application.to_json())
    application_dict['start'] = application.start.isoformat()
    application_dict['end'] = application.end.isoformat()
    user_id = str(application_dict['userid'])
    data_dict = ast.literal_eval(user_id.replace("'", "\""))
    user_id = data_dict['$oid']
    user = auth._db.find_user_by(id=user_id)
    application_dict['username'] = f"{user.firstname} {user.lastname}"
    del application_dict['userid']
    return application_dict


# View Leave Applications
# Endpoint: GET /admin/leave-applications
# Description: View all leave applications submitted by employees.
@app_views.route('/admin/leave-applications',
                 methods=['GET'], strict_slashes=False)
@role_required('admin')
def admin_get_all_applications():
    """ View all leave applications """
    try:
        all_applications = manager.admin_get_all_applications()
        applications_list = sorted([convert_json(app) for app in all_applications],
                                   key=lambda x: ('pending', 'rejected', 'approved')
                                   .index(x['status'])
                                   )
        return render_template('dashboard/manage_leaves.html',
                               applications=applications_list, datetime=datetime, date=date)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Approve Leave
# Endpoint: PUT /admin/approve-leave/<leave_id>
# Description: Approve a leave application.
@app_views.route('/admin/approve-leave/<leave_id>',
                 methods=['PUT'], strict_slashes=False)
@role_required('admin')
def approve_leave(leave_id):
    """ Approve leave application """
    try:
        data_dict = ast.literal_eval(leave_id.replace("'", "\""))
        leave_id = data_dict['$oid']
        if manager.approve_leave_application(leave_id):
            return jsonify({"message": "Leave application approved"}), 200
        abort(400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Reject Leave
# Endpoint: PUT /admin/reject-leave/<leave_id>
# Description: Reject a leave application.
@app_views.route('/admin/reject-leave/<leave_id>',
                 methods=['PUT'], strict_slashes=False)
@role_required('admin')
def reject_leave(leave_id):
    """ Reject leave application """
    try:
        data_dict = ast.literal_eval(leave_id.replace("'", "\""))
        leave_id = data_dict['$oid']
        if manager.reject_leave_application(leave_id):
            return jsonify({"message": "Leave application rejected"}), 200
        abort(400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# View Employee Leave History
# Endpoint: GET /admin/employee-leave-history/<employee_id>
# Description: View the leave history of a specific employee.
@app_views.route('/admin/employee-leave-history/<employee_id>',
                 methods=['GET'], strict_slashes=False)
@role_required('admin')
def admin_get_all_by_user(employee_id):
    """ View leave history of an employee """
    try:
        last, first, email, all_applications = (
            manager.admin_get_all_user_applications(employee_id))
        applications_list = \
            [convert_json(app, True) for app in all_applications]
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
        user = auth.__current_user
        if not user:
            abort(401)

        employee = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": "*************",
        }
        applications = manager.admin_get_all_applications()
        applications = [convert_json(app) for app in applications]
        total, pending, approved, rejected = manager.get_stats()
        stats = {
            "total_leaves": total,
            "pending_leaves": pending,
            "approved_leaves": approved,
            "rejected_leaves": rejected,
        }
        applications = applications[0:7]
        return render_template('dashboard/Admin.html',
                               employee=employee, stats=stats, applications=applications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
