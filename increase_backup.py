import bpy

class BA_OT_increase_backup(bpy.types.Operator):
    bl_idname = "bak.increase_backup"
    bl_label = "增量备份"
    bl_description = "增量备份"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        self.report({'INFO'}, "显示“增量备份”")
        print("Outliner header button clicked!")
        return {'FINISHED'}