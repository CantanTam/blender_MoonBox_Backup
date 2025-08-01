import bpy
import datetime
from . import ADDON_NAME
from .func_remove_unlinked import remove_all_unlinked
from .func_list_backup import list_all_backup,list_backup_with_origin
from .progress_notice import progress_notice

class BA_OT_restore_backup(bpy.types.Operator):
    bl_idname = "bak.restore_backup"
    bl_label = "恢复备份"
    bl_description = "恢复备份"
    bl_options = {'REGISTER', 'UNDO'}
    
    has_origin_object = True
    origin_object_name = ""
    origin_object_data_name = ""

    def draw(self, context):
        layout = self.layout
        if self.has_origin_object:
            layout.label(text=f"恢复文件将会覆盖\"{self.origin_object_name}\"，确认恢复？",icon="ERROR")
        else:
            layout.label(text="原文件已经被删除，确认恢复？", icon='ERROR')

    def invoke(self, context, event):
        origin_name_uuids = {
            item.ba_data.object_uuid: item.name
            for item in bpy.data.objects 
            if item.ba_data.object_type == 'ORIGIN'
            and item.ba_data.object_uuid != "" }
        
        if context.active_object.ba_data.object_uuid in origin_name_uuids:
            self.has_origin_object = True
            self.origin_object_name = origin_name_uuids[context.active_object.ba_data.object_uuid]
            self.origin_object_data_name = bpy.data.objects[self.origin_object_name].data.name
        else:
            self.has_origin_object = False

        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):

        list_all_backup()

        #bpy.data.collections["BACKUP"].hide_select = False
        bpy.data.collections["BACKUP"].hide_viewport = False
        bpy.data.collections["BACKUP"].hide_render = False
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = False

        bpy.ops.object.select_all(action='DESELECT')
        context.active_object.select_set(True)
        bpy.context.view_layer.objects.active = context.active_object
        
        bpy.ops.object.duplicate()

        restore_object = context.active_object

        bpy.context.active_object.ba_data.object_type = "ORIGIN"
        bpy.context.active_object.ba_data.backup_uuid = ""
        bpy.context.active_object.use_fake_user = False        

        if self.has_origin_object:
            for item in bpy.data.objects:
                if item.ba_data.object_uuid == context.active_object.ba_data.object_uuid and item.ba_data.object_type == 'ORIGIN':
                    item.hide_set(False)

            collections = bpy.data.objects[self.origin_object_name].users_collection

            for coll in collections:
                coll.objects.link(context.active_object)

            bpy.data.collections["BACKUP"].objects.unlink(context.active_object)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[self.origin_object_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[self.origin_object_name]
            bpy.ops.object.delete()

            remove_all_unlinked()

            restore_object.name = self.origin_object_name
            restore_object.data.name = self.origin_object_data_name

        else:
            # 为防止无原始文件数据名称冲突，这里直接使用日期时间作为数据名称
            restore_object.data.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            bpy.data.collections["BACKUP"].objects.unlink(restore_object)
            bpy.context.scene.collection.objects.link(restore_object)

            remove_all_unlinked()
            self.report({'INFO'}, "没有原始文件")

        restore_object.select_set(True)
        bpy.context.view_layer.objects.active = restore_object

        #bpy.data.collections["BACKUP"].hide_select = True
        bpy.data.collections["BACKUP"].hide_viewport = True
        bpy.data.collections["BACKUP"].hide_render = True
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True

        list_backup_with_origin()

        bpy.ops.wm.show_backup()

        progress_notice("RESTORE.png")

        return {'FINISHED'}


