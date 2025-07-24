import bpy

def is_edit_change():
    edit_object = bpy.context.active_object

    object_matrix = edit_object.matrix_world

    object_matrix_tuple = tuple(v for row in object_matrix for v in row)