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

from .preference import BA_OT_preference
from . import load_custom_icons
from .detect_backup_folder import BA_OT_detect_backup_folder
from .increase_backup import BA_OT_increase_backup
from .overwrite_backup import BA_OT_overwrite_backup
from .delete_backup import BA_OT_delete_backup
from .show_button_and_menu import (
    draw_outliner_header_button,
    draw_outliner_delete_backup,
)

def register():
    bpy.utils.register_class(BA_OT_preference)
    load_custom_icons.load_custom_icons()
    bpy.utils.register_class(BA_OT_detect_backup_folder)
    bpy.utils.register_class(BA_OT_increase_backup)
    bpy.utils.register_class(BA_OT_overwrite_backup)
    bpy.utils.register_class(BA_OT_delete_backup)
    bpy.types.OUTLINER_HT_header.prepend(draw_outliner_header_button)
    bpy.types.OUTLINER_MT_object.append(draw_outliner_delete_backup)



def unregister():
    bpy.types.OUTLINER_MT_object.remove(draw_outliner_delete_backup)
    bpy.types.OUTLINER_HT_header.remove(draw_outliner_header_button)
    bpy.utils.unregister_class(BA_OT_delete_backup)
    bpy.utils.unregister_class(BA_OT_overwrite_backup)
    bpy.utils.unregister_class(BA_OT_increase_backup)
    bpy.utils.unregister_class(BA_OT_detect_backup_folder)
    load_custom_icons.clear_custom_icons()
    bpy.utils.unregister_class(BA_OT_preference)


if __name__ == "__main__":
    register()