import bpy  #type: ignore
from ..constants import get_operator
from ..msc.git import Git

class GIT_OT_Clone(bpy.types.Operator):
    bl_idname = get_operator("clone")
    bl_label = "Clone"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(subtype='DIR_PATH') #type: ignore

    def execute(self, context):
        git = Git(bpy.data.filepath)
        git.clone(self.directory)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}