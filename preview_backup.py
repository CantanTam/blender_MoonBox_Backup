import bpy

class BA_OT_preview_backup(bpy.types.Operator):
    bl_idname = "wm.preview_backup"
    bl_label = "预览备份"
    bl_description = "预览备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.active_object:
            self.report({'INFO'}, "测试点击预览功能")
        return {'FINISHED'}