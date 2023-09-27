#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    os                  = fields.Raw()
    domain              = fields.Raw()
    cpu                 = fields.Raw()
    memory              = fields.Raw()
    disks               = fields.Raw()
    network_interfaces  = fields.Raw()
##############################################################################