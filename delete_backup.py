import bpy
from . import ADDON_NAME

def remove_all_unlinked():
    for data_block in [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.textures,
        bpy.data.images,
        bpy.data.curves,
        bpy.data.objects,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.actions,
        bpy.data.collections,
        bpy.data.grease_pencils,
        bpy.data.armatures,
        bpy.data.texts,
        bpy.data.node_groups,
    ]:
        for datablock in data_block:
            if datablock.users == 0:
                data_block.remove(datablock)

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