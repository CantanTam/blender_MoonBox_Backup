import bpy
from . import load_custom_icons
from . import ADDON_NAME

def draw_outliner_header_button(self, context):
    layout = self.layout

    prefs = context.preferences.addons[ADDON_NAME].preferences

    if context.area.type == 'OUTLINER':
        if prefs.backup_mode == "OVERWRITE":
            layout.operator("bak.overwrite_backup", text="", icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id)
        elif prefs.backup_mode == "INCREASE":
            layout.operator("bak.increase_backup", text="", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)

def draw_outliner_delete_backup(self, context):
    layout = self.layout

    layout.separator()
    layout.operator("bak.delete_backup", text="删除备份", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)