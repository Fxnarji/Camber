import bpy # type: ignore
import os
import tempfile
from ..constants import get_operator, get_preferences
from ..msc.api import API

class CAMBER_OT_locked_file_dialog(bpy.types.Operator):
    """Checks file lock and handles the UI intervention if necessary"""
    bl_idname = get_operator("locked_file_dialog")
    bl_label = "File Lock Status"
    bl_options = {'REGISTER', 'INTERNAL'}
        

    def invoke(self, context, event):
        print("invoked!")
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Warning: Locked File", icon='ERROR')
        layout.label(text="You do not have permission to edit this file.")
        layout.separator()
        
        box = layout.box()
        box.label(text="Options:", icon='QUESTION')
        box.label(text="• Click 'OK' to open a temporary view-only copy.")
        box.label(text="• Click 'Cancel' or press Esc to Close Blender.")

    def execute(self, context):
        # User clicked "OK" - Move to temp file
        filename = os.path.basename(bpy.data.filepath)
        temp_filepath = os.path.join(tempfile.gettempdir(), f"LOCKED_COPY_{filename}")
        
        bpy.ops.wm.save_as_mainfile(filepath=temp_filepath)
        bpy.ops.camber.refresh()
        self.report({'INFO'}, "Opened temporary copy.")
        return {'FINISHED'}

    def cancel(self, context):
        """
        This runs if the user clicks 'Cancel', hits Esc, 
        or clicks outside the popup.
        """
        print("User rejected locked file. Closing Blender...")
        bpy.ops.wm.quit_blender()