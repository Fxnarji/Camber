import bpy
from ..constants import get_operator
from ..msc.git import Git as git
from pathlib import Path

class GIT_OT_RefreshHistory(bpy.types.Operator):
    bl_idname = get_operator("refresh")
    bl_label = "Refresh Git History"
    bl_options = {'REGISTER', 'UNDO'}

    detailed: bpy.props.BoolProperty(default = False)#type: ignore

    def execute(self, context):
            scene = context.scene
            
            try:
                current_version = git.get_current_commit_hash(bpy.data.filepath)
                if self.detailed:
                    history_data = git.get_detailed_git_history(bpy.data.filepath)
                    print(history_data)
                else:
                    history_data = git.get_git_history(bpy.data.filepath)
                git.fetch(bpy.data.filepath)

            except Exception as e:

                print("not a git file, not loading history", e)
                scene.git_history.clear()
                scene.camber_data.is_tracked = False
                return{'FINISHED'}

            scene.camber_data.is_tracked = True
            scene.git_history.clear()
            scene.camber_data.current_version = current_version

            for entry in history_data:
                item = scene.git_history.add()
                item.name = entry['message']
                item.hash = entry['hash']
                item.date = entry['date']
                item.author = entry['author']
            
                item.size = entry.get("size") or ""

            return {'FINISHED'}