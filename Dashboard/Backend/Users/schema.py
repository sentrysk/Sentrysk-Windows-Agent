#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
##############################################################################

# Regexs
##############################################################################
ALPH_NUM_REGX = r"^[a-zA-Z]{1,25}(?: [a-zA-Z]{1,25})?$"
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    name       = fields.Str(required = True,validate=validate.Regexp(ALPH_NUM_REGX))
    lastname   = fields.Str(required = True)
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)

class LoginSchema(Schema):
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)
##############################################################################