import bpy  # type: ignore
from ..constants import get_operator
from ..msc.api import API
from pathlib import Path
from datetime import datetime


class OBJECT_OT_Lock(bpy.types.Operator):
    bl_idname = get_operator("lock")
    bl_description = "Lock or unlock this file via Git LFS"
    bl_label = "Lock File"
    bl_options = {"REGISTER", "UNDO"}

    lock: bpy.props.BoolProperty(name="Lock", default=True)  # type: ignore

    def execute(self, context):
        filepath = Path(bpy.data.filepath)
        api = API()

        if self.lock:
            response = api.lock(filepath)
            if response is None:
                self.report({'ERROR'}, "Failed to lock file.")
                return {'CANCELLED'}
            owner = response["lock"]["owner"]["name"]
            date = response["lock"]["locked_at"]
            context.scene.camber_data.lock_owner = owner
            context.scene.camber_data.lock_date = format_lock_date(date)
            self.report({'INFO'}, f"File locked by {owner}.")
        else:
            lock_id = api.find_lock_id_by_path(filepath)
            if lock_id is None:
                self.report({'WARNING'}, "No active lock found for this file.")
                return {'CANCELLED'}
            if not api.unlock(lock_id):
                self.report({'ERROR'}, "Failed to unlock file.")
                return {'CANCELLED'}
            context.scene.camber_data.lock_owner = ""
            context.scene.camber_data.lock_date = ""
            self.report({'INFO'}, "File unlocked.")

        return {'FINISHED'}


def format_lock_date(iso_string):
    try:
        dt = datetime.fromisoformat(iso_string)
        now = datetime.now(dt.tzinfo)
        time_str = dt.strftime("%I:%M %p").lstrip('0').lower()
        delta = now.date() - dt.date()

        if delta.days == 0:
            return f"today {time_str}"
        elif delta.days == 1:
            return f"yesterday {time_str}"
        elif delta.days < 7:
            return f"{dt.strftime('%A')} {time_str}"
        else:
            return dt.strftime("%b %d, %Y")
    except Exception:
        return "Unknown date"
