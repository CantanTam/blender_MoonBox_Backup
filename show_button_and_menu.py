import bpy
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
    if (any(coll.name == "BACKUP" for coll in context.scene.collection.children)) \
        and not any(coll.name == "BACKUP" for coll in context.active_object.users_collection):
        layout = self.layout

        layout.separator()
        layout.operator("bak.delete_backup", text="删除备份", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)


def draw_shortcut_backup(self, context):
    prefs = context.preferences.addons[ADDON_NAME].preferences

    if prefs.right_click_backup:

        layout = self.layout

        layout.separator()
        layout.operator(
            "wm.shortcut_backup", 
            text="覆盖备份" if prefs.backup_mode == "OVERWRITE" else "增量备份", 
            icon_value=(
                load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id
                if prefs.backup_mode == "OVERWRITE" 
                else load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id),
            )