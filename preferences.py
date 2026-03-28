import bpy  # type: ignore
from .constants import get_operator


class Sample_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    git_path: bpy.props.StringProperty(
        name="Git Path",
        description="Path to git executable (e.g., git or C:\\Program Files\\Git\\cmd\\git.exe)",
        default="git",
    )

    admin_permissions: bpy.props.BoolProperty(
        name="Admin Mode",
        description="Enable advanced Git operations",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.prop(self, "git_path")
        box.prop(self, "admin_permissions")
