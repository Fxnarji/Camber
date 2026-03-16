import bpy  # type: ignore
from ..constants import get_operator, get_preferences
from ..msc.git import Git as git

class GIT_OT_Verify(bpy.types.Operator):
    bl_idname = get_operator("verify")
    bl_label = "Verify"

    mode: bpy.props.StringProperty()#type: ignore

    def execute(self, context):

        self.git = git(bpy.data.filepath)
        self.preferences = get_preferences()

        if self.mode == "repository":
            self.verify_repository(context)
            return {"FINISHED"}
        
        elif self.mode == "git":
            self.verify_git(context)
            return {"FINISHED"}
        
        elif self.mode == "username":
            self.verify_lfs_username(context)

    def verify_lfs_username(self, context):
        pass
    

    def verify_repository(self, context):
        try:
            success, result = self.git.verify_repository()
            self.preferences.repository_link_verified = success
            self.report({'INFO'}, f"Success: {success} {result}")
            return True
        
        except Exception as e:
            self.preferences.repository_link_verified = False
            self.report({'ERROR'}, message = e)
            return False
    
    def verify_git(self, context):
        try:
            success, result = self.git.verify_git_bin()
            self.preferences.git_verified = success
            self.report({'INFO'}, f"Success: {success} {result}")
            return True
        
        except Exception as e:
            self.preferences.git_verified = False
            self.report({'ERROR'}, message = e)
            return False

