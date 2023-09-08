#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)
##############################################################################