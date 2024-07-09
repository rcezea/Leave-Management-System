#!/usr/bin/env python3
"""
user.py
Defining the User Document and Leave Document
"""
import mongoengine


class User(mongoengine.Document):
    """ User document definition """
    role = mongoengine.StringField(required=True, choices=['admin', 'employee'], default='employee')
    firstname = mongoengine.StringField(required=True)
    lastname = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    applications = mongoengine.ListField(mongoengine.ReferenceField('Leave'))
    session_id = mongoengine.StringField(required=False)

    def add_applications(self, leave):
        """ Add leave application """
        self.update(push__applications=leave)

    meta = {
        'db_alias': 'core',
        'collection': 'user'
    }


class Leave(mongoengine.Document):
    """ Leave document definition """

    userid = mongoengine.ObjectIdField(required=True)
    start = mongoengine.DateField(required=True)  # default date.today()
    end = mongoengine.DateField(required=True)
    type = mongoengine.StringField(required=True)
    reason = mongoengine.StringField(required=True)
    status = mongoengine.BooleanField(required=True, default=False)

    meta = {
        'db_alias': 'core',
        'collection': 'leave'
    }
