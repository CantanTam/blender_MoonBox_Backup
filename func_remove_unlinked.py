import bpy

def remove_all_unlinked():
    data_block_list = [
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
        bpy.data.armatures,
        bpy.data.texts,
        bpy.data.node_groups,
    ]

    # 3.4 版本之后增加了 grease_pencils_v3 属性,保证兼容性
    if hasattr(bpy.data,"grease_pencils_v3"):
        data_block_list.append(bpy.data.grease_pencils_v3)

    for data_block in data_block_list:
        for datablock in list(data_block):
            if datablock.users == 0:
                data_block.remove(datablock)