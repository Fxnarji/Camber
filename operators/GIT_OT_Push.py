import bpy
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Push(bpy.types.Operator):
    bl_idname = get_operator("push")
    bl_label = "Push"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save the file first.")
            return {'CANCELLED'}

        success, message = git.push(filepath)
        self.report({'INFO' if success else 'ERROR'}, message)
        return {'FINISHED' if success else 'CANCELLED'}
