import bpy
from .func_remove_unlinked import remove_all_unlinked
from . import ADDON_NAME

class BA_OT_delete_backup(bpy.types.Operator):
    bl_idname = "bak.delete_backup"
    bl_label = "删除备份"
    bl_description = "删除备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        name_infix = context.preferences.addons[ADDON_NAME].preferences.custom_suffix

        selected_object_name = context.active_object.name

        to_delete_object_name = context.active_object.name + "_" + name_infix + "_"

        backup_collection = bpy.data.collections["BACKUP"]

        to_delete_objects = []
        for obj in backup_collection.objects:
            if obj.name.startswith(to_delete_object_name + ".") and obj.name != to_delete_object_name:
                if len(obj.users_collection) == 1:
                    to_delete_objects.append(obj)

        for obj in to_delete_objects:
            backup_collection.objects.unlink(obj)
            bpy.data.objects.remove(obj, do_unlink=True)

        remove_all_unlinked()

        self.report({'INFO'}, f"已经删除{selected_object_name}的所有备份")
        return {'FINISHED'}