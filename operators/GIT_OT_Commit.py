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

        success, message = git.commit(msg, filepath)
        if success:
            self.report({'INFO'}, message)
            camber_data["commit_message"] = ""
            self.refresh_history(context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
