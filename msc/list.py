import bpy#type: ignore
from ..operators.GIT_OT_Checkout import GIT_OT_Checkout
class GitListItem(bpy.types.PropertyGroup):
    # Each row will have a name and a custom icon/string
    hash: bpy.props.StringProperty()#type: ignore
    msg: bpy.props.StringProperty()#type: ignore
    author: bpy.props.StringProperty()#type: ignore
    date: bpy.props.StringProperty()#type: ignore
    icon: bpy.props.StringProperty(default = "Null")#type: ignore
    size: bpy.props.StringProperty()#type: ignore



class GitUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        detailed = context.scene.camber_data["admin_mode"]

        if detailed:
            self.draw_detailed(layout, context, item)
        else:
            self.draw_simple(layout, context, item)
    
    def draw_simple(self, layout, context, item):

            row = layout.row(align=True)

            #row.prop(item, "size", text=f"", emboss=False, icon = "DISK_DRIVE")
            split = row.split(factor=0.8)
            split.prop(item, "name", text=f"{item.author}", emboss=False)

            current_hash = context.scene.camber_data.get("current_version")
            if current_hash == item.hash:
                checkout = split.operator(GIT_OT_Checkout.bl_idname, text = f"", icon = "COLLECTION_COLOR_04")
            else:
                checkout = split.operator(GIT_OT_Checkout.bl_idname, text = f"get", icon = "IMPORT")
                 
            checkout.hash = item.hash


    def draw_detailed(self, layout, context, item):
            # Create a base row
            row = layout.row(align=True)
            
            s = row.split(factor=0.1) 
            s.label(text=item.hash)
            
            s = s.split(factor=0.15)
            s.label(text=item.author)
            
            s = s.split(factor=0.5)
            s.label(text=item.name)
            
            s = s.split(factor=0.35)
            s.label(text=item.size, icon = "DISK_DRIVE")
            
            s = s.split(factor=0.6)
            s.label(text=item.date)
            row = s.row(align = True)
            row.operator(GIT_OT_Checkout.bl_idname, text="get", icon="LOOP_BACK").hash = item.hash


            



