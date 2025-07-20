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

        origin_object_name = context.active_object.name

        
        self.report({'INFO'}, "显示“覆盖备份”")
        print("Outliner header button clicked!")
        return {'FINISHED'}