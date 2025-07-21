import bpy

bl_info = {
    "name": "Backup Assistant",
    "author": "Canta Tam",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D",
    "description": "让备份更简单",
    "category": "3D View",
    "doc_url": "https://www.bilibili.com/video/BV12q4y1t7h9/?spm_id_from=333.1387.upload.video_card.click&vd_source=e4cbc5ec88a2d9cfc7450c34eb007abe", 
    "support": "COMMUNITY"
}

ADDON_NAME = __package__

addon_keymaps = []


from .preference import BA_OT_preference
from . import load_custom_icons
from .detect_backup_folder import BA_OT_detect_backup_folder
from .increase_backup import BA_OT_increase_backup
from .overwrite_backup import BA_OT_overwrite_backup
from .shortcut_backup import BA_OT_shortcut_backup
from .delete_backup import BA_OT_delete_backup
from .header_popover_panel import BA_PT_backup_setting
from .show_button_and_menu import (
    draw_outliner_header_button,
    draw_outliner_delete_backup,
    draw_shortcut_backup,
)

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # View3D 的 keymap
        km_view3d = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi_view3d = km_view3d.keymap_items.new("wm.shortcut_backup", type='A', value='PRESS', ctrl=True, shift=True)

        # Outliner 的 keymap
        km_outliner = kc.keymaps.new(name='Outliner', space_type='OUTLINER')
        kmi_outliner = km_outliner.keymap_items.new("wm.shortcut_backup", type='A', value='PRESS', ctrl=True, shift=True)

        # 保存方便注销时移除
        addon_keymaps.extend([
            (km_view3d, kmi_view3d),
            (km_outliner, kmi_outliner),
        ])

def unregister_keymaps():
    # 逐一移除快捷键
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(BA_OT_preference)
    load_custom_icons.load_custom_icons()
    bpy.utils.register_class(BA_OT_detect_backup_folder)
    bpy.utils.register_class(BA_OT_increase_backup)
    bpy.utils.register_class(BA_OT_overwrite_backup)
    bpy.utils.register_class(BA_OT_shortcut_backup)
    bpy.utils.register_class(BA_OT_delete_backup)
    bpy.utils.register_class(BA_PT_backup_setting)
    bpy.types.OUTLINER_HT_header.prepend(draw_outliner_header_button)
    bpy.types.OUTLINER_MT_object.append(draw_outliner_delete_backup)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_shortcut_backup)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_shortcut_backup)
    register_keymaps()



def unregister():
    unregister_keymaps()
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_shortcut_backup)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_shortcut_backup)
    bpy.types.OUTLINER_MT_object.remove(draw_outliner_delete_backup)
    bpy.types.OUTLINER_HT_header.remove(draw_outliner_header_button)
    bpy.utils.unregister_class(BA_PT_backup_setting)
    bpy.utils.unregister_class(BA_OT_delete_backup)
    bpy.utils.unregister_class(BA_OT_shortcut_backup)
    bpy.utils.unregister_class(BA_OT_overwrite_backup)
    bpy.utils.unregister_class(BA_OT_increase_backup)
    bpy.utils.unregister_class(BA_OT_detect_backup_folder)
    load_custom_icons.clear_custom_icons()
    bpy.utils.unregister_class(BA_OT_preference)


if __name__ == "__main__":
    register()