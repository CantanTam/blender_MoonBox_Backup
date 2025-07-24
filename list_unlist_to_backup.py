import bpy
from .func_detect_backup_statu import object_backup_status

class BA_OT_list_unlist_to_backup(bpy.types.Operator):
    bl_idname = "bak.list_unlist_to_backup"
    bl_label = "添加/移除备份状态"
    bl_description = "具有备份状态的对象才会被备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not object_backup_status():
            new_backup_object = bpy.context.scene.addon_backup_objects.backup_object_list.add()
            new_backup_object.backup_object_name = bpy.context.active_object.name

        else:
            backup_object_list = bpy.context.scene.addon_backup_objects.backup_object_list
            object_to_unlist = bpy.context.active_object.name

            for i, item in enumerate(backup_object_list):
                if item.backup_object_name == object_to_unlist:
                    backup_object_list.remove(i)
                    break

        return {'FINISHED'}
