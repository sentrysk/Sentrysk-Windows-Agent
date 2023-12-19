#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Schemas
##############################################################################
class LastLogonSchema(Schema):
    last_logons = fields.List(
        fields.Dict(
            username    = fields.Str(),
            last_logon  = fields.DateTime()
        )
    )
##############################################################################