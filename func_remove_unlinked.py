import bpy

def remove_all_unlinked():
    for data_block in [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.textures,
        bpy.data.images,
        bpy.data.curves,
        bpy.data.objects,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.actions,
        bpy.data.collections,
        bpy.data.grease_pencils,
        bpy.data.grease_pencils_v3,
        bpy.data.armatures,
        bpy.data.texts,
        bpy.data.node_groups,
    ]:
        for datablock in data_block:
            if datablock.users == 0:
                data_block.remove(datablock)