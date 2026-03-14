import bpy  # type: ignore
from ..constants import AddonProperties
from ..operators.OBJECT_OT_Lock import OBJECT_OT_Lock
from ..operators.GIT_OT_Commit import GIT_OT_Commit
from ..msc.api import API

class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    bl_label = "Camber Debug"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout

        self.draw_commit(context, layout)
        self.draw_history(context, layout)
        self.draw_lock_status(context, layout)


    def draw_lock_status(self, context, layout):
        camber_data = context.scene.camber_data
        box = layout.box()
        box.enabled = False
        box.label(text = f"locked by: {camber_data.get('lock_owner')} since {camber_data.get('lock_date')}", icon = "LOCKED")

    def draw_commit(self, context, parent):
        camber_data = context.scene.camber_data
        
        box = parent.box()
        col = box.column()
        col.label(text="Commit Message:")
        col.prop(camber_data, "commit_message", text = "")
        col.operator(GIT_OT_Commit.bl_idname, text="Push", icon = "EXPORT" )

    def draw_history(self, context, layout):
        layout.template_list(
            "GitUIList", 
            "", 
            context.scene, 
            "git_history", 
            context.scene, 
            "git_history_index")
        
        current_hash = context.scene.camber_data.get("current_version")
        layout.label(text = f"currently checked out: {current_hash}")
        