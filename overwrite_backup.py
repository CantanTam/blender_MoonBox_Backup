import bpy

class BA_OT_overwrite_backup(bpy.types.Operator):
    bl_idname = "bak.overwrite_backup"
    bl_label = "覆盖备份"
    bl_description = "覆盖备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        bpy.ops.bak.detect_backup_folder()

        bpy.ops.bak.delete_backup()

        bpy.ops.bak.increase_backup()
        
        self.report({'INFO'}, "已经完成覆盖备份")
        return {'FINISHED'}