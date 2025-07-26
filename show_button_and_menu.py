import bpy
import re
import bmesh
from . import load_custom_icons
from . import ADDON_NAME
from .func_detect_backup_statu import is_in_backup_list

def draw_outliner_header_button(self, context):
    layout = self.layout
    row = layout.row(align=True)

    prefs = context.preferences.addons[ADDON_NAME].preferences

    if context.area.type == 'OUTLINER':
        row.operator("wm.start_backup", text="", icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id)

        if prefs.show_auto_backup:
            row.prop(prefs, "use_auto_backup",icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)
            
        if prefs.backup_preview_button:
            row.prop(prefs, "backup_preview",
                    icon_value=(
                        load_custom_icons.custom_icons["PREVIEW_ON"].icon_id 
                        if prefs.backup_preview 
                        else load_custom_icons.custom_icons["PREVIEW_OFF"].icon_id), 
                    )
    
        row.popover(panel="bak.backup_setting", text="")

def draw_list_unlist_backup(self, context):    
    select_objects = bpy.context.selected_objects

    if is_in_backup_list() in {1,3}:

        layout = self.layout
        layout.separator()
        layout.operator(
            "bak.unlist_from_backup",
            text=f"{select_objects[0].name}移出备份列表" if is_in_backup_list() == 1 else "全部移出备份列表" ,
            icon="RESTRICT_SELECT_ON",
            )
        
    if is_in_backup_list() in {2,4}:
        layout = self.layout
        layout.separator()
        layout.operator(
            "bak.list_to_backup",
            text=f"{select_objects[0].name}移入备份列表" if is_in_backup_list() == 2 else "全部移入备份列表" ,
            icon="RESTRICT_SELECT_OFF",
            )
        
    if is_in_backup_list() == 5:
        layout = self.layout
        layout.separator()
        layout.operator("bak.list_to_backup",text="全部移入备份列表",icon="RESTRICT_SELECT_OFF")
        layout.operator("bak.unlist_from_backup",text="全部移出备份列表",icon="RESTRICT_SELECT_ON")


def draw_start_backup(self, context):
    if not is_in_backup_list():
        return

    layout = self.layout

    prefs = context.preferences.addons[ADDON_NAME].preferences

    backup_object_name = bpy.context.active_object.name

    if prefs.right_click_backup:
        if bpy.context.mode == 'OBJECT' and bpy.context.selected_objects:

            layout.separator()
            layout.operator(
                "wm.start_backup", 
                text=f"备份\"{backup_object_name}\"", 
                icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id,
                ),
                
            
        elif bpy.context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
            if any(v.select for v in bm.verts) or any(e.select for e in bm.edges) or any(f.select for f in bm.faces):

                layout.separator()
                layout.operator(
                    "wm.start_backup", 
                    text=f"备份\"{backup_object_name}\"", 
                    icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id,
                    )

def draw_outliner_delete_backup(self, context):
    if context.active_object.ba_data.object_type == "ORIGIN" and context.active_object.ba_data.object_uuid != "":

        layout = self.layout
        layout.separator()
        layout.operator("bak.delete_backup", text=f"删除{context.active_object.name}的所有备份", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)

def draw_outliner_restore_backup(self, context):
    if not any(coll.name == "BACKUP" for coll in context.scene.collection.children):
        return

    if not any(coll.name == "BACKUP" for coll in bpy.context.active_object.users_collection):
        return
    
    if bpy.context.mode != 'OBJECT':
        return
    
    layout = self.layout

    layout.separator()
    layout.operator("bak.store_backup", text="恢复备份", icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id)

    




                
