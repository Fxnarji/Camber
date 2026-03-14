import bpy  # type: ignore
from ..constants import get_operator, get_preferences
from ..msc.api import API
from pathlib import Path

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
            path = f"{filepath.name}"
            if self.lock:
                response = api.lock(path)
                print(response.get("path"))
                print(response.get("owner"))

            else:
                id = api.find_lock_id_by_path(path)
                print(id)
                api.unlock(id)
            return {'FINISHED'}