import bpy
import re
from . import ADDON_NAME

class BA_OT_restore_backup(bpy.types.Operator):
    bl_idname = "bak.store_backup"
    bl_label = "恢复备份"
    bl_description = "恢复备份"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        restore_object_name = context.active_object.name

        restore_suffix = "_" + context.preferences.addons[ADDON_NAME].preferences.custom_suffix + "_"
        
        del_object_name = re.sub(re.escape(restore_suffix) + ".*$", "", restore_object_name)
        
        shortcut_backup_mode = context.preferences.addons[ADDON_NAME].preferences.backup_mode

        if shortcut_backup_mode == "OVERWRITE":
            bpy.ops.bak.overwrite_backup()
            self.report({'INFO'}, "已经完成覆盖备份")
        elif shortcut_backup_mode == "INCREASE":
            bpy.ops.bak.increase_backup()
            self.report({'INFO'}, "已经完成增量备份")

        return {'FINISHED'}