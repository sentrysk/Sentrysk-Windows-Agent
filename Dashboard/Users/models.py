#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import Document, StringField, DateTimeField, BinaryField
from datetime import datetime
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

    def __str__(self):
        return str(self.serialize())
##############################################################################
