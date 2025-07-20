import bpy
from . import ADDON_NAME

def not_empty_suffix(self, context):
    if self.custom_suffix.strip() == "":
        self.custom_suffix = "BAK"

class BA_OT_preference(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    custom_suffix:bpy.props.StringProperty(
        name="",
        description="备份对象的名称的后缀名，留空则使用默认值",
        default="BAK",
        update=not_empty_suffix,
    )

    backup_mode: bpy.props.EnumProperty(
        name="",
        items=[
            ('OVERWRITE',   "覆盖备份", "用当前状态覆盖原备份"),
            ('INCREASE', "增量备份", "只保存更改的部分"),
        ],
        default='OVERWRITE',
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