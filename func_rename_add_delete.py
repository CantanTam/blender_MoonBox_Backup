import bpy
from . import ADDON_NAME

def detect_rename_add_delete():
    all_object_names = {obj.name for obj in bpy.data.objects}

    if bool(bpy.data.collections.get("BACKUP")):
        
        print("has backup")

    else:
        print("NO BACKUP")
    
    return bpy.context.preferences.addons[ADDON_NAME].preferences.detect_rename_interval
