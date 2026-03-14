import bpy

class CamberPropertyGroup(bpy.types.PropertyGroup):
    commit_message: bpy.props.StringProperty(
        name="Commit Message",
        description="the commit message",
    )#type: ignore