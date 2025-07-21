import bpy
from . import ADDON_NAME

class BA_OT_increase_backup(bpy.types.Operator):
    bl_idname = "bak.increase_backup"
    bl_label = "增量备份"
    bl_description = "增量备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        name_infix = context.preferences.addons[ADDON_NAME].preferences.custom_suffix

        bpy.ops.bak.detect_backup_folder()

        origin_edit_mode = context.object.mode
        origin_object = context.active_object

        temp_object_name = context.active_object.name + "_" + name_infix + "_"

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()

        context.active_object.name = temp_object_name

        temp_object = context.active_object

        bpy.ops.object.duplicate()

        bpy.context.active_object.data.name = bpy.context.active_object.name

        backup_object = context.active_object

        for coll in backup_object.users_collection:
            coll.objects.unlink(backup_object)
        bpy.data.collections["BACKUP"].objects.link(backup_object)


        bpy.ops.object.select_all(action='DESELECT')
        temp_object.select_set(True)
        bpy.context.view_layer.objects.active = temp_object
        bpy.ops.object.delete()

        bpy.context.view_layer.objects.active = origin_object
        origin_object.select_set(True)

        bpy.ops.object.mode_set(mode=origin_edit_mode)


        
        self.report({'INFO'}, "已经完成增量备份")
        return {'FINISHED'}