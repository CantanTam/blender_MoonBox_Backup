import bpy
from . import ADDON_NAME
from . import load_custom_icons


class BA_PT_backup_setting(bpy.types.Panel):
    bl_idname = "bak.backup_setting"
    bl_label = "备份设置"
    bl_space_type = 'OUTLINER'
    bl_region_type = 'HEADER'

    def draw(self, context):
        prefs = context.preferences.addons[ADDON_NAME].preferences
        layout = self.layout
        
        split = layout.split(factor=0.25)
        col_left = split.column()
        col_left.alignment = 'LEFT'
        col_right = split.column()
        
        layout.separator()

        split = layout.split(factor=0.25)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="显示选项")
        row = col_right.row()
        row.prop(prefs, "show_auto_backup", icon="CHECKBOX_HLT" if prefs.show_auto_backup else "CHECKBOX_DEHLT")
        row.prop(prefs, "list_leftover_backup", icon="CHECKBOX_HLT" if prefs.list_leftover_backup else "CHECKBOX_DEHLT")
        row.prop(prefs, "right_click_backup", icon="CHECKBOX_HLT" if prefs.right_click_backup else "CHECKBOX_DEHLT")

        col_left.label(text="手动备份")
        row = col_right.row(align=True)
        row.prop(prefs, "custom_suffix")
        row.prop(prefs, "backup_copies_count")

        split = layout.split(factor=0.25)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="自动备份")
        row = col_right.row(align=True)
        row.prop(prefs, "auto_backup_interval")
        row.prop(prefs, "use_auto_backup",icon_value=load_custom_icons.custom_icons["AUTOBACKUP"].icon_id, text="")

        box = layout.box()
        row = box.row()
        row.alert = True
        row.operator("bak.delete_all_backup",text="删除所有备份", icon='TRASH')
        row.operator("bak.delete_leftover_backup",text="删除残留备份",icon="TRASH")

        # 删除下面行可以移除按钮
        box.operator("bak.open_bilibili",text="🌐本插件B站教程",depress=True)
