import bpy

def is_edit_change():
    edit_change_object_list = bpy.context.scene.addon_backup_objects.backup_object_list

    edit_object = bpy.context.active_object

    for item in edit_change_object_list:
        if item.backup_object_name == edit_object.name:
            object_matrix = edit_object.matrix_world
            object_matrix_tuple = tuple(round(v,6) for row in object_matrix for v in row)
            edit_transform_hash = str(hash(object_matrix_tuple))

            if item.backup_transform_hash != edit_transform_hash:
                item.backup_transform_hash = edit_transform_hash
                return True
            
