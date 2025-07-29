import bpy
import bpy.utils.previews
import os

backup_snapshot_dict = {}
backup_snapshots = None
is_snapshot_loaded = False

def load_backup_snapshots():
    global backup_snapshots
    if backup_snapshots is None:
        backup_snapshots = bpy.utils.previews.new()

    snapshot_dir = os.path.join(os.path.dirname(__file__), "backup_snapshots")

    for filename in os.listdir(snapshot_dir):
        if filename.lower().endswith(".jpg"):
            snapshot_name = os.path.splitext(filename)[0]
            snapshot_path = os.path.join(snapshot_dir, filename)
            backup_snapshots.load(snapshot_name, snapshot_path, 'IMAGE')

def clear_backup_snapshots():
    global backup_snapshots
    global is_snapshot_loaded
    if backup_snapshots is not None:
        bpy.utils.previews.remove(backup_snapshots)
        backup_snapshots = None
        is_snapshot_loaded = False

class BA_PT_backup_snapshot_sidebar(bpy.types.Panel):
    bl_label = "Icon Image Example"
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
        if backup_snapshots and current_snapshot in backup_snapshots:
            box = layout.box()  # 创建一个带边框的区域
            box.template_icon(icon_value=backup_snapshots[current_snapshot].icon_id, scale=10)
        else:
            layout.label(text="未加载图标")
        layout.operator("transform.translate", icon="CUBE", text="")


