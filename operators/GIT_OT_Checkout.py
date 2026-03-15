import bpy  #type: ignore
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Checkout(bpy.types.Operator):
    bl_idname = get_operator("checkout")
    bl_label = "checkout"
    bl_options = {'REGISTER', 'UNDO'}

    hash: bpy.props.StringProperty() #type: ignore

    

    def execute(self, context):
        git.checkout(self.hash, bpy.data.filepath)
        bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath, load_ui = False)
        bpy.ops.camber.refresh()
        return {'FINISHED'}