import bpy
import os
from ..constants import get_operator
from ..msc.git import Git as git

class GIT_OT_Pull(bpy.types.Operator):
    bl_idname = get_operator("pull")
    bl_label = "Pull Changes" # Fixed label from 'Commit Changes'
    bl_options = {'REGISTER', 'UNDO'}

    fetch_only: bpy.props.BoolProperty(default=False) # type: ignore
    
    def execute(self, context):
        filepath = bpy.data.filepath
        
        if not filepath:
            self.report({'ERROR'}, "Save the file before pulling.")
            return {'CANCELLED'}

        if self.fetch_only:
            success, message = git.fetch(filepath)
            self.report({'INFO' if success else 'ERROR'}, message)
        else:
            # 1. Perform the pull
            success, message = git.pull(filepath)
            
            if not success:
                self.report({'ERROR'}, f"Pull failed: {message}")
                return {'CANCELLED'}

            # 2. Check if the file still exists (it might have been deleted/moved in the pull)
            if os.path.exists(filepath):
                self.report({'INFO'}, "File updated. Re-opening...")
                # Re-open the file to reflect disk changes
                bpy.ops.wm.open_mainfile(filepath=filepath)
            else:
                # 3. Handle deletion
                self.report_deletion(context, filepath)
    
        return {'FINISHED'}

    def report_deletion(self, context, original_path):
        filename = os.path.basename(original_path)
        
        def draw_deletion_msg(self, context):
            self.layout.label(text=f"The file '{filename}' is no longer in the repository.", icon='TRASH')
            self.layout.label(text="It may have been deleted or moved by another user.")
            self.layout.label(text="Current data remains in memory, but you cannot sync to the original path.")

        context.window_manager.popup_menu(draw_deletion_msg, title="File Deleted on Remote", icon='ERROR')