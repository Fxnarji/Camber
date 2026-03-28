import bpy
import os
from ..constants import get_operator
from ..msc.git import Git as git
from .GIT_OT_RefreshHistory import GIT_OT_RefreshHistory

class GIT_OT_Pull(bpy.types.Operator):
    bl_idname = get_operator("pull")
    bl_label = "Pull Changes"
    bl_options = {'REGISTER', 'UNDO'}

    fetch_only: bpy.props.BoolProperty(default=False)
    
    def execute(self, context):
        filepath = bpy.data.filepath
        
        if not filepath:
            self.report({'ERROR'}, "Save the file before pulling.")
            return {'CANCELLED'}

        if self.fetch_only:
            success, message = git.fetch(filepath)
            self.report({'INFO' if success else 'ERROR'}, message)
            if success:
                GIT_OT_RefreshHistory.refresh_history(context)
        else:
            success, message = git.pull(filepath)
            
            if not success:
                self.report({'ERROR'}, f"Pull failed: {message}")
                return {'CANCELLED'}

            if os.path.exists(filepath):
                self.report({'INFO'}, "File updated. Re-opening...")
                bpy.ops.wm.open_mainfile(filepath=filepath)
            else:
                self.report_deletion(context, filepath)
            
            GIT_OT_RefreshHistory.refresh_history(context)
            self.update_lock_status(context)
        
        return {'FINISHED'}

    def update_lock_status(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            return
        
        lock = git.lfs_get_lock(filepath)
        camber_data = context.scene.camber_data
        if lock:
            camber_data.lock_owner = lock.get("owner", "")
            camber_data.lock_id = str(lock.get("id", ""))
        else:
            camber_data.lock_owner = ""
            camber_data.lock_id = ""

    def report_deletion(self, context, original_path):
        filename = os.path.basename(original_path)
        
        def draw_deletion_msg(self, context):
            self.layout.label(text=f"The file '{filename}' is no longer in the repository.", icon='TRASH')
            self.layout.label(text="It may have been deleted or moved by another user.")
            self.layout.label(text="Current data remains in memory, but you cannot sync to the original path.")

        context.window_manager.popup_menu(draw_deletion_msg, title="File Deleted on Remote", icon='ERROR')