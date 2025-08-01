import bpy
from . import ADDON_NAME
from .func_list_backup import unlist_all_backup,list_all_backup,list_backup_with_origin,list_backup_without_origin
from .func_sync_name import sync_origin_backup_name
from .preview_backup_sidebar import clear_backup_snapshots

class BA_OT_show_backup(bpy.types.Operator):
    bl_idname = "wm.show_backup"
    bl_label = "列出有原件备份"
    bl_description = "只列出当前选择原文件的备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object.ba_data.object_type == "ORIGIN" and context.active_object.ba_data.object_uuid != ""

    def execute(self, context):
        bpy.data.collections["BACKUP"].hide_viewport = False

        clear_backup_snapshots()

        sync_origin_backup_name()

        list_backup_with_origin()

        return {'FINISHED'}
    
# 这个类，其实可以删除，因为采用侧边栏
class BA_OT_show_backup_without_origin(bpy.types.Operator):
    bl_idname = "wm.show_backup_withou_origin"
    bl_label = "列出无原件备份"
    bl_description = "列出全部"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.collections["BACKUP"].hide_viewport = False

        clear_backup_snapshots()

        sync_origin_backup_name()

        list_backup_without_origin()
        
        return {'FINISHED'}