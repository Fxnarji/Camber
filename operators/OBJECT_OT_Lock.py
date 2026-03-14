import bpy  # type: ignore
from ..constants import get_operator, get_preferences
from ..msc.api import API
from pathlib import Path
from datetime import datetime
# Define the operator to snap FK bones to IK bones
class OBJECT_OT_Lock(bpy.types.Operator):
    bl_idname = get_operator("lock")
    bl_description = "Renames selected Object to Hello World"
    bl_label = "Test"
    bl_options = {"REGISTER", "UNDO"}

    # 2. The Server URL Property
    lock: bpy.props.BoolProperty(name="lock", default= False) #type: ignore

    def execute(self, context):

            filepath = Path(bpy.data.filepath)

            api = API()
            if self.lock:
                response = api.lock(filepath)
                owner = response["lock"]["owner"]["name"]
                date = response["lock"]["locked_at"]
                print(response)

                context.scene.camber_data["lock_owner"] = owner
                context.scene.camber_data["lock_date"] = format_lock_date(date)

            else:
                id = api.find_lock_id_by_path(filepath)
                print(id)
                api.unlock(id)
            return {'FINISHED'}
    

def format_lock_date(iso_string):
    try:
        # 1. Parse the ISO string into a datetime object
        dt = datetime.fromisoformat(iso_string)
        now = datetime.now(dt.tzinfo) # Ensure we use the same timezone for comparison
        
        # 2. Extract the time in a 12-hour format (e.g., 3:58 AM)
        time_str = dt.strftime("%I:%M %p").lstrip('0').lower()
        
        # 3. Calculate the day difference
        delta = now.date() - dt.date()
        
        if delta.days == 0:
            return f"today {time_str}"
        elif delta.days == 1:
            return f"yesterday {time_str}"
        elif delta.days < 7:
            return f"{dt.strftime('%A')} {time_str}" # e.g., Monday 3:58 am
        else:
            return dt.strftime("%b %d, %Y") # e.g., Mar 14, 2026
            
    except Exception as e:
        return "Unknown date"