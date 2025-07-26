import bpy
import re
from . import ADDON_NAME
from . import load_custom_icons


# 强制 custom_suffix 只能使用字母或者数字
def not_empty_suffix(self, context):
    s = self.custom_suffix.replace(" ", "")
    if not s or not re.fullmatch(r'[A-Za-z0-9]+', s):
        self.custom_suffix = "BAK"
    else:
        self.custom_suffix = s

class BA_OT_preference(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    custom_suffix:bpy.props.StringProperty(
        name="",
        description="备份对象名称的后缀名，只能使用大小写字母或数字,空格会被清除",
        default="BAK",
        update=not_empty_suffix,
    )

    backup_copies_count:bpy.props.IntProperty(
        name="",
        description="设定保留的最近备份的副本数量，0 为无限次",
        default=0,
        min=0,
        soft_max=5,
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

    show_auto_backup:bpy.props.BoolProperty(
        name="",
        description="在大纲视窗头部栏显示自动备份按钮",
        default=True,
    )

    use_auto_backup:bpy.props.BoolProperty(
        name="",
        description="启用自动备份功能",
        default=False,
    )

    auto_backup_interval:bpy.props.FloatProperty(
        name="",
        description="自动备份的时间间隔，单位为秒",
        default=20,
        precision=1,
        subtype='TIME',
        
    )

    detect_rename_interval:bpy.props.FloatProperty(
        name="",
        description="后台检测重命名、添加、删除状态变化的时间间隔，单位为秒",
        default=1.0,
        min=0.1,
        max=10,
        soft_max=2,
        precision=1,
    )

    color_prop: bpy.props.FloatVectorProperty(
        name="My Color",
        subtype='COLOR',
        default=(1.0, 0.5, 0.0),
        min=0.0,
        max=1.0,
        description="选择一个颜色"
    )

    def draw(self, context):
        layout = self.layout

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_left.alignment = 'LEFT'
        col_right = split.column()

        col_left.label(text="自动备份")
        col_right.prop(self, "use_auto_backup")

        if self.use_auto_backup:
            split = layout.split(factor=0.2)
            col_left = split.column()
            col_right = split.column()

            col_left.label(text="备份间隔")
            col_right.prop(self, "auto_backup_interval")

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="备份后缀")
        row = col_right.row(align=True)
        row.prop(self, "custom_suffix", text="")  # 属性不重复 label
        row.operator("wm.start_backup", text="", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)

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

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="副本数量")
        col_right.prop(self, "backup_copies_count")

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="检测间隔")
        col_right.prop(self, "detect_rename_interval")

        split = layout.split(factor=0.2)
        col_left = split.column()
        col_right = split.column()

        col_left.label(text="颜色选择")
        col_right.enabled = True
        col_right.prop(self, "color_prop")