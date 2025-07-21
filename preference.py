import bpy
import re
from . import ADDON_NAME

# 强制 custom_suffix 只能使用字母或者数字
def not_empty_suffix(self, context):
    s = self.custom_suffix.replace(" ", "")
    if not s or not re.fullmatch(r'[A-Za-z0-9_-]+', s):
        self.custom_suffix = "BAK"
    else:
        self.custom_suffix = s

class BA_OT_preference(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    custom_suffix:bpy.props.StringProperty(
        name="",
        description="备份对象名称的后缀名，只能使用字母、数字、_、- 这四种符号,空格会被清除",
        default="BAK",
        update=not_empty_suffix,
    )

    backup_mode: bpy.props.EnumProperty(
        name="",
        items=[
            ('OVERWRITE',   "覆盖备份", "用当前状态覆盖原备份"),
            ('INCREASE', "增量备份", "只保存更改的部分"),
        ],
        default='INCREASE',
)
    
    backup_preview:bpy.props.BoolProperty(
        name="",
        description="实时显示选中备份对象",
        default=True,
    )

    backup_preview_button:bpy.props.BoolProperty(
        name="",
        description="是否在大纲视窗头部栏显示实时预览按钮",
        default=True,
    )

    right_click_backup:bpy.props.BoolProperty(
        name="",
        description="开启后，右键菜单会出现备份菜单选项",
        default=True,
    )


    def draw(self, context):
        layout = self.layout

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_left.alignment = 'LEFT'
        col_right = split.column()

        col_left.label(text="备份模式")
        col_right.prop(self, "backup_mode", text="abc", expand=True)

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="备份后缀")
        col_right.prop(self, "custom_suffix")

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="预览按钮")
        col_right.prop(self, "backup_preview_button")

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="右键备份")
        col_right.prop(self, "right_click_backup")