import bpy
from . import ADDON_NAME

class BA_OT_preference(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    custom_suffix:bpy.props.StringProperty(
        name="",
        description="自定义备份对象的名称的后缀名",
        default="BAK"
    )

    backup_mode: bpy.props.EnumProperty(
        name="",
        description="选择默认的备份模式",
        items=[
            ('OVERWRITE',   "覆盖备份", "用当前状态覆盖原备份", 'MESH_PLANE', 0),
            ('INCREMENTAL', "增量备份", "只保存更改的部分", 'CUBE', 1),
        ],
        default='OVERWRITE',
)
    
    def draw(self, context):
        layout = self.layout
        split = layout.row().split(factor=0.2)

        col_left = split.column()
        col_left.alignment = 'LEFT'
        col_right = split.column()

        col_left.label(text="备份后缀")
        row = col_right.row()
        row.prop(self, "custom_suffix")

        col_left.label(text="备份模式")
        row = col_right.row()
        row.prop(self, "backup_mode")