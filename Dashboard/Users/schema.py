#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    name       = fields.Str(required = True)
    lastname   = fields.Str(required = True)
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)

class LoginSchema(Schema):
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)
##############################################################################