import bpy

def has_backup_folder():
    if any(child.name == "BACKUP" for child in bpy.context.scene.collection.children):
        #bpy.data.collections["BACKUP"].hide_select = True
        bpy.data.collections["BACKUP"].hide_viewport = True
        bpy.data.collections["BACKUP"].hide_render = True
        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True
    else:
        bpy.context.scene.collection.children.link(bpy.data.collections.new(name="BACKUP"))

    #bpy.data.collections["BACKUP"].hide_select = True
    bpy.data.collections["BACKUP"].hide_viewport = True
    bpy.data.collections["BACKUP"].hide_render = True
    bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = True

    