import bpy  # type: ignore
from .constants import get_operator
from .msc.git import Git as git
from .msc.api import API

try: 
    # use sensitive defaults in seperate file in gitignore
    from .defaults import Defaults

except:
    pass



class Sample_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    def validate_github(self, context):
        success, status = git.validate_git_binary()
        self.github_status = status
        print(self.github_status)
        self.valid_github = success


    def verify_repository(self, context):
        api = API()
        success, status  = api.verify_repository()
        self.valid_repository = success
        self.repository_status = status

    def validate_server(self, context):
        api = API()
        success, status = api.verify_server()
        self.valid_server = success
        self.server_status = status

    def validate_credentials(self, context):
        api = API()
        valid_login = api.authenticate_user(self.username)
        if valid_login:
            self.user_status = True
        else:
            self.user_status = False




    # 2. The Server URL Property
    repository_link: bpy.props.StringProperty(
        name="Server URL",
        description="e.g. https://git.mydomain.com/User/Repository",
        default=Defaults.server_url or "",
        update=validate_server
    )#type: ignore


    username: bpy.props.StringProperty(
        name="Username",
        description="e.g. TheLegend27",
        default=Defaults.username or "",
        update=validate_credentials
    )#type: ignore


    repository_name: bpy.props.StringProperty(
        name="Repo Name",
        description="e.g. MyRepository",
        default=Defaults.repo_name or "",
        update=verify_repository
    )#type: ignore


    owner: bpy.props.StringProperty(
        name="Repo Owner",
        description="e.g. TheLegend27",
        default=Defaults.owner or ""
    )#type: ignore


    git_path: bpy.props.StringProperty(
        name="Git Path",
        description="e.g. git",
        subtype='FILE_PATH',
        default = Defaults.git_path or "",
        update = validate_github
    )#type: ignore


    admin_permissions: bpy.props.BoolProperty(
        default = True
    )#type: ignore


    # Validations

    valid_github: bpy.props.BoolProperty(
        default = False
    )#type: ignore

    github_status: bpy.props.StringProperty(
        default = "git not set"
    )#type: ignore

    user_status: bpy.props.BoolProperty(
        default = False
    )#type: ignore

    valid_server: bpy.props.BoolProperty(
        default = False
    )#type: ignore

    server_status: bpy.props.StringProperty(
        default = "Server not set"
    )#type: ignore

    valid_repository: bpy.props.BoolProperty(
        default = False
    )#type: ignore

    repository_status: bpy.props.StringProperty(
        default = "Repository not set"
    )#type: ignore




    def draw(self, context):
        self.success_icon = "KEYTYPE_JITTER_VEC"
        self.failure_icon = "KEYTYPE_EXTREME_VEC"
        layout = self.layout

        self.draw_server(context, layout)
        self.draw_repository(context,layout)
        self.draw_credentials(context,layout)
        self.draw_github(context, layout)
        

    def draw_server(self, context, layout):
        box = layout.box()
        box.prop(self, "server_url")
        if self.valid_server:
            box.label(text =f"Connected to {self.repository_link}, version is: {self.server_status}", icon = self.success_icon)
        else:
            box.label(text = f"Invali API response from: {self.repository_link}, {self.server_status}", icon = self.failure_icon)
        
            

    def draw_repository(self, context, layout):
        box = layout.box()
        column = box.column()
        column.prop(self, "repository_name")
        column.prop(self, "owner")
        row = column.row()
        if self.valid_repository:
            row.label(text = f"{self.repository_status} is valid", icon = self.success_icon)
        else:
            row.label(text = self.repository_status, icon = self.failure_icon)
        row.prop(self, "admin_permissions", toggle= True, text = "Admin", icon = "USER")

        row.operator(get_operator("clone"), icon = "IMPORT")
            

    def draw_credentials(self, context, layout):
        box = layout.box()
        column = box.column()
        column.prop(self, "username")
        column.prop(self, "forgejo_token")
        if self.user_status:
            column.label(text =f"Authenticated as: {self.username}", icon = self.success_icon)
        else:
            column.label(text =f"Authentication failed", icon = self.failure_icon)
            

    def draw_github(self, context, layout):
        box = layout.box()
        column = box.column()
        column.prop(self, "git_path")
        row = column.row()


        if self.valid_github:
            row.label(text = self.github_status, icon = self.success_icon)
        else:
            row.label(text = self.github_status, icon = self.failure_icon)

        