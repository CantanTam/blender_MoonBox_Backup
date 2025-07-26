import bpy
from .func_remove_unlinked import remove_all_unlinked

class BA_OT_delete_backup(bpy.types.Operator):
    bl_idname = "bak.delete_backup"
    bl_label = "删除备份"
    bl_description = "删除原始文件的所有备份"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"删除{bpy.context.active_object.name}的所有备份？",icon="ERROR")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        delete_objects_uuid = bpy.context.active_object.ba_data.object_uuid

        for item in bpy.data.objects:
            if item.ba_data.object_uuid == delete_objects_uuid and item.ba_data.object_type == "DUPLICATE":
                bpy.data.objects.remove(item, do_unlink=True)

        bpy.context.active_object.ba_data.object_uuid = ""

        remove_all_unlinked()

        return {'FINISHED'}