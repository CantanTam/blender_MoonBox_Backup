import bpy
from . import ADDON_NAME
from .func_list_backup import list_backup_without_origin,list_backup_with_origin
from .preview_backup_sidebar import to_stop_sidbar

class BA_OT_handle_repeat_uuid(bpy.types.Operator):
    bl_idname = "bak.handler_repeat_uuid"
    bl_label = "处理重复uuid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="文件含有重复uuid，需处理后备份", icon="ERROR")
        
        row = layout.row()
        row.operator("bak.remove_other_uuid", text="清除其它uuid", icon="TRASH")
        row.operator("bak.remove_self_uuid", text="清除自身uuid", icon="TRASH")

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=210)

class BA_OT_remove_other_uuid(bpy.types.Operator):
    bl_idname = "bak.remove_other_uuid"
    bl_label = "清除其它文件重复的uuid，然后执行备份"
    bl_description = "清除其它原文件中重复的uuid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_object = context.active_object
        for item in {
            item 
            for item in bpy.data.objects
            if item.ba_data.object_uuid !=""
            and item.ba_data.object_uuid == selected_object.ba_data.object_uuid
            and item != selected_object}:
            item.ba_data.object_uuid = ""

        bpy.ops.wm.start_backup()

        return {'FINISHED'}

class BA_OT_remove_self_uuid(bpy.types.Operator):
    bl_idname = "bak.remove_self_uuid"
    bl_label = "清除文件自身内部的uuid"
    bl_description = "清除其它文件重复的uuid，然后执行备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.active_object.ba_data.object_uuid = ""

        bpy.ops.wm.start_backup()

        return {'FINISHED'}
    
class BA_OT_handle_conflict_name(bpy.types.Operator):
    bl_idname = "bak.handler_conflict_name"
    bl_label = "重命名当前"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="当前文件与残留备份文件名字冲突", icon="ERROR")
        
        row = layout.row()
        row.operator("bak.rename_conflict_object", text="重命名物体", icon="GREASEPENCIL")
        row.operator("bak.del_name_conflict_duplicate", text="清除名字冲突备份件", icon="GREASEPENCIL")

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=250)


class BA_OT_rename_conflict_object(bpy.types.Operator):
    bl_idname = "bak.rename_conflict_object"
    bl_label = "重命名名字冲突对象"
    bl_description = "当前原文件名字与残留的备份文件名字冲突"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_panel(name="TOPBAR_PT_name", keep_open=False)

        return {'FINISHED'}
    
class BA_OT_del_name_conflict_duplicate(bpy.types.Operator):
    bl_idname = "bak.del_name_conflict_duplicate"
    bl_label = "删除名字冲突备份"
    bl_description = "删除与原件名字冲突的残留备件"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.collections["BACKUP"].hide_viewport = False
        bpy.data.collections["BACKUP"].hide_render = False
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = False
        
        auto_backup_statu = context.preferences.addons[ADDON_NAME].preferences.use_auto_backup
        context.preferences.addons[ADDON_NAME].preferences.use_auto_backup = False

        global to_stop_sidbar
        to_stop_sidbar = True

        list_backup_without_origin()

        current_object = context.active_object

        backup_uuids = {
            item.ba_data.object_uuid
            for item in bpy.data.objects
            if item.ba_data.object_type == "ORIGIN"
        }

        delete_count = 0

        backup_to_delete = {
            item
            for item in bpy.data.objects
            if item.ba_data.object_type == "DUPLICATE"
            and item.name.split(item.ba_data.backup_infix)[0] == current_object.name
            and item.ba_data.object_uuid not in backup_uuids
        }
        
        for item in backup_to_delete:

            bpy.ops.object.select_all(action='DESELECT')
            item.select_set(True)
            bpy.context.view_layer.objects.active = item
            bpy.ops.object.delete()

            delete_count += 1

        bpy.ops.object.select_all(action='DESELECT')
        current_object.select_set(True)
        bpy.context.view_layer.objects.active = current_object

        context.preferences.addons[ADDON_NAME].preferences.use_auto_backup = auto_backup_statu

        bpy.data.collections["BACKUP"].hide_viewport = True
        bpy.data.collections["BACKUP"].hide_render = True
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True

        to_stop_sidbar = False

        list_backup_with_origin()

        self.report({'WARNING'},f"删除{delete_count}个与\"{current_object.name}\"名字冲突的残留备份")                

        return {'FINISHED'}