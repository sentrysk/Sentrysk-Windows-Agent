#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, StringField, DateTimeField, BinaryField, BooleanField
)
from datetime import datetime, timedelta
##############################################################################

# Configs
##############################################################################

##############################################################################


# Models
##############################################################################
class User(Document):
    email     = StringField(required=True, unique=True)
    password  = BinaryField(required=True)
    created   = DateTimeField(default=datetime.now)

    def serialize(self):
        return {
            "id":str(self.id),
            "email":self.type,
            "password":self.token,
            "created":self.created
        }
    
    def safe_serialize(self):
        return {
            "id":str(self.id),
            "email":self.type,
            "created":self.created
        }

    def __str__(self):
        return str(self.serialize())

class Session(Document):
    email         = StringField(required=True)
    token         = StringField(required=True, unique=True)
    expire_date   = DateTimeField(default=datetime.now + timedelta(hours=24))
    is_expired    = BooleanField(required=True, default=False)
    created       = DateTimeField(default=datetime.now)
##############################################################################
