import bpy
#from .addon_property import BA_PG_object_edit_record,BA_PG_object_edit_record_list

def object_backup_status():
    detect_object_backup_list = bpy.context.scene.addon_object_edit_record

    selected_object_name = bpy.context.active_object.name

    return selected_object_name in  [item.backup_object_name for item in detect_object_backup_list.backup_object_list]

