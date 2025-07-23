import bpy

class BA_PG_backup_object(bpy.types.PropertyGroup):
    backup_object: bpy.props.StringProperty()

class BA_PG_backup_object_list(bpy.types.PropertyGroup):
    backup_object_list: bpy.props.CollectionProperty(type=BA_PG_backup_object)

