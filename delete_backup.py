import bpy
import os
from . import ADDON_NAME
from .func_remove_unlinked import remove_all_unlinked
from .progress_notice import progress_notice

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

        snapshot_dir = os.path.join(os.path.dirname(__file__), "backup_snapshots")

        for item in bpy.data.objects:
            if item.ba_data.object_uuid == delete_objects_uuid and item.ba_data.object_type == "DUPLICATE":
                # 靠删除 snapshot 再删除 object
                delete_backup_name = item.ba_data.object_uuid + "_" + item.ba_data.backup_uuid + ".jpg"
                if os.path.exists(os.path.join(snapshot_dir, delete_backup_name)):
                    os.remove(os.path.join(snapshot_dir, delete_backup_name))
                
                bpy.data.objects.remove(item, do_unlink=True)


        bpy.context.active_object.ba_data.object_uuid = ""

        remove_all_unlinked()

        progress_notice("DELETE.png")

        return {'FINISHED'}
    
class BA_OT_del_name_conflict_duplicate(bpy.types.Operator):
    bl_idname = "bak.del_name_conflict_duplicate"
    bl_label = "删除名字冲突备份"
    bl_description = "删除与原件名字冲突的残留备件"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        auto_backup_statu = context.preferences.addons[ADDON_NAME].preferences.use_auto_backup
        context.preferences.addons[ADDON_NAME].preferences.use_auto_backup = False

        current_object = context.active_object

        backup_uuids = {
            item.ba_data.object_uuid
            for item in bpy.data.objects
            if item.ba_data.object_type == "ORIGIN"
        }

        delete_count = 0
        snapshot_dir = os.path.join(os.path.dirname(__file__), "backup_snapshots")

        for item in bpy.data.objects:
            if item.ba_data.object_type == "DUPLICATE" \
                and item.name.split(item.ba_data.backup_infix)[0] == current_object.name \
                and item.ba_data.object_uuid not in backup_uuids:

                os.remove(os.path.join(snapshot_dir, item.ba_data.object_uuid + "_" + item.ba_data.backup_uuid + ".jpg"))
                bpy.data.objects.remove(item, do_unlink=True)

                delete_count += 1

        self.report({'WARNING'},f"删除{delete_count}个与\"{current_object.name}\"名字冲突的残留备份")                
        
        remove_all_unlinked()

        context.preferences.addons[ADDON_NAME].preferences.use_auto_backup = auto_backup_statu

        progress_notice("DELETE.png")

        return {'FINISHED'}