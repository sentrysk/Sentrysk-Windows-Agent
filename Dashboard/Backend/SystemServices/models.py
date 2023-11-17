#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField, DateTimeField, ListField,
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
class Service(EmbeddedDocument):
    display_name    = StringField()
    service_name    = StringField()
    status          = StringField()
    description     = StringField()

    def __eq__(self, other):
        return (
            self.display_name == other.display_name and
            self.service_name == other.service_name and
            self.status == other.status and
            self.description == other.description
        )

    def serialize(self):
        data = {
            "display_name": self.display_name,
            "service_name": self.service_name,
            "status": self.status,
            "description": self.description
        }

        return data

    def __str__(self):
        return str(self.serialize())

class SystemServices(Document):
    agent     = ReferenceField(Agent)
    services  = ListField(EmbeddedDocumentField(Service))
    updated   = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "services":self.services,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

##############################################################################