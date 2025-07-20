import bpy

class BA_OT_detect_backup_folder(bpy.types.Operator):
    bl_idname = "bak.detect_backup_folder"
    bl_label = "检测backup文件夹"
    
    def execute(self, context):

        if any(child.name == "BACKUP" for child in context.scene.collection.children):
            bpy.data.collections["BACKUP"].hide_select = True
            bpy.data.collections["BACKUP"].hide_viewport = True
            bpy.data.collections["BACKUP"].hide_render = True
        else:
            bpy.context.scene.collection.children.link(bpy.data.collections.new(name="BACKUP"))

        bpy.data.collections["BACKUP"].hide_select = True
        bpy.data.collections["BACKUP"].hide_viewport = True
        bpy.data.collections["BACKUP"].hide_render = True


        return {'FINISHED'}
    