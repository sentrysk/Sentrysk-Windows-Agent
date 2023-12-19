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
class LogonData(EmbeddedDocument):
    username        = StringField()
    last_logon      = DateTimeField()
##############################################################################

##############################################################################
class SystemLastLogons(Document):
    agent               = ReferenceField(Agent)
    last_logons         = ListField(EmbeddedDocumentField(LogonData))
    updated             = DateTimeField(default=datetime.utcnow)
##############################################################################