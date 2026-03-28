import bpy
import os
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Checkout(bpy.types.Operator):
    bl_idname = get_operator("checkout")
    bl_label = "Checkout"
    bl_options = {'REGISTER', 'UNDO'}

    hash: bpy.props.StringProperty()

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save the file first.")
            return {'CANCELLED'}

        try:
            git.checkout(self.hash, filepath)
            if os.path.exists(filepath):
                bpy.ops.wm.open_mainfile(filepath=filepath)
            self.report({'INFO'}, f"Checked out: {self.hash}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Checkout failed: {e}")
            return {'CANCELLED'}