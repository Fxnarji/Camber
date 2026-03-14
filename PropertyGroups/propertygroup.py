import bpy #type: ignore

class CamberPropertyGroup(bpy.types.PropertyGroup):
    commit_message: bpy.props.StringProperty(
        name="Commit Message",
        description="the commit message",
    )#type: ignore

    current_version: bpy.props.StringProperty(
        name="Current Version"
    )#type: ignore

    lock_owner: bpy.props.StringProperty(
    )#type: ignore

    lock_date: bpy.props.StringProperty(
    )#type: ignore

    is_tracked: bpy.props.BoolProperty(
    )#type: ignore

    remote_commits: bpy.props.IntProperty(
    )#type: ignore

    admin_mode: bpy.props.BoolProperty(
        default = False
    )#type: ignore
    