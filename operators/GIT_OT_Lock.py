import bpy  # type: ignore
from ..constants import get_operator
from ..msc.git import Git

class GIT_OT_Lock(bpy.types.Operator):
    bl_idname = get_operator("lock")
    bl_label = "Lock"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save the file first.")
            return {'CANCELLED'}

        lock = Git.lfs_get_lock(filepath)
        if lock:
            self.report({'INFO'}, "File is already locked")
            return {'FINISHED'}

        success, message = Git.lfs_lock(filepath)
        if success:
            camber_data = context.scene.camber_data
            camber_data.lock_owner = Git.get_current_user().get("name", "You")
            lock = Git.lfs_get_lock(filepath)
            if lock:
                camber_data.lock_id = str(lock.get("id", ""))
            self.report({'INFO'}, message)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

    @classmethod
    def poll(cls, context):
        if not bpy.data.filepath:
            return False
        lock = Git.lfs_get_lock(bpy.data.filepath)
        return lock is None
