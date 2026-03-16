import bpy  # type: ignore
from .msc.session import get_session
from .operators.GIT_OT_Verify import GIT_OT_Verify
from .operators.GIT_OT_Clone import GIT_OT_Clone
try: 
    # use sensitive defaults in seperate file in gitignore
    from .defaults import Defaults

except:
    pass



class CamberPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    session = get_session()

    def update_repository(self, context):
        self.session.repository_url = self.repository_link

    def update_git(self, context):
        self.session.git_bin = self.git_bin


    # 2. The Server URL Property
    repository_link: bpy.props.StringProperty(
        name="Repository Link",
        description="e.g. https://git.mydomain.com/User/Repository",
        default=Defaults.server_url or "", #type: ignore
        update=update_repository
    )#type: ignore

    repository_link_verified: bpy.props.BoolProperty(default = False)#type: ignore

    # 2. The Server URL Property
    git_bin: bpy.props.StringProperty(
        name="Git Path",
        description="e.g. C:\\Program Files\\Git\\bin\\git.exe",
        default=Defaults.git_path or "", #type: ignore
        subtype = 'FILE_PATH',
        update=update_git
    )#type: ignore

    git_verified: bpy.props.BoolProperty(default = False)#type: ignore


    def draw(self, context):
        self.success_icon = "FAKE_USER_ON"
        self.failure_icon = "FAKE_USER_OFF"
        layout = self.layout

        self.draw_repository(context, layout)
        self.draw_git_bin(context, layout)


    def draw_git_bin(self, context, layout):
        box = layout.box()
        row = box.row()
        row.prop(self, "git_bin")
        if self.git_verified:
            row.operator(GIT_OT_Verify.bl_idname, text = "", icon = self.success_icon).mode = "git"
        else:
            row.operator(GIT_OT_Verify.bl_idname, text = "", icon = self.failure_icon).mode = "git"

    def draw_repository(self, context, layout):
        box = layout.box()
        row = box.row()
        combined_row = row.row(align = True)
        combined_row.prop(self, "repository_link")
        combined_row.operator(GIT_OT_Clone.bl_idname, text = "", icon = "IMPORT")
        if self.repository_link_verified:
            row.operator(GIT_OT_Verify.bl_idname, text = "", icon = self.success_icon).mode = "repository"
        else:
            row.operator(GIT_OT_Verify.bl_idname, text = "", icon = self.failure_icon).mode = "repository"
        
        
            
