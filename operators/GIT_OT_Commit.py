import bpy
from ..constants import get_operator
from ..msc.git import Git as git
from .GIT_OT_RefreshHistory import GIT_OT_RefreshHistory

class GIT_OT_Commit(bpy.types.Operator):
    bl_idname = get_operator("commit")
    bl_label = "Commit"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.camber_data.get("commit_message") != ""

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save the file first.")
            return {'CANCELLED'}

        camber_data = context.scene.camber_data
        msg = camber_data.get("commit_message")

<<<<<<< Updated upstream
        success, message = git.commit(msg, filepath)
        if success:
            self.report({'INFO'}, message)
            camber_data["commit_message"] = ""
            GIT_OT_RefreshHistory.refresh_history(context=context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
=======
        result = git.commit(msg, bpy.data.filepath)

        if isinstance(result, tuple) and not result[0]:
            self.report({'ERROR'}, f"Commit failed: {result[1]}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Committed: {msg}")

        camber_data["commit_message"] = ""
        bpy.ops.camber.lock()
        bpy.ops.camber.refresh()
        return {'FINISHED'}
>>>>>>> Stashed changes
