import bpy
from . import ADDON_NAME

class BA_PT_backup_setting(bpy.types.Panel):
    bl_idname = "bak.backup_setting"
    bl_label = "备份设置"
    bl_space_type = 'OUTLINER'
    bl_region_type = 'HEADER'

    def draw(self, context):
        prefs = context.preferences.addons[ADDON_NAME].preferences
        layout = self.layout

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        layout.label(text="备份模式")
        layout.prop(prefs, "backup_mode", text="abc", expand=True)

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="备份后缀")
        row = col_right.row(align=True)
        row.prop(prefs, "custom_suffix", text="")
        row.operator("wm.shortcut_backup", text="", icon="FILE_REFRESH")

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="预览按钮")
        col_right.prop(prefs, "backup_preview_button")

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="右键备份")
        col_right.prop(prefs, "right_click_backup")