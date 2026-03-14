import bpy#type: ignore
from ..operators.GIT_OT_Checkout import GIT_OT_Checkout
class GitListItem(bpy.types.PropertyGroup):
    # Each row will have a name and a custom icon/string
    hash: bpy.props.StringProperty()#type: ignore
    msg: bpy.props.StringProperty()#type: ignore
    author: bpy.props.StringProperty()#type: ignore
    date: bpy.props.StringProperty()#type: ignore



class GitUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            row = layout.row(align=True)
            sub = row.row(align=True)

            row.prop(item, "name", text=item.author, emboss=False)

            sub = row.row(align=True)

            sub.alignment = 'RIGHT'
            checkout = sub.operator(GIT_OT_Checkout.bl_idname, text = "get", icon = "LOOP_BACK")
            checkout.hash = item.hash
