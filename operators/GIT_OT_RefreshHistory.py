import bpy #type: ignore
from ..constants import get_operator
from ..msc.git import Git
from pathlib import Path

class GIT_OT_RefreshHistory(bpy.types.Operator):
    bl_idname = get_operator("refresh")
    bl_label = "Refresh Git History"
    bl_options = {'REGISTER', 'UNDO'}

    detailed: bpy.props.BoolProperty(default = False)#type: ignore

    def execute(self, context):
            scene = context.scene
            self.git = Git(bpy.data.filepath)

            try:
                success, current_version = self.git.get_current_commit()
                success, history_data = self.git.get_detailed_git_history()
                self.git.fetch()

            except Exception as e:

                print("not a git file, not loading history", e)
                scene.git_history.clear()
                scene.camber_data.is_tracked = False
                return{'FINISHED'}

            scene.camber_data.is_tracked = True
            scene.git_history.clear()
            scene.camber_data.current_version = current_version

            print(history_data)
            return {'FINISHED'}

            for entry in history_data:
                item = scene.git_history.add()
                item.name = entry['message']
                item.hash = entry['hash']
                item.date = entry['date']
                item.author = entry['author']
            
                item.size = entry.get("size") or ""

            return {'FINISHED'}