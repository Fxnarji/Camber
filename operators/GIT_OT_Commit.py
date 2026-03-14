import bpy
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Commit(bpy.types.Operator):
    bl_idname = get_operator("commit")
    bl_label = "Commit Changes"
    bl_options = {'REGISTER', 'UNDO'}

    message: bpy.props.StringProperty(
        name="Commit Message",
        description="Briefly describe what you changed",
        default=""
    )#type: ignore

    def invoke(self, context, event):
            self.message = ""
            # Increase width to 400 pixels for easier typing
            return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        if not self.message.strip():
            self.report({'ERROR'}, "Commit message cannot be empty!")
            return {'CANCELLED'}

        git.commit(self.message)
        
        
        self.report({'INFO'}, f"Committed: {self.message}")
        return {'FINISHED'}

    # Optional: Customize the look of the popup
    def draw(self, context):
        layout = self.layout
        layout.label(text="Enter your work summary:")
        layout.prop(self, "message")