#!/usr/bin/env python3
"""
leave.py
Control Leave processing
"""
from models.db import DB

def is_valid_objectid(id):
    """
    Validate if the given id is a valid ObjectId.
    
    Args:
        id (str): The id to validate.
    
    Returns:
        bool: True if the id is valid, False otherwise.
    """
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
        """
        Initialize the LeaveManager class.
        
        Args:
            auth_instance: An instance of the authentication manager.
        """
        super().__init__()
        self._auth = auth_instance
        self._db = DB()

    def create_leave_application(self, email, **kwargs):
        """
        Create a leave application for a user.
        
        Args:
            email (str): The email of the user.
            **kwargs: Additional leave application details.
        
        Returns:
            dict: The created leave application.
        
        Raises:
            Exception: If there's an error creating the leave application.
        """
        try:
            leave = self._db.create_leave_application(email, kwargs=kwargs)
            return leave
        except Exception as e:
            raise e

    def get_all_applications_by_user(self, userid):
        """
        Retrieve all leave applications by a user.
        
        Args:
            userid (str): The ID of the user.
        
        Returns:
            list: A list of leave applications.
        
        Raises:
            ValueError: If the userid is invalid.
            Exception: If there's an error retrieving the applications.
        """
        try:
            if not is_valid_objectid(userid):
                raise ValueError("Application does not exist")
            return self._db.all_by_user(userid=userid)
        except Exception as e:
            raise e

    def delete_leave(self, user, leave_id):
        """
        Delete a leave application.
        
        Args:
            user (object): The user object.
            leave_id (str): The ID of the leave application.
        
        Returns:
            bool: True if the leave application was deleted, False otherwise.
        
        Raises:
            ValueError: If the leave_id is invalid.
        """
        try:
            if not is_valid_objectid(leave_id):
                raise ValueError("Application does not exist")
            if self._db.delete_application(user.email, leave_id=leave_id):
                return True
        except ValueError as e:
            raise e

    def admin_get_all_applications(self):
        """
        Retrieve all leave applications for admin.
        
        Returns:
            list: A list of all leave applications.
        """
        return self._db.all()

    def admin_get_all_user_applications(self, userid):
        """
        Retrieve all leave applications by a specific user for admin.
        
        Args:
            userid (str): The ID of the user.
        
        Returns:
            tuple: A tuple containing user details and leave applications.
        
        Raises:
            ValueError: If the userid is invalid.
        """
        if not is_valid_objectid(userid):
            raise ValueError("Application does not exist")
        user = self._db.find_user_by(id=userid)
        application = (user.lastname, user.firstname, user.email,
                       self.get_all_applications_by_user(userid))
        return application

    def reject_leave_application(self, leave_id):
        """
        Reject a leave application.
        
        Args:
            leave_id (str): The ID of the leave application.
        
        Returns:
            bool: True if the leave application was rejected, False otherwise.
        
        Raises:
            ValueError: If the leave_id is invalid.
        """
        if is_valid_objectid(leave_id):
            return self._db.approve_reject_leave(leave_id, status="rejected")
        raise ValueError("Application does not exist")

    def approve_leave_application(self, leave_id):
        """
        Approve a leave application.
        
        Args:
            leave_id (str): The ID of the leave application.
        
        Returns:
            bool: True if the leave application was approved, False otherwise.
        
        Raises:
            ValueError: If the leave_id is invalid.
        """
        if is_valid_objectid(leave_id):
            return self._db.approve_reject_leave(leave_id, status="approved")
        raise ValueError("Application does not exist")

    def get_stats(self):
        """
        Retrieve leave statistics.
        
        Returns:
            dict: A dictionary of leave statistics.
        """
        return self._db.leave_statistics()

    def get_leave_balance(self, user_id):
        """
        Retrieve remaining leave balance for a user.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            dict: A dictionary containing the leave balance.
        
        Raises:
            ValueError: If there's a ValueError retrieving the balance.
            Exception: If there's an error retrieving the balance.
        """
        try:
            return self._db.leave_balance(user_id)
        except ValueError as e:
            raise ValueError(e)
        except Exception as e:
            raise Exception("Failed to retrieve leave balance: " + str(e))
