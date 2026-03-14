import bpy
from ..constants import get_operator
from ..msc.git import Git as git
from pathlib import Path

class GIT_OT_RefreshHistory(bpy.types.Operator):
    bl_idname = get_operator("refresh")
    bl_label = "Refresh Git History"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        history_data = git.get_git_history(bpy.data.filepath)
        
        # 3. Access the collection and clear it
        scene = context.scene
        scene.git_history.clear()
        # 4. Populate the collection
        for entry in history_data:
            item = scene.git_history.add()
            item.name = entry['message']
            item.hash = entry['hash']
            item.date = entry['date']
            item.author = entry['author']
            
        return {'FINISHED'}