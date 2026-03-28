import bpy  # type: ignore
from ..constants import get_operator
from ..msc.git import Git

class GIT_OT_Unlock(bpy.types.Operator):
    bl_idname = get_operator("unlock")
    bl_label = "Unlock"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save the file first.")
            return {'CANCELLED'}

        lock = Git.lfs_get_lock(filepath)
        if not lock:
            self.report({'INFO'}, "File is not locked")
            return {'FINISHED'}

        current_user = Git.get_current_user()
        if lock.get("owner") != current_user.get("name"):
            self.report({'ERROR'}, "You do not own this lock")
            return {'CANCELLED'}

        success, message = Git.lfs_unlock(lock["id"])
        if success:
            camber_data = context.scene.camber_data
            camber_data.lock_owner = ""
            camber_data.lock_id = ""
            self.report({'INFO'}, message)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

    @classmethod
    def poll(cls, context):
        if not bpy.data.filepath:
            return False
        camber_data = context.scene.camber_data
        if not camber_data.lock_owner:
            return False
        current_user = Git.get_current_user()
        return camber_data.lock_owner == current_user.get("name")
