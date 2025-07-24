import bpy

def is_object_edit_change(scene, depsgraph):
    for update in depsgraph.updates:
        id_data = update.id