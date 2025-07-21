import bpy
import re
import bmesh
from . import load_custom_icons
from . import ADDON_NAME

def draw_outliner_header_button(self, context):
    layout = self.layout
    row = layout.row(align=True)

    prefs = context.preferences.addons[ADDON_NAME].preferences

    if context.area.type == 'OUTLINER':
        if prefs.backup_mode == "OVERWRITE":
            row.operator("bak.overwrite_backup", text="", icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id)
        elif prefs.backup_mode == "INCREASE":
            row.operator("bak.increase_backup", text="", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)
        
        if prefs.backup_preview_button:
            row.prop(prefs, "backup_preview",
                    icon_value=(
                        load_custom_icons.custom_icons["PREVIEW_ON"].icon_id 
                        if prefs.backup_preview 
                        else load_custom_icons.custom_icons["PREVIEW_OFF"].icon_id), 
                    )
    
        row.popover(panel="bak.backup_setting", text="")

def draw_outliner_delete_backup(self, context):
    if not any(coll.name == "BACKUP" for coll in context.scene.collection.children):
        return

    if any(coll.name == "BACKUP" for coll in bpy.context.active_object.users_collection):
        return

    backup_collection = bpy.data.collections.get("BACKUP")
    if not backup_collection:
        return

    del_suffix = bpy.context.preferences.addons[ADDON_NAME].preferences.custom_suffix

    del_prefix = f"{bpy.context.active_object.name}_{del_suffix}_"

    del_pattern = re.compile(rf"^{re.escape(del_prefix)}\..+")

    if not any(del_pattern.match(obj.name) for obj in backup_collection.objects):
        return

    layout = self.layout

    layout.separator()
    layout.operator("bak.delete_backup", text="删除备份", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)


def draw_shortcut_backup(self, context):
    layout = self.layout

    prefs = context.preferences.addons[ADDON_NAME].preferences

    if prefs.right_click_backup:
        if bpy.context.mode == 'OBJECT' and bpy.context.selected_objects:

            layout.separator()
            layout.operator(
                "wm.shortcut_backup", 
                text="覆盖备份" if prefs.backup_mode == "OVERWRITE" else "增量备份", 
                icon_value=(
                    load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id
                    if prefs.backup_mode == "OVERWRITE" 
                    else load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id),
                )
            
        elif bpy.context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
            if any(v.select for v in bm.verts) or any(e.select for e in bm.edges) or any(f.select for f in bm.faces):

                layout.separator()
                layout.operator(
                    "wm.shortcut_backup", 
                    text="覆盖备份" if prefs.backup_mode == "OVERWRITE" else "增量备份", 
                    icon_value=(
                        load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id
                        if prefs.backup_mode == "OVERWRITE" 
                        else load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id),
                    )