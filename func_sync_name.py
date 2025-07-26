import bpy
import re
from . import ADDON_NAME

# 每次同步之前需要先同步原件/备份件名称，防止错乱
def sync_origin_backup_name():
    # 原件当中的名字与 uuid 都是唯一，所以可以它来生成字典给 备份件查找
    origin_name_uuid = {
        item.ba_data.object_uuid: item.name
        for item in bpy.data.objects if item.ba_data.object_type == 'ORIGIN'
        and item.ba_data.object_uuid != "" }

    backup_objects = {item2 for item2 in bpy.data.objects if item2.ba_data.object_type == 'DUPLICATE'}

    for item3 in backup_objects:
        if item3.ba_data.object_uuid in origin_name_uuid:
            current_object_name = origin_name_uuid[item3.ba_data.object_uuid]
            current_name_infix = "_" + bpy.context.preferences.addons[ADDON_NAME].preferences.custom_suffix + "_"

            current_backup_name = item3.name
            current_backup_infix = item3.ba_data.backup_infix

            temp_backup_name = item3.name.replace(current_backup_infix,current_name_infix)
            item3.name = temp_backup_name

            final_backup_name = re.sub(rf'^.*(?={re.escape(current_name_infix)}\.)', current_object_name, item3.name)

            item3.name = final_backup_name
            item3.data.name = final_backup_name    

            item3.ba_data.backup_infix = current_name_infix




