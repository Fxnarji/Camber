import bpy  # type: ignore
from bpy.app.handlers import persistent #type: ignore
# preferences
from .preferences import Sample_Preferences

# list
from .msc.list import GitListItem, GitUIList

# Operators
from .operators.OBJECT_OT_Lock import OBJECT_OT_Lock
from .operators.DUMMY_OT_DummyOperator import DUMMY_OT_DummyOperator
from .operators.GIT_OT_Commit import GIT_OT_Commit
from .operators.GIT_OT_RefreshHistory import GIT_OT_RefreshHistory
from .operators.GIT_OT_Checkout import GIT_OT_Checkout

# property groups
from .PropertyGroups.propertygroup import CamberPropertyGroup

# panels
from .panels.VIEW3D_PT_UI_Sample import VIEW3D_PT_UI_Sample


# reading values such as name, version and more from toml so there is no need to change information in two places
def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()

    # reading addon name
    extension_name = manifest["name"]

    # reading addon version
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

    # reading Blender version
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

    bl_info = {
        "name": extension_name,
        "version": version_tuple,
        "blender": blender_version_tuple,
    }

    return bl_info


blender_manifest = load_manifest_info()
bl_info = {
    "name": blender_manifest["name"],
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Your Name",
    "version": blender_manifest["version"],
    "blender": blender_manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
    # preferences
    Sample_Preferences,
    # List
    GitListItem,
    GitUIList,   

    # operators:
    OBJECT_OT_Lock,
    DUMMY_OT_DummyOperator,
    GIT_OT_Commit,
    GIT_OT_RefreshHistory,
    GIT_OT_Checkout,
    # Property Groups:
    CamberPropertyGroup,
    # panels:
    VIEW3D_PT_UI_Sample,
]

@persistent
def on_open_handler(dummy):
    print(f"File Opened: {bpy.data.filepath}")
    
    # Example: Refresh your Git history automatically on open
    if bpy.data.filepath:
        try:
            bpy.ops.camber.refresh()
        except Exception as e:
            print(f"Could not refresh git: {e}")


def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.camber_data = bpy.props.PointerProperty(type=CamberPropertyGroup)
    bpy.types.Scene.git_history = bpy.props.CollectionProperty(type=GitListItem)
    bpy.types.Scene.git_history_index = bpy.props.IntProperty(name="Index", default=0)

    bpy.app.handlers.load_post.append(on_open_handler)

def unregister():
    for i in reversed(classes):
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.camber_data
    del bpy.types.Scene.git_history
    del bpy.types.Scene.git_history_index

    bpy.app.handlers.load_post.remove(on_open_handler)

if __name__ == "__main__":
    register()

