#!/usr/bin/env python3

# Libraries
##############################################################################
import winreg

from .user_info import get_user_info
##############################################################################

# Functions
##############################################################################
def get_installed_programs():
    """
    Retrieve a list of installed programs and their versions from the Windows Registry.
    """
    installed_programs = []

    # Registry paths to search for installed programs
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    try:
        # Machine-wide installed programs
        for reg_path in reg_paths:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]

            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey_path = rf"{reg_path}\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

                try:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    program_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    installed_programs.append({
                        'name': program_name,
                        'version': program_version
                    })
                except WindowsError:
                    continue

                winreg.CloseKey(subkey)

            winreg.CloseKey(reg_key)

        # User-specific installed programs
        users = get_user_info()
        for user in users:
            user_reg_path = rf"HKEY_USERS\{user['sid']}\Software\Microsoft\Windows\CurrentVersion\Uninstall"
            reg_key = winreg.OpenKey(winreg.HKEY_USERS, user_reg_path, 0, winreg.KEY_READ)
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]

            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey_path = rf"{user_reg_path}\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_USERS, subkey_path, 0, winreg.KEY_READ)

                try:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    program_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    installed_programs.append({
                        'name': program_name,
                        'version': program_version
                    })
                except WindowsError:
                    continue

                winreg.CloseKey(subkey)

            winreg.CloseKey(reg_key)
    except WindowsError:
        pass

    return installed_programs
##############################################################################