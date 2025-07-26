import bpy

# 根据时间戳为场景中出现的 object 添加一个 uuid 通过 使 原件/备份件/备份状态名字同步
class BA_PG_origin_object(bpy.types.PropertyGroup):
    origin_object_uuid: bpy.props.IntProperty(default=0)
    origin_object_name: bpy.props.StringProperty(default="")

class BA_PG_origin_object_list(bpy.types.PropertyGroup):
    origin_object_list: bpy.props.CollectionProperty(type=BA_PG_origin_object)






# 根据 uuid 对 原始 object与备份object 进行绑定 
class BA_PG_copy_object(bpy.types.PropertyGroup):
    copy_object_uuid: bpy.props.IntProperty(default=0)
    copy_object_name: bpy.props.StringProperty(default="")


class BA_PG_copy_object_list(bpy.types.PropertyGroup):
    copy_object_list: bpy.props.CollectionProperty(type=BA_PG_copy_object)







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

    use_backup: bpy.props.BoolProperty(default=False)