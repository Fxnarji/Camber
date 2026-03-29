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
