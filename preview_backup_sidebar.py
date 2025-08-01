import bpy
import bpy.utils.previews
import webbrowser
import os
from . import ADDON_NAME
from .import realtime_preview_backup as modal

backup_snapshots = None
is_snapshot_loaded = False
backup_snapshot_dict = {}
backup_snapshot_reverse_dict = {}

# left right 按钮共用计数
left_right_arrow_shared_count = 0

def load_backup_snapshots():
    global backup_snapshot_dict
    global backup_snapshot_reverse_dict

    global backup_snapshots
    global snapshot_count

    backup_infix = "_" + bpy.context.preferences.addons[ADDON_NAME].preferences.custom_suffix + "_."


    if backup_snapshots is None:
        backup_snapshots = bpy.utils.previews.new()

    snapshot_dir = os.path.join(os.path.dirname(__file__), "backup_snapshots")

    # 同时用于预览和左右按钮预览功能
    backup_snapshot_dict = {
        int(item.name.split(backup_infix)[-1]): item
        for item in bpy.data.objects
        if item.ba_data.object_uuid == bpy.context.active_object.ba_data.object_uuid
        and item.ba_data.object_type == "DUPLICATE"
    }

    # 用于左右按钮预览功能
    backup_snapshot_reverse_dict = {
        item: int(item.name.split(backup_infix)[-1])
        for item in bpy.data.objects
        if item.ba_data.object_uuid == bpy.context.active_object.ba_data.object_uuid
        and item.ba_data.object_type == "DUPLICATE"
    }

    snapshot_count = len(backup_snapshot_dict)

    for item in backup_snapshot_dict.values():
        snapshot_index = item.ba_data.object_uuid + "_" + item.ba_data.backup_uuid
        snapshot_path = os.path.join(snapshot_dir, snapshot_index + ".jpg")
        backup_snapshots.load(snapshot_index, snapshot_path, 'IMAGE' )
        

def clear_backup_snapshots():
    global backup_snapshots
    global is_snapshot_loaded
    if backup_snapshots is not None:
        bpy.utils.previews.remove(backup_snapshots)
        backup_snapshots = None
        is_snapshot_loaded = False

class BA_PT_backup_snapshot_sidebar(bpy.types.Panel):
    bl_label = "备份预览"
    bl_idname = "bak.backup_snapshot_sidebar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Preview"

    def draw(self, context):
        global is_snapshot_loaded
        if not is_snapshot_loaded:
            load_backup_snapshots()
            is_snapshot_loaded = True

        current_backup = bpy.context.active_object
        current_snapshot = current_backup.ba_data.object_uuid + "_" + current_backup.ba_data.backup_uuid

        layout = self.layout
        if context.active_object.ba_data.object_uuid == "" or modal.realtime_preview_statu:
            return
        
        if context.active_object and backup_snapshots and current_snapshot in backup_snapshots:
            box = layout.box()  # 创建一个带边框的区域
            box.template_icon(icon_value=backup_snapshots[current_snapshot].icon_id, scale=10)
            row = layout.row(align=True)
            row.operator("view3d.left_backup", text="◀")
            row.operator("bak.restore_backup",text="恢复备份")
            row.operator("view3d.right_backup", text="▶")
        else:
            box = layout.box()
            box.operator("view3d.backup_snapshot_modal",text="▶启动实时预览")


class BA_OT_left_backup(bpy.types.Operator):
    bl_idname = "view3d.left_backup"
    bl_label = "上一个备份"
    bl_description = "查看上一个备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return backup_snapshot_reverse_dict[context.active_object] > 1

    def execute(self, context):
        global backup_snapshot_reverse_dict

        previous_index = backup_snapshot_reverse_dict[context.active_object] - 1
        previous_object = backup_snapshot_dict[previous_index]

        bpy.data.collections["BACKUP"].hide_select = False
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = False

        bpy.ops.object.select_all(action='DESELECT')
        previous_object.select_set(True)
        bpy.context.view_layer.objects.active = previous_object

        bpy.data.collections["BACKUP"].hide_select = True
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True

        return {'FINISHED'}

class BA_OT_right_backup(bpy.types.Operator):
    bl_idname = "view3d.right_backup"
    bl_label = "下一个备份"
    bl_description = "查看下一个备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return backup_snapshot_reverse_dict[context.active_object] < len(backup_snapshot_reverse_dict)

    def execute(self, context):
        global backup_snapshot_reverse_dict

        next_index = backup_snapshot_reverse_dict[context.active_object] + 1
        next_object = backup_snapshot_dict[next_index]

        bpy.data.collections["BACKUP"].hide_select = False
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = False

        bpy.ops.object.select_all(action='DESELECT')
        next_object.select_set(True)
        bpy.context.view_layer.objects.active = next_object

        bpy.data.collections["BACKUP"].hide_select = True
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True

        return {'FINISHED'}

