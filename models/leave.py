#!/usr/bin/env python3
"""
leave.py
Control Leave processing
"""
from models.db import DB


def is_valid_objectid(id):
    try:
        from bson import ObjectId
        from bson.errors import InvalidId
        ObjectId(id)
        return True
    except (InvalidId, TypeError):
        return False


class LeaveManager:
    """ Leave Manager class """

    def __init__(self, auth_instance):
        super().__init__()
        self._auth = auth_instance
        self._db = DB()

    def create_leave_application(self, email, **kwargs):
        try:
            leave = self._db.create_leave_application(email, kwargs=kwargs)
            return leave
        except Exception as e:
            raise e

    def get_all_applications_by_user(self, userid):
        try:
            if not is_valid_objectid(userid):
                raise ValueError("Application does not exist")
            return self._db.all_by_user(userid=userid)
        except Exception as e:
            raise e

    def delete_leave(self, user, leave_id):
        try:
            if not is_valid_objectid(leave_id):
                raise ValueError("Application does not exist")
            if self._db.delete_application(user.email, leave_id=leave_id):
                return True
        except ValueError as e:
            raise e

    def admin_get_all_applications(self):
        return self._db.all()

    def admin_get_all_user_applications(self, userid):
        if not is_valid_objectid(userid):
            raise ValueError("Application does not exist")
        user = self._db.find_user_by(id=userid)
        application = (user.lastname, user.firstname, user.email,
                       self.get_all_applications_by_user(userid))
        return application

    def reject_leave_application(self, leave_id):
        if is_valid_objectid(leave_id):
            return self._db.approve_reject_leave(leave_id, status="rejected")
        raise ValueError("Application does not exist")

    def approve_leave_application(self, leave_id):
        if is_valid_objectid(leave_id):
            return self._db.approve_reject_leave(leave_id, status="approved")
        raise ValueError("Application does not exist")

    def get_stats(self):
        return self._db.leave_statistics()

    def get_leave_balance(self, user_id):
        """ Retrieve remaining leave balance for a user """
        try:
            return self._db.leave_balance(user_id)
        except ValueError as e:
            raise ValueError(e)
        except Exception as e:
            raise Exception("Failed to retrieve leave balance: " + str(e))
