from ..msc.api import API
from ..msc.git import Git
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
    def spawn_sentinel(file_path):
        api = API() # Get current API (using Blender prefs)
        sec = api.sec
        
        watcher_script = os.path.join(os.path.dirname(__file__), "watcher.py")
        print(watcher_script)
        addon_dir = os.path.dirname(os.path.dirname(__file__)) 

        args = [
            sys.executable, watcher_script,
            str(os.getpid()),
            file_path,
            sec.root,
            sec.owner,
            sec.repo,
            sec.username,
            sec.token,
            addon_dir
        ]

        process = subprocess.Popen(
            args,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            start_new_session=True 
        )
        pid_file = os.path.join(bpy.app.tempdir, "camber_sentinel.pid")
        print(pid_file)
        with open(pid_file, "w") as f:
            f.write(str(process.pid))


