import bpy

class BA_OT_overwrite_backup(bpy.types.Operator):
    bl_idname = "bak.overwrite_backup"
    bl_label = "覆盖备份"
    bl_description = "覆盖备份"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        self.report({'INFO'}, "显示“覆盖备份”")
        print("Outliner header button clicked!")
        return {'FINISHED'}