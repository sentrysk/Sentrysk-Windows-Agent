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

    # To compare 2 App Data
    def compare_servies(self, other):
        if not isinstance(other, SystemServices):
            raise ValueError("Comparison should be done with another SystemInstalledApps instance")

        self_apps = {app.name: app for app in self.apps}
        other_apps = {app.name: app for app in other.apps}

        # Newly Added Apps
        new_apps = [app.serialize() for name, app in other_apps.items() if name not in self_apps]
        # Deleted Apps
        deleted_apps = [app.serialize() for name, app in self_apps.items() if name not in other_apps]
        # Updated Apps and Fields
        updated_apps = {}

        # Find the Updated Fields
        for appname in self_apps:
            if appname in other_apps and self_apps[appname] != other_apps[appname]:
                updated_fields = {}
                for field in InstalledApp._fields:
                    if str(self_apps[appname][field]) != str(other_apps[appname][field]):
                        updated_fields[field] = {
                            "previous_value":self_apps[appname][field],
                            "new_value":other_apps[appname][field]
                        }
                # Add Updated Fields to Updated apps Dict
                updated_apps[appname] = updated_fields

        # Return Compared Data
        return new_apps, deleted_apps, updated_apps
    
    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "services":self.services,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogSystemServices(Document):
    services   = ReferenceField(SystemServices)
    timestamp  = DateTimeField(default=datetime.utcnow)
    changes    = DictField()

    def serialize(self):
        return {
            "id":str(self.id),
            "timestamp":self.timestamp,
            "changes":self.changes
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################