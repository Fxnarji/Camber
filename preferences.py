import bpy  # type: ignore
from .constants import get_operator


class Sample_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

# 1. The Token Property
    forgejo_token: bpy.props.StringProperty(
        name="Forgejo Token",
        description="Your Personal Access Token from Forgejo",
        default="",
        subtype='PASSWORD' # Hides the text in the UI
    )

    # 2. The Server URL Property
    server_url: bpy.props.StringProperty(
        name="Server URL",
        description="e.g. https://git.mydomain.com",
        default="https://git.fynnluft.com",
    )

    username: bpy.props.StringProperty(
        name="Username",
        description="e.g. TheLegend27",
        default="Fxnarji",
    )

    repository_name: bpy.props.StringProperty(
        name="Repo Name",
        description="e.g. MyRepository",
        default="Camber",
    )

    owner: bpy.props.StringProperty(
        name="Repo Owner",
        description="e.g. TheLegend27",
        default="Fxnarji",
    )

    git_path: bpy.props.StringProperty(
        name="Git Path",
        description="e.g. git",
        default="Camber",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Forgejo API Configuration")
        
        box = layout.box()
        column = box.column()
        column.prop(self, "server_url")
        column.prop(self, "repository_name")
        column.prop(self, "owner")

        
        box = layout.box()
        column = box.column()
        column.prop(self, "username")
        column.prop(self, "forgejo_token")

        box = layout.box()
        column = box.column()
        column.prop(self, "git_path")