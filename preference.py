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

    list_leftover_backup:bpy.props.BoolProperty(
        name="",
        description="在大纲头栏显示备份列出类型",
        default=True,
    )

    auto_backup_interval:bpy.props.FloatProperty(
        name="",
        description="自动备份的时间间隔，单位为分钟",
        default=5,
        precision=1,
        subtype='TIME',
        
    )
