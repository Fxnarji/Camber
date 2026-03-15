from ..msc.api import API
from ..msc.git import Git
from ..constants import get_preferences
import os
import subprocess
import sys
import signal

import bpy #type: ignore

class Handler():

    @staticmethod
    def refresh_list():
        if bpy.data.filepath:
            try:
                bpy.ops.camber.refresh()
            except Exception as e:
                print(f"Could not refresh git: {e}")

    @staticmethod
    def lock_file(lock = True):
        if bpy.data.filepath:
            try:
                bpy.ops.camber.lock(lock = lock)
            except Exception as e:
                print(f"Could not Lock File: {e}")


    @staticmethod
    def is_file_locked(filepath) -> None|bool:
        """
        This runs slightly after the file opens via a timer.
        It allows us to safely use UI operators and popups.
        """
        if not filepath:
            return None
        
        if not Git.file_in_repo(filepath):
            return None
        
        api = API()
        lock = api.is_file_locked(filepath)
        
        if lock is not None:
            lock_owner = lock["owner"]["name"]
            user = get_preferences().username
            is_user_verified = api.authenticate_user(user)
        
            if lock_owner == user and is_user_verified:
                return False
            else:
                return True
        
        return None
            