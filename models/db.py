#!/usr/bin/env python3
"""
db.py
Database Initialization
"""

import uuid
from datetime import date, datetime, timedelta
import mongoengine
from models.user import User, Leave
from flask import jsonify


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())


class DB:
    """ Class for CRUD operations on the database """

    def __init__(self):
        mongoengine.connect(db='leave_management_system',
                            alias='core', host='localhost')

    def create_user(self, **kwargs):
        """ Create a new user """
        try:
            user = User(**kwargs)
            user.save()
            return True
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    def create_leave_application(self, email, kwargs=None):
        """
        Create a new leave application and append to user's applications
        :param email: user email
        :param kwargs: dictionary containing start, end, type, reason, status
        :return: True if successfully created, False otherwise
        """
        try:
            user = User.objects(email=email).first()
            if not user:
                raise ValueError("User not found")

            if self.check_leave_balance(user, kwargs['start'], kwargs['end']):
                # Create leave application and save
                leave = Leave(**kwargs)
                leave.save()

                # Update user's applications
                user.applications.append(leave.id)
                user.save()
                return True
            else:
                raise Exception("Insufficient leave balance")
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Error creating leave application: {str(e)}")

    def find_user_by(self, email=None, id=None):
        """ Find user by email or ID """
        try:
            if email:
                return User.objects(email=email).first()
            if id:
                return User.objects(id=id).first()
            return None
        except Exception as e:
            raise Exception(f"Error finding user: {str(e)}")

    def find_leave_by(self, user=None, leave_id=None):
        """ Find leave application by user or leave ID """
        try:
            if user and leave_id:
                print(user)
                return Leave.objects(userid=user.id, id=leave_id).first()
            if leave_id:
                return Leave.objects(id=leave_id).first()
            return None
        except Exception as e:
            raise Exception(f"Error finding leave for user "
                            f"{user.id} and leave_id {leave_id}: {str(e)}")

    def all(self):
        """ Retrieve all leave applications """
        return Leave.objects()

    def all_by_user(self, userid):
        """ Retrieve all leave applications by user """
        try:
            return Leave.objects(userid=userid)
        except Exception as e:
            raise Exception(f"Error retrieving applications "
                            f"for user {userid}: {str(e)}")

    def leave_statistics(self):
        """ Retrieve leave statistics """
        total = Leave.objects().count()
        pending = Leave.objects(status="pending").count()
        rejected = Leave.objects(status="rejected").count()
        approved = Leave.objects(status="approved").count()
        return total, pending, approved, rejected

    def update_user(self, email, **kwargs):
        """ Update user information """
        user = self.find_user_by(email=email)
        if user:
            for key, value in kwargs.items():
                if ((key != 'applications', key != 'email')
                        and hasattr(user, key)):
                    setattr(user, key, value)
            user.save()
            return True
        return False

    def approve_reject_leave(self, leave_id, status):
        """ Approve or reject leave application """
        leave = self.find_leave_by(leave_id=leave_id)
        if leave:
            leave.status = status
            leave.save()
            return True
        return False

    def leave_balance(self, user_id):
        """ Retrieve remaining leave balance for a user """
        try:
            total_leave = 30  # Assuming 25 days annual leave per year
            applications = Leave.objects(
                userid=user_id, status="approved", end__gte=date.today())
            used_leave = sum((app.end - app.start).days + 1
                             for app in applications)
            remaining_leave = max(0, total_leave - used_leave)
            return remaining_leave
        except Exception as e:
            raise Exception("Failed to retrieve leave balance: " + str(e))

    def check_leave_balance(self, user, start, end) -> bool:
        """ Checks that balance is enough for new application"""
        try:
            balance = self.leave_balance(user_id=user.id)
            print(balance)
            end = datetime.strptime(end, '%Y-%m-%d').date()
            start = datetime.strptime(start, '%Y-%m-%d').date()
            duration = (end - start).days + 1
            print(balance > duration)
            return balance > duration
        except Exception as e:
            raise Exception(e)

    def delete_application(self, email, leave_id):
        """ Delete a leave application """
        user = User.objects(email=email).first()
        if not user:
            raise ValueError("User not found.")
        leave = Leave.objects(id=leave_id).first()
        if leave and leave.status is not "pending":
            user.applications =\
                [app for app in user.applications if app.id != leave.id]
            leave.delete()
            user.save()
            return True
        else:
            raise ValueError("Can't find pending application.")

    def destroy_user(self, email):
        """ Delete a user and associated leave applications """
        user = self.find_user_by(email=email)
        if user:
            applications = Leave.objects(userid=user.id)
            for leave in applications:
                leave.delete()
            user.delete()
            return jsonify({"message": "User deleted successfully"}), 204
