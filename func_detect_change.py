import bpy

def is_edit_change():
    edit_change_object_list = bpy.context.scene.addon_object_edit_record.backup_object_list

    edit_object = bpy.context.active_object

    for item in edit_change_object_list:
        if item.backup_object_name == edit_object.name:

            # 通过物体形变的与否来判定编辑状态
            if item.backup_transform_hash != str(hash(tuple(round(v,6) for row in edit_object.matrix_world for v in row))):
                item.backup_transform_hash = str(hash(tuple(round(v,6) for row in edit_object.matrix_world for v in row)))
                return True
            
            # 通过添加的修改器数量差别来判定编辑状态
            elif item.backup_modifier_count != len(bpy.context.object.modifiers):
                item.backup_modifier_count = len(bpy.context.object.modifiers)
                return True
            
            # 通过点/线/面各自的值组
            elif item.backup_vef_hash != str(hash((
                    len(bpy.context.active_object.data.vertices),
                    len(bpy.context.active_object.data.edges),
                    len(bpy.context.active_object.data.polygons),
                    ))):
                item.backup_vef_hash = str(hash((
                    len(bpy.context.active_object.data.vertices),
                    len(bpy.context.active_object.data.edges),
                    len(bpy.context.active_object.data.polygons),
                    )))
                return True

            else:
                return False
            

