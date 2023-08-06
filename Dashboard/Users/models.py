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
##############################################################################
