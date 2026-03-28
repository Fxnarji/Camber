import bpy  # type: ignore

class CamberPropertyGroup(bpy.types.PropertyGroup):
    commit_message: bpy.props.StringProperty(
        name="Commit Message",
        description="the commit message",
    )

    current_version: bpy.props.StringProperty(
        name="Current Version"
    )

    is_tracked: bpy.props.BoolProperty(
    )

    remote_commits: bpy.props.IntProperty(
    )

    admin_mode: bpy.props.BoolProperty(
        default=False
    )

    lock_owner: bpy.props.StringProperty(
    )

    lock_id: bpy.props.StringProperty(
    )
