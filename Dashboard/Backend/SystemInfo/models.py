#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document,  ListField, DictField, ReferenceField,  DateTimeField,
    StringField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################

##############################################################################
class SystemInfo(Document):
    agent               = ReferenceField(Agent)
    os                  = DictField()
    domain              = DictField()
    cpu                 = DictField()
    memory              = DictField()
    disks               = ListField(DictField())
    network_interfaces  = ListField(DictField())

class ChangeLogSystemInfo(Document):
    timestamp = DateTimeField(default=datetime.utcnow)
    changes = DictField()
##############################################################################