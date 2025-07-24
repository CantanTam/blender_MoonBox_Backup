import bpy

class BA_PG_backup_object(bpy.types.PropertyGroup):
    backup_object: bpy.props.StringProperty()

class BA_PG_backup_object_list(bpy.types.PropertyGroup):
    backup_object_list: bpy.props.CollectionProperty(type=BA_PG_backup_object)

# 用于检测编辑对象是否已经发生的检测项
class BA_PG_change_statu(bpy.types.PropertyGroup):
    transform_statu_hash: bpy.props.StringProperty(default="")
    modifier_statu_hash: bpy.props.StringProperty(default="")

class BA_PG_change_statu_list(bpy.types.PropertyGroup):
    change_statu_list: bpy.props.CollectionProperty(type=BA_PG_change_statu)

