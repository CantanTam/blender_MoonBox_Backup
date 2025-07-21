import bpy
import re
from . import ADDON_NAME
from .func_remove_unlinked import remove_all_unlinked

class BA_OT_restore_backup(bpy.types.Operator):
    bl_idname = "bak.store_backup"
    bl_label = "恢复备份"
    bl_description = "恢复备份"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        remove_all_unlinked()

        restore_object = context.active_object
        restore_object_name = context.active_object.name

        restore_suffix = "_" + context.preferences.addons[ADDON_NAME].preferences.custom_suffix + "_"
        
        del_object_name = re.sub(re.escape(restore_suffix) + ".*$", "", restore_object_name)

        origin_edit_mode = context.object.mode
        
        bpy.data.collections["BACKUP"].hide_select = False
        bpy.data.collections["BACKUP"].hide_viewport = False
        bpy.data.collections["BACKUP"].hide_render = False

        bpy.ops.object.select_all(action='DESELECT')
        restore_object.select_set(True)
        bpy.context.view_layer.objects.active = restore_object

        bpy.ops.object.duplicate()

        if not bpy.data.objects.get(del_object_name):
            bpy.context.active_object.name = del_object_name
            bpy.context.active_object.data.name = del_object_name

            bpy.data.collections["BACKUP"].objects.unlink(bpy.data.objects.get(del_object_name))
            bpy.context.scene.collection.objects.link(bpy.data.objects.get(del_object_name))

        bpy.data.collections["BACKUP"].hide_select = True
        bpy.data.collections["BACKUP"].hide_viewport = True
        bpy.data.collections["BACKUP"].hide_render = True

        return {'FINISHED'}