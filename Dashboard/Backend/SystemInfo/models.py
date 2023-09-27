#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document,  ListField, DictField, ReferenceField
)
from Agents.models import Agent
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
##############################################################################