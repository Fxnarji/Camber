import bpy
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Commit(bpy.types.Operator):
    bl_idname = get_operator("commit")
    bl_label = "Commit Changes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        camber_data = context.scene.camber_data
        msg = camber_data.get("commit_message")

        git.commit(msg)

        self.report({'INFO'}, f"Committed: {msg}")

        camber_data["commit_message"] = ""
        bpy.ops.camber.refresh()
        return {'FINISHED'}