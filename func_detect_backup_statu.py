import bpy
from .addon_property import BA_PG_backup_object,BA_PG_backup_object_list

def object_backup_status():
    detect_object_backup_list = bpy.context.scene.addon_backup_objects

    selected_object_name = bpy.context.active_object.name

    return selected_object_name in  [item.backup_object for item in detect_object_backup_list.backup_object_list]

