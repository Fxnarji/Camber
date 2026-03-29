from ..msc.api import API
from ..constants import get_preferences

import bpy  # type: ignore


class Handler():

    @staticmethod
    def refresh_list():
        if bpy.data.filepath:
            try:
                bpy.ops.camber.refresh()
            except Exception as e:
                print(f"Could not refresh git: {e}")

    @staticmethod
    def verify_and_cache_credentials():
        prefs = get_preferences()
        if not prefs:
            print("Could not get preferences for verification")
            return False

        api = API()

        if not api.verify_credentials():
            print("Credential verification failed")
            prefs.verified_username = ""
            return False

        verified_name = api.get_verified_username()
        if verified_name:
            prefs.verified_username = verified_name
            print(f"Verified username: {verified_name}")
        else:
            prefs.verified_username = prefs.username
            print(f"Using configured username: {prefs.username}")

        return True

    @staticmethod
    def refresh_lock_status():
        """Check the LFS lock status for the open file and store it in scene
        properties for the panel to display. Called once via timer on file open."""
        filepath = bpy.data.filepath
        if not filepath:
            return None

        try:
            from ..operators.OBJECT_OT_Lock import format_lock_date
            api = API()
            lock = api.is_file_locked(filepath)
            scene = bpy.context.scene

            if lock:
                scene.camber_data.lock_owner = lock["owner"]["name"]
                scene.camber_data.lock_date = format_lock_date(lock.get("locked_at", ""))
            else:
                scene.camber_data.lock_owner = ""
                scene.camber_data.lock_date = ""
        except Exception as e:
            print(f"Could not refresh lock status: {e}")

        return None  # Don't repeat the timer
