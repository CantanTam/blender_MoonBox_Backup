import bpy

# 每次操作完，需要反转 BACKUP 内容备份对象的 use_faker_user 值
def reverse_backup_fake_user():
    for item in {item for item in bpy.data.objects if item.ba_data.object_type == "DUPLICATE"}:
        if item.name in bpy.data.collections["BACKUP"].objects:
            item.use_fake_user = False
        else:
            item.use_fake_user = True

def unlist_all_backup():
    for item in {item for item in bpy.data.objects if item.ba_data.object_type == "DUPLICATE"}:
        if item.name in bpy.data.collections["BACKUP"].objects:
            bpy.data.collections["BACKUP"].objects.unlink(item)

    reverse_backup_fake_user()
            

def list_all_backup():
    for item in {item for item in bpy.data.objects if item.ba_data.object_type == "DUPLICATE"}:
        if item.name not in bpy.data.collections["BACKUP"].objects:
            bpy.data.collections["BACKUP"].objects.link(item)

    reverse_backup_fake_user()
            

def list_backup_with_origin():
    unlist_all_backup()

    if bpy.context.active_object.ba_data.object_type == "ORIGIN":
        for item in {item for item in bpy.data.objects if item.ba_data.object_type == "DUPLICATE" 
                    and item.ba_data.object_uuid == bpy.context.active_object.ba_data.object_uuid}:
            bpy.data.collections["BACKUP"].objects.link(item)

    reverse_backup_fake_user()
            

def list_backup_without_origin():
    unlist_all_backup()
    origin_object_uuids = {item.ba_data.object_uuid for item in bpy.data.objects if item.ba_data.object_type == "ORIGIN" }

    for item in {item for item in bpy.data.objects if item.ba_data.object_type == "DUPLICATE" and item.ba_data.object_uuid not in origin_object_uuids}:
        bpy.data.collections["BACKUP"].objects.link(item)

    reverse_backup_fake_user()
        