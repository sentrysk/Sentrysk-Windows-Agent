#!/usr/bin/env python3

# Libraries
##############################################################################
from Modules.Register import *
from Modules.Login import *
##############################################################################

# Register Tests
##############################################################################
# Invalid Name Test
if test_register_invalid_name():
    print("[SUCCESS]\t[test_register_invalid_name]")
else:
    print("[FAIL]\t[test_register_invalid_name]")

# Invalid Lastname Test
if test_register_invalid_lastname():
    print("[SUCCESS]\t[test_register_invalid_lastname]")
else:
    print("[FAIL]\t[test_register_invalid_lastname]")

# Email Test
if test_register_invalid_email():
    print("[SUCCESS]\t[test_register_invalid_email]")
else:
    print("[FAIL]\t[test_register_invalid_email]")

# Successfuly Register Test
USER_DATA = test_register_success()
if USER_DATA:
    print("[SUCCESS]\t[test_register_success]")
else:
    print("[FAIL]\t[test_register_success]")
##############################################################################

# Login Tests
##############################################################################
# Invalid Name Test
if test_login_success(USER_DATA):
    print("[SUCCESS]\t[test_login_success]")
else:
    print("[FAIL]\t[test_login_success]")

if test_login_invalid_email():
    print("[SUCCESS]\t[test_login_invalid_email]")
else:
    print("[FAIL]\t[test_login_invalid_email]")
##############################################################################