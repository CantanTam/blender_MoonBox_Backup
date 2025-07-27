import bpy
from .func_list_backup import unlist_all_backup,list_all_backup,list_backup_with_origin,list_backup_without_origin

class BA_OT_preview_backup(bpy.types.Operator):
    bl_idname = "wm.preview_backup"
    bl_label = "预览备份"
    bl_description = "预览备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        list_backup_with_origin()
        
        self.report({'INFO'}, f"{bpy.context.active_object.name}测试点击list预览功能")
        return {'FINISHED'}
    

class BA_OT_hide_preview_backup(bpy.types.Operator):
    bl_idname = "wm.hide_preview_backup"
    bl_label = "预览备份"
    bl_description = "预览备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        list_backup_without_origin()
        
        self.report({'INFO'}, "测试unlist预览功能")
        return {'FINISHED'}