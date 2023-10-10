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

    def serialize(self):
        data = {
            "username": self.username
        }
        if self.user_id:
            data["user_id"] = self.user_id
        if self.group_id:
            data["group_id"] = self.group_id
        if self.home_directory:
            data["home_directory"] = self.home_directory
        if self.shell:
            data["shell"] = self.shell
        if self.full_name:
            data["full_name"] = self.full_name
        if self.comment:
            data["comment"] = self.comment
        if self.last_logon:
            data["last_logon"] = self.last_logon
        if self.flags:
            data["flags"] = self.flags
        if self.sid:
            data["sid"] = self.sid

        return data

    def __str__(self):
        return str(self.serialize())

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