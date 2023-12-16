#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
from enum import Enum,unique
##############################################################################

# Enums
##############################################################################
@unique
class AgentTypeEnum(str,Enum):
    windows   : str = "windows"
    linux     : str = "linux"
    macos     : str = "macos"
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    type = fields.Str(
        required=True, 
        validate = validate.OneOf([val for val in AgentTypeEnum])
    )
##############################################################################