import bpy  # type: ignore
from .constants import get_operator

try:
    from .defaults import defaults as user_defaults
except ImportError:
    user_defaults = None


def get_default(key, fallback):
    if user_defaults and key in user_defaults:
        return user_defaults[key]
    return fallback


class Sample_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

<<<<<<< Updated upstream
    git_path: bpy.props.StringProperty(
        name="Git Path",
        description="Path to git executable (e.g., git or C:\\Program Files\\Git\\cmd\\git.exe)",
        default="git",
=======
    personal_access_token: bpy.props.StringProperty(
        name="LFS Personal Access Token",
        description="Your Personal Access Token for Git LFS server",
        default="",
        subtype='PASSWORD'
    )

    server_url: bpy.props.StringProperty(
        name="Server URL",
        description="e.g. https://git.example.com",
        default=get_default("server_url", "https://git.example.com"),
    )

    username: bpy.props.StringProperty(
        name="Username",
        description="Your username on the Git LFS server",
        default=get_default("username", "username"),
    )

    repository_name: bpy.props.StringProperty(
        name="Repository Name",
        description="e.g. MyRepository",
        default=get_default("repository_name", "my-repo"),
    )

    owner: bpy.props.StringProperty(
        name="Repository Owner",
        description="Owner of the repository (user or organization)",
        default=get_default("owner", "owner"),
    )

    git_path: bpy.props.StringProperty(
        name="Git Path",
        description="Path to git executable",
        default=get_default("git_path", "git"),
>>>>>>> Stashed changes
    )

    admin_permissions: bpy.props.BoolProperty(
        name="Admin Mode",
<<<<<<< Updated upstream
        description="Enable advanced Git operations",
        default=True,
=======
        description="Enable advanced features",
        default=False
    )

    verified_username: bpy.props.StringProperty(
        name="Verified Username",
        description="Cached username from server verification",
        default=""
>>>>>>> Stashed changes
    )

    def draw(self, context):
        layout = self.layout
<<<<<<< Updated upstream
        
        box = layout.box()
        box.prop(self, "git_path")
        box.prop(self, "admin_permissions")
=======
        layout.label(text="Git LFS API Configuration")
        
        box = layout.box()
        column = box.column()
        column.prop(self, "server_url")
        column.prop(self, "repository_name")
        column.prop(self, "owner")

        box = layout.box()
        column = box.column()
        column.prop(self, "username")
        column.prop(self, "personal_access_token")

        box = layout.box()
        column = box.column()
        column.prop(self, "git_path")
        column.prop(self, "admin_permissions")
        
>>>>>>> Stashed changes
