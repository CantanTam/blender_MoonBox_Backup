import bpy
from . import ADDON_NAME

class BA_OT_shortcut_backup(bpy.types.Operator):
    bl_idname = "bak.shortcut_backup"
    bl_label = "快捷键备份"
    bl_description = "快捷键备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)
    
    def execute(self, context):
        shortcut_backup_mode = context.preferences.addons[ADDON_NAME].preferences.backup_mode

        if shortcut_backup_mode == "OVERWRITE":
            bpy.ops.bak.overwrite_backup()
        elif shortcut_backup_mode == "INCREASE":
            bpy.ops.bak.increase_backup()

        return {'FINISHED'}