import bpy
from . import ADDON_NAME

def detect_rename_add_delete():
    
    all_object_names = {obj.name for obj in bpy.data.objects}

    # 记录备份文件名字与uuid变化的数据结构
    copy_object_names = { item.origin_object_name for item in bpy.context.scene.addon_copy_object.copy_object_list}

    # 记录原文件名字与uuid变化的数据结构
    origin_objects_names = {item.origin_object_name for item in bpy.context.scene.addon_origin_object.origin_object_list}

    if "BACKUP" in bpy.data.collections:
        print("NO BACKUP")

    else:
        if all_object_names == origin_objects_names:
            print("全部一样")

        else:
            print("NONE")
    
    return bpy.context.preferences.addons[ADDON_NAME].preferences.detect_rename_interval
