#!/usr/bin/env python3

# Libraries
##############################################################################
from configparser import ConfigParser
##############################################################################

# Config
##############################################################################
CONFIG_FILE = 'config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

# App
SECRET_KEY  = config.get('Flask','SECRET_KEY')
APP_HOST    = config.get('Flask','HOST')
APP_PORT    = int(config.get('Flask','PORT'))

# JWT Algorithm
JWT_ALG = config.get('JWT','JWT_ALG') 

# DB
DB_HOST      = config.get('Database','HOST')
DB_NAME      = config.get('Database','DB')
DB_USERNAME  = config.get('Database','USERNAME')
DB_PASSWORD  = config.get('Database','PASSWORD')
#############################################################################


print("SECRET_KEY:"+SECRET_KEY+str(type(SECRET_KEY)))
print("APP_HOST:"+APP_HOST+str(type(APP_HOST)))
print("APP_PORT:"+str(APP_PORT)+str(type(APP_PORT)))

print("\nJWT_ALG:"+JWT_ALG+str(type(JWT_ALG)))

print("\nDB_HOST"+DB_HOST+str(type(DB_HOST)))
print("DB_NAME:"+DB_NAME+str(type(DB_NAME)))
print("DB_USERNAME"+DB_USERNAME+str(type(DB_USERNAME)))
print("DB_PASSWORD"+DB_PASSWORD+str(type(DB_PASSWORD)))