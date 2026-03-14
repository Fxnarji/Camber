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
            
        layout.operator(OBJECT_OT_Lock.bl_idname, text = "lock").lock = True
        layout.operator(OBJECT_OT_Lock.bl_idname, text = "unlock").lock = False

        self.draw_commit(context, layout)
        self.draw_history(context, layout)

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
        