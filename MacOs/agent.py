#!/usr/bin/env python3

# Libraries
##############################################################################
import json
from configparser import ConfigParser,ExtendedInterpolation
import logging

##############################################################################

# Configs
##############################################################################
CONFIG_FILE = 'config.ini'

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(CONFIG_FILE)

DASHBOARD_URL   = config.get('dashboard','url')
LOGFILE         = config.get('logging','logfile')


FORMAT = '%(asctime)s :: %(levelname)-6s :: %(name)s :: [%(filename)s:%(lineno)s - %(funcName)s()] :: %(message)s'
# Configure logging to write logs to a log file
logging.basicConfig(
    filename=LOGFILE, 
    level=logging.INFO,
    format=FORMAT,
    encoding='utf-8'
)
##############################################################################

# Functions
##############################################################################
"""
    Retrieve system information.
"""

system_info = {}
##############################################################################