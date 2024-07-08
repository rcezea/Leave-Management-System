#!/usr/bin/env python3
"""
db.py
Database Initialization
"""

import uuid
from datetime import date
import mongoengine
from models.user import User, Leave
from flask import jsonify


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())


class DB:
    """ Class for CRUD operations on the database """

    def __init__(self):
        mongoengine.connect(db='leave_management_system', alias='core', host='localhost')

    def create_user(self, email, password, firstname, lastname, role=None):
        """ Create a new user """
        user = User()
        user.email = email
        user.password = password.decode('utf-8')
        user.firstname = firstname
        user.lastname = lastname
        if role == 'admin':
            user.role = role
        user.save()
        return True

    def create_leave_application(self, email, kwargs=None):
        """ Create a new leave application """
        user = self.find_user_by(email=email)
        start = kwargs.get('start')
        end = kwargs.get("end")
        type = kwargs.get("type")
        reason = kwargs.get("reason")
        status = kwargs.get("status")
        leave = Leave(start=start, end=end, type=type,
                      reason=reason, status=status, userid=user.id)
        leave.save()
        user.applications.append(leave.id)
        user.save()
        return True

    def find_user_by(self, email=None, id=None):
        """ Find user by email or ID """
        if email:
            return User.objects(email=email).first()
        if id:
            return User.objects(id=id).first()
        return None

    def find_leave_by(self, user=None, leave_id=None):
        """ Find leave application by user or leave ID """
        if user and leave_id:
            return Leave.objects(userid=user.id, id=leave_id).first()
        if leave_id:
            return Leave.objects(id=leave_id).first()
        return None

    def all(self):
        """ Retrieve all leave applications """
        return Leave.objects()

    def all_by_user(self, user_id):
        """ Retrieve all leave applications by user """
        return Leave.objects(userid=user_id)

    def leave_statistics(self):
        """ Retrieve leave statistics """
        total = Leave.objects().count()
        pending = Leave.objects(status=False).count()
        approved = Leave.objects(status=True).count()
        return total, pending, approved

    def update_user(self, email, **kwargs):
        """ Update user information """
        user = self.find_user_by(email=email)
        if user:
            for key, value in kwargs.items():
                if key != 'applications' and hasattr(user, key):
                    setattr(user, key, value)
            user.save()
            return True
        return False

    def approve_reject_leave(self, leave_id, status=False):
        """ Approve or reject leave application """
        leave = self.find_leave_by(leave_id=leave_id)
        if leave:
            leave.status = status
            leave.save()
            return True
        return False

    def leave_balance(self, user_id):
        """ Retrieve remaining leave balance for a user """
        user = self.find_user_by(id=user_id)
        if user:
            total_leave = 30  # Assuming 25 days annual leave per year
            applications = Leave.objects(userid=user.id, status=True, end__gte=date.today())
            used_leave = sum((app.end - app.start).days + 1 for app in applications)
            print(used_leave)
            remaining_leave = max(0, total_leave - used_leave)
            return remaining_leave
        return None

    def delete_application(self, email, leave_id):
        """ Delete a leave application """
        user = self.find_user_by(email)
        if user:
            leave = Leave.objects(userid=user.id, id=leave_id).first()
            if leave:
                user.applications = [app for app in user.applications if app.id != leave.id]
                leave.delete()
                user.save()
                return True
        return False

    def destroy_user(self, email):
        """ Delete a user and associated leave applications """
        user = self.find_user_by(email=email)
        if user:
            applications = Leave.objects(userid=user.id)
            for leave in applications:
                leave.delete()
            user.delete()
            return jsonify({"message": "User deleted successfully"}), 204
