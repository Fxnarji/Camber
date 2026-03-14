import bpy#type: ignore
from ..operators.GIT_OT_Checkout import GIT_OT_Checkout
class GitListItem(bpy.types.PropertyGroup):
    # Each row will have a name and a custom icon/string
    hash: bpy.props.StringProperty()#type: ignore
    msg: bpy.props.StringProperty()#type: ignore
    author: bpy.props.StringProperty()#type: ignore
    date: bpy.props.StringProperty()#type: ignore
    icon: bpy.props.StringProperty(default = "Null")#type: ignore



class GitUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            row = layout.row(align=True)

            split = row.split(factor=0.8)
            split.prop(item, "name", text=f"{item.author}", emboss=False)

                 
            current_hash = context.scene.camber_data.get("current_version")
            if current_hash == item.hash:
                checkout = split.operator(GIT_OT_Checkout.bl_idname, text = "", icon = "COLLECTION_COLOR_04")
            else:
                checkout = split.operator(GIT_OT_Checkout.bl_idname, text = "get", icon = "LOOP_BACK")
                 
            checkout.hash = item.hash
