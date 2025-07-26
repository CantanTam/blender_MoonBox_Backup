import bpy

class BA_OT_list_to_backup(bpy.types.Operator):
    bl_idname = "bak.list_to_backup"
    bl_label = "移入备份列表"
    bl_description = "被移入备份列表的物体才会被备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in bpy.context.selected_objects:
            item.ba_data.use_backup = True

        return {'FINISHED'}
    
class BA_OT_unlist_from_backup(bpy.types.Operator):
    bl_idname = "bak.unlist_from_backup"
    bl_label = "移出备份列表"
    bl_description = "被移出备份列表的物体不会被备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in bpy.context.selected_objects:
            item.ba_data.use_backup = False

        return {'FINISHED'}
