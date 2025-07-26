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
        col_left.alignment = 'LEFT'
        col_right = split.column()

        col_left.label(text="自动备份")
        col_right.prop(prefs, "show_auto_backup")

        if prefs.show_auto_backup:

            split = layout.split(factor=0.3)
            col_left = split.column()
            col_right = split.column()

            col_left.label(text="备份间隔")
            col_right.prop(prefs, "auto_backup_interval")

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="备份后缀")
        row = col_right.row(align=True)
        row.prop(prefs, "custom_suffix", text="")
        row.operator("wm.start_backup", text="", icon="FILE_REFRESH")
        row.separator()
        row.operator("wm.start_backup", text="", icon="FILE_REFRESH")

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

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="副本数量")
        col_right.prop(prefs, "backup_copies_count")

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="检测间隔")
        col_right.prop(prefs, "detect_rename_interval",icon="ADD")

        split = layout.split(factor=0.3)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="备份后缀")
        row = col_right.row(align=True)
        row.operator("wm.start_backup", text="", icon="FILE_REFRESH")
        row.operator("wm.start_backup", text="", icon="FILE_REFRESH")