import bpy

class BA_PG_object_edit_record(bpy.types.PropertyGroup):
    backup_object_uuid: bpy.props.IntProperty(default=0)
    # 记录需要备份的 object 名称
    backup_object_name: bpy.props.StringProperty(default="")
    # 用于存储编辑变化状态
    backup_transform_hash: bpy.props.StringProperty(default="")
    backup_modifier_count: bpy.props.IntProperty(default=0)
    backup_vef_hash: bpy.props.StringProperty(default="")

    backup_modifier_hash: bpy.props.StringProperty(default="")

class BA_PG_object_edit_record_list(bpy.types.PropertyGroup):
    backup_object_list: bpy.props.CollectionProperty(type=BA_PG_object_edit_record)


class BA_OB_property(bpy.types.PropertyGroup):
    object_type: bpy.props.EnumProperty(items=[('ORIGIN', "原始文件",""), ('DUPLICATE', "备份文件","")])
    object_uuid: bpy.props.StringProperty(default="")
    # 复制的时候，直接自带 中缀，防止因为用户修改而且产生恢复过程的错乱
    backup_infix: bpy.props.StringProperty(default="")
    backup_time: bpy.props.StringProperty(default="")
    use_backup: bpy.props.BoolProperty(default=True)
    # 用来区分相同原物体的备份快照文件名称
    backup_uuid: bpy.props.StringProperty(default="")
