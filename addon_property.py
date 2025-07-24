import bpy

class BA_PG_backup_object(bpy.types.PropertyGroup):
    # 记录需要备份的 object 名称
    backup_object_name: bpy.props.StringProperty(default="")
    # 用于存储编辑变化状态
    backup_transform_hash: bpy.props.StringProperty(default="")
    backup_modifier_count: bpy.props.IntProperty(default=0)
    backp_vef_hash:bpy.props.StringProperty(default="")

    backup_modifier_hash: bpy.props.StringProperty(default="")

class BA_PG_backup_object_list(bpy.types.PropertyGroup):
    backup_object_list: bpy.props.CollectionProperty(type=BA_PG_backup_object)
