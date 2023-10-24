#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################

# Global Values
##############################################################################
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
##############################################################################

##############################################################################
class InstalledApp(EmbeddedDocument):
    name            = StringField()
    version         = StringField()
    installed_by    = StringField()

    def serialize(self):
        data = {
            "username": self.username,
            "version": self.version
        }
        if self.installed_by:
            data["installed_by"] = self.installed_by

        return data

    def __str__(self):
        return str(self.serialize())

class SystemInstalledApps(Document):
    agent     = ReferenceField(Agent)
    apps      = ListField(EmbeddedDocumentField(InstalledApp))
    updated   = DateTimeField(default=datetime.utcnow)
    
    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "apps":self.apps,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################