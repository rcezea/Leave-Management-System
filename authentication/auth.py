#!/usr/bin/env python3
"""
auth.py
Authentication module
"""
import uuid
from typing import List
import bcrypt
from models.db import DB
from models.user import User


def _hash_password(password: str) -> bytes:
    """ hash the password """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())


class Auth:
    """ Class providing authentication functionalities """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def authorization_header(self, request=None) -> str:
        """ Retrieve Authorization header """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for a path """
        if path and excluded_paths:
            slash = str(path) + '/'
            if slash in excluded_paths or path in excluded_paths:
                return False
        return True

    def current_user(self, request=None):
        """ Current User """
        if request is not None:
            session_id = request.cookies.get("session_id")
            return self.get_user_from_session_id(session_id)
        return None

    def register_user(self, email, password, firstname, lastname, role=None) -> User:
        """ Register a new user """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError
        return self._db.create_user(email, _hash_password(password), firstname, lastname, role)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate login credentials """
        user = self._db.find_user_by(email=email)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        return False

    def create_session(self, email):
        """ Create a new session """
        session_id = _generate_uuid()
        self._db.update_user(email, session_id=session_id)
        return session_id

    def update_user(self, email, **kwargs):
        """ Update user information """
        if self._db.update_user(email=email, **kwargs):
            return True

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """ Retrieve user based on session ID """
        if session_id:
            return User.objects(session_id=session_id).first()
        return None

    def session_cookie(self, request=None) -> str:
        """ Retrieve session cookie """
        if request:
            return request.cookies.get("session_id")
        return None

    def destroy_session(self, email) -> None:
        """ Destroy user session """
        self._db.update_user(email, session_id=None)
