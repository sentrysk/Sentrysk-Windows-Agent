#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField,  DateTimeField,  ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################

##############################################################################
class UserData(EmbeddedDocument):
    username        = StringField()
    user_id         = StringField()
    group_id        = StringField()
    home_directory  = StringField()
    shell           = StringField()
    full_name       = StringField()
    comment         = StringField()
    last_logon      = DateTimeField()
    flags           = ListField()
    sid             = StringField()

class SystemUsers(Document):
    agent               = ReferenceField(Agent)
    users               = ListField(EmbeddedDocumentField(UserData))
    updated             = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "users":self.users,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogSystemUsers(Document):
    sys_users       = ReferenceField(SystemUsers)
    timestamp       = DateTimeField(default=datetime.utcnow)
    changes         = DictField()

    def serialize(self):
        return {
            "id":str(self.id),
            "timestamp":self.timestamp,
            "changes":self.changes
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################