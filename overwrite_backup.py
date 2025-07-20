import bpy
from . import ADDON_NAME

class BA_OT_overwrite_backup(bpy.types.Operator):
    bl_idname = "bak.overwrite_backup"
    bl_label = "覆盖备份"
    bl_description = "覆盖备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        name_infix = context.preferences.addons[ADDON_NAME].preferences.custom_suffix
        bpy.ops.bak.detect_backup_folder()

        to_delete_object_name = context.active_object.name + "_" + name_infix + "_"

        backup_collection = bpy.data.collections["BACKUP"]

        to_delete_objects = []
        for obj in backup_collection.objects:
            if obj.name.startswith(to_delete_object_name + ".") and obj.name != to_delete_object_name:
                if len(obj.users_collection) == 1:
                    to_delete_objects.append(obj)

        for obj in to_delete_objects:
            backup_collection.objects.unlink(obj)
            bpy.data.objects.remove(obj)

        bpy.ops.bak.increase_backup()
        
        self.report({'INFO'}, "显示“覆盖备份”")
        print("Outliner header button clicked!")
        return {'FINISHED'}