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
        pass
    
            