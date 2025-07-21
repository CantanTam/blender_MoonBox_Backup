import bpy
from . import ADDON_NAME

class BA_OT_shortcut_backup(bpy.types.Operator):
    bl_idname = "wm.shortcut_backup"
    # bl_idname 必须使用 'object','view3d','wm' 这样的标准命名方法才能指定快捷键
    bl_label = "快捷键备份"
    bl_description = "快捷键备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.selected_objects
    
    def execute(self, context):
        shortcut_backup_mode = context.preferences.addons[ADDON_NAME].preferences.backup_mode

        if shortcut_backup_mode == "OVERWRITE":
            bpy.ops.bak.overwrite_backup()
            self.report({'INFO'}, "已经完成覆盖备份")
        elif shortcut_backup_mode == "INCREASE":
            bpy.ops.bak.increase_backup()
            self.report({'INFO'}, "已经完成增量备份")

        return {'FINISHED'}