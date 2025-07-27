import bpy
import re
from . import ADDON_NAME
from .func_remove_unlinked import remove_all_unlinked
from .func_list_backup import list_all_backup

class BA_OT_restore_backup(bpy.types.Operator):
    bl_idname = "bak.restore_backup"
    bl_label = "恢复备份"
    bl_description = "恢复备份"
    bl_options = {'REGISTER', 'UNDO'}
    
    has_origin_object = True
    origin_object_name = ""

    def draw(self, context):
        layout = self.layout
        if self.has_origin_object:
            layout.label(text=f"恢复文件将会覆盖\"{self.origin_object_name}\"，确认恢复？",icon="ERROR")
        else:
            layout.label(text="原文件已经被删除，确认恢复？", icon='ERROR')

    def invoke(self, context, event):
        origin_name_uuids = {
            item.ba_data.object_uuid: item.name
            for item in bpy.data.objects if item.ba_data.object_type == 'ORIGIN'
            and item.ba_data.object_uuid != "" }
        
        if context.active_object.ba_data.object_uuid in origin_name_uuids:
            self.has_origin_object = True
            self.origin_object_name = origin_name_uuids[context.active_object.ba_data.object_uuid]
        else:
            self.has_origin_object = False

        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        list_all_backup()

        restore_object = context.active_object

        if self.has_origin_object:
            self.report({'INFO'}, f"{self.origin_object_name}")
        else:
            self.report({'INFO'}, "没有原始文件")

        return {'FINISHED'}


