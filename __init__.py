import bpy  # type: ignore
<<<<<<< Updated upstream
from bpy.app.handlers import persistent
=======
from bpy.app.handlers import persistent #type: ignore
from .msc.handler_actions import Handler

# preferences
>>>>>>> Stashed changes
from .preferences import Sample_Preferences
from .msc.list import GitListItem, GitUIList
from .operators.GIT_OT_Lock import GIT_OT_Lock
from .operators.GIT_OT_Unlock import GIT_OT_Unlock
from .operators.GIT_OT_Commit import GIT_OT_Commit
from .operators.GIT_OT_Push import GIT_OT_Push
from .operators.GIT_OT_Pull import GIT_OT_Pull
from .operators.GIT_OT_RefreshHistory import GIT_OT_RefreshHistory
from .operators.GIT_OT_Checkout import GIT_OT_Checkout
<<<<<<< Updated upstream
=======

# property groups
>>>>>>> Stashed changes
from .PropertyGroups.propertygroup import CamberPropertyGroup
from .panels.VIEW3D_PT_UI_Sample import VIEW3D_PT_UI_Sample
from .msc.git import Git


def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()
<<<<<<< Updated upstream
    extension_name = manifest["name"]
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))
=======

    extension_name = manifest["name"]

    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

>>>>>>> Stashed changes
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

    return {
        "name": extension_name,
        "version": version_tuple,
        "blender": blender_version_tuple,
    }

<<<<<<< Updated upstream

def update_lock_status():
    """Check and cache the current file's lock status."""
    filepath = bpy.data.filepath
    scene = bpy.context.scene
    
    if not filepath or not scene.camber_data.is_tracked:
        scene.camber_data.lock_owner = ""
        scene.camber_data.lock_id = ""
        return

    lock = Git.lfs_get_lock(filepath)
    if lock:
        scene.camber_data.lock_owner = lock.get("owner", "")
        scene.camber_data.lock_id = str(lock.get("id", ""))
    else:
        scene.camber_data.lock_owner = ""
        scene.camber_data.lock_id = ""

=======
>>>>>>> Stashed changes

blender_manifest = load_manifest_info()
bl_info = {
    "name": blender_manifest["name"],
    "description": "Git LFS integration for Blender",
    "author": "Your Name",
    "version": blender_manifest["version"],
    "blender": blender_manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
    Sample_Preferences,
    GitListItem,
    GitUIList,
<<<<<<< Updated upstream
    GIT_OT_Lock,
    GIT_OT_Unlock,
=======

    # operators:
    OBJECT_OT_Lock,
    DUMMY_OT_DummyOperator,
>>>>>>> Stashed changes
    GIT_OT_Commit,
    GIT_OT_Push,
    GIT_OT_RefreshHistory,
    GIT_OT_Checkout,
    GIT_OT_Pull,
<<<<<<< Updated upstream
=======

    # Property Groups:
>>>>>>> Stashed changes
    CamberPropertyGroup,
    VIEW3D_PT_UI_Sample,
]

<<<<<<< Updated upstream

@persistent
def on_file_open(dummy):
    update_lock_status()


@persistent
def on_file_save(dummy):
    update_lock_status()
=======
@persistent
def on_open_handler(dummy):
    Handler.verify_and_cache_credentials()
    Handler.refresh_list()
    bpy.app.timers.register(Handler.refresh_lock_status, first_interval=0.5)
>>>>>>> Stashed changes


def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.camber_data = bpy.props.PointerProperty(type=CamberPropertyGroup)
    bpy.types.Scene.git_history = bpy.props.CollectionProperty(type=GitListItem)
    bpy.types.Scene.git_history_index = bpy.props.IntProperty(name="Index", default=0)

<<<<<<< Updated upstream
    bpy.app.handlers.load_post.append(on_file_open)
    bpy.app.handlers.save_post.append(on_file_save)

=======
    bpy.app.handlers.load_post.append(on_open_handler)
>>>>>>> Stashed changes

def unregister():
    bpy.app.handlers.load_post.remove(on_file_open)
    bpy.app.handlers.save_post.remove(on_file_save)

    for i in reversed(classes):
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.camber_data
    del bpy.types.Scene.git_history
    del bpy.types.Scene.git_history_index

<<<<<<< Updated upstream
=======
    bpy.app.handlers.load_post.remove(on_open_handler)
>>>>>>> Stashed changes

if __name__ == "__main__":
    register()
