import bpy
import os
from bpy.app.handlers import persistent


bl_info = {
    "name": "Backup Assistant",
    "author": "Canta Tam",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D",
    "description": "妈妈再也不怕我误删文件了",
    "category": "3D View",
    "doc_url": "https://www.bilibili.com/video/BV12q4y1t7h9/?spm_id_from=333.1387.upload.video_card.click&vd_source=e4cbc5ec88a2d9cfc7450c34eb007abe", 
    "support": "COMMUNITY"
}

ADDON_NAME = os.path.basename(os.path.dirname(__file__))

addon_keymaps = []

from .addon_property import (
    BA_PG_object_edit_record,
    BA_PG_object_edit_record_list,
    BA_OB_property,
)
from .preference import BA_OT_preference
from . import load_custom_icons
from .list_unlist_backup import (
    BA_OT_list_to_backup,
    BA_OT_unlist_from_backup,
)
from .start_backup import BA_OT_start_backup
from .handler_repeat_origin import (
    BA_OT_handle_repeat_uuid,
    BA_OT_remove_other_uuid,
    BA_OT_remove_self_uuid,
)
from .func_auto_backup import auto_backup
from .delete_backup import BA_OT_delete_backup
from .restore_backup import BA_OT_restore_backup
from .show_hide_backup import (
    BA_OT_show_backup,
    BA_OT_show_backup_without_origin,
)
from .header_popover_panel import BA_PT_backup_setting
from .show_button_and_menu import (
    draw_outliner_header_button,
    draw_list_unlist_backup,
    draw_start_backup,
    draw_outliner_delete_backup,
    draw_outliner_rerestore_backup,
)
from .preview_backup_sidebar import (
    BA_PT_backup_snapshot_sidebar,
    BA_OT_left_backup,
    BA_OT_right_backup,
)

from .open_web import BAK_OT_open_website

from .realtime_preview_backup import BA_OT_backup_snapshot_modal


def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # View3D 的 keymap
        km_view3d = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi_view3d = km_view3d.keymap_items.new("wm.start_backup", type='A', value='PRESS', ctrl=True, shift=True)

        # Outliner 的 keymap
        km_outliner = kc.keymaps.new(name='Outliner', space_type='OUTLINER')
        kmi_outliner = km_outliner.keymap_items.new("wm.start_backup", type='A', value='PRESS', ctrl=True, shift=True)

        km_preview = kc.keymaps.new(name='Outliner', space_type='OUTLINER')
        kmi_preview = km_preview.keymap_items.new("wm.show_backup", type='LEFTMOUSE', value='PRESS', ctrl=True)

        # 保存方便注销时移除
        addon_keymaps.extend([
            (km_view3d, kmi_view3d),
            (km_outliner, kmi_outliner),
            (km_preview, kmi_preview),
        ])

def unregister_keymaps():
    # 逐一移除快捷键
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

@persistent
def auto_backup_on_load(dummy):
    bpy.app.timers.register(auto_backup, first_interval=20.0)

def register():
    bpy.utils.register_class(BA_OB_property)
    bpy.types.Object.ba_data = bpy.props.PointerProperty(type=BA_OB_property)
    bpy.utils.register_class(BA_PG_object_edit_record)
    bpy.utils.register_class(BA_PG_object_edit_record_list)
    bpy.types.Scene.addon_object_edit_record = bpy.props.PointerProperty(type=BA_PG_object_edit_record_list)
    bpy.utils.register_class(BA_OT_preference)
    load_custom_icons.load_custom_icons()
    bpy.utils.register_class(BA_OT_list_to_backup)
    bpy.utils.register_class(BA_OT_unlist_from_backup)
    bpy.utils.register_class(BA_OT_start_backup)
    bpy.utils.register_class(BA_OT_handle_repeat_uuid)
    bpy.utils.register_class(BA_OT_remove_other_uuid)
    bpy.utils.register_class(BA_OT_remove_self_uuid)
    bpy.app.handlers.load_post.append(auto_backup_on_load)
    bpy.utils.register_class(BA_OT_delete_backup)
    bpy.utils.register_class(BA_OT_restore_backup)
    bpy.utils.register_class(BA_OT_show_backup)
    bpy.utils.register_class(BA_OT_show_backup_without_origin)
    bpy.utils.register_class(BA_PT_backup_setting)
    bpy.types.OUTLINER_HT_header.prepend(draw_outliner_header_button)
    bpy.types.OUTLINER_MT_object.append(draw_list_unlist_backup)
    bpy.types.OUTLINER_MT_object.append(draw_outliner_delete_backup)
    bpy.types.OUTLINER_MT_object.append(draw_outliner_rerestore_backup)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_start_backup)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_start_backup)
    bpy.utils.register_class(BA_PT_backup_snapshot_sidebar)
    bpy.utils.register_class(BA_OT_left_backup)
    bpy.utils.register_class(BA_OT_right_backup)
    register_keymaps()

    bpy.utils.register_class(BAK_OT_open_website)
    bpy.utils.register_class(BA_OT_backup_snapshot_modal)




def unregister():
    bpy.utils.unregister_class(BA_OT_backup_snapshot_modal)
    bpy.utils.unregister_class(BAK_OT_open_website)

    unregister_keymaps()
    bpy.utils.unregister_class(BA_OT_right_backup)
    bpy.utils.unregister_class(BA_OT_left_backup)
    bpy.utils.unregister_class(BA_PT_backup_snapshot_sidebar)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_start_backup)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_start_backup)
    bpy.types.OUTLINER_MT_object.remove(draw_outliner_rerestore_backup)
    bpy.types.OUTLINER_MT_object.remove(draw_outliner_delete_backup)
    bpy.types.OUTLINER_MT_object.remove(draw_list_unlist_backup)
    bpy.types.OUTLINER_HT_header.remove(draw_outliner_header_button)
    bpy.utils.unregister_class(BA_PT_backup_setting)
    bpy.utils.unregister_class(BA_OT_show_backup_without_origin)
    bpy.utils.unregister_class(BA_OT_show_backup)
    bpy.utils.unregister_class(BA_OT_restore_backup)
    bpy.utils.unregister_class(BA_OT_delete_backup)
    bpy.app.handlers.load_post.remove(auto_backup_on_load)
    bpy.utils.unregister_class(BA_OT_remove_self_uuid)
    bpy.utils.unregister_class(BA_OT_remove_other_uuid)
    bpy.utils.unregister_class(BA_OT_handle_repeat_uuid)
    bpy.utils.unregister_class(BA_OT_start_backup)
    bpy.utils.unregister_class(BA_OT_unlist_from_backup)
    bpy.utils.unregister_class(BA_OT_list_to_backup)
    load_custom_icons.clear_custom_icons()
    bpy.utils.unregister_class(BA_OT_preference)
    del bpy.types.Scene.addon_object_edit_record
    bpy.utils.unregister_class(BA_PG_object_edit_record_list)
    bpy.utils.unregister_class(BA_PG_object_edit_record)
    del bpy.types.Object.ba_data
    bpy.utils.unregister_class(BA_OB_property)


if __name__ == "__main__":
    register()