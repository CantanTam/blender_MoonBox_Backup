from . import load_custom_icons
from . import ADDON_NAME

def draw_backup_assistant_button(self, context):
    layout = self.layout

    prefs = context.preferences.addons[ADDON_NAME].preferences

    if context.area.type == 'OUTLINER':
        if prefs.backup_mode == "OVERWRITE":
            layout.operator("bak.overwrite_backup", text="", icon_value=load_custom_icons.custom_icons["OVERWRITE_BACKUP"].icon_id)
        elif prefs.backup_mode == "INCREASE":
            layout.operator("bak.increase_backup", text="", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)