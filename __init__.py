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
from .increase_backup import BA_OT_increase_backup
from .overwrite_backup import BA_OT_overwrite_backup
from .show_backup_button import draw_backup_assistant_button

def register():
    bpy.utils.register_class(BA_OT_preference)
    load_custom_icons.load_custom_icons()
    bpy.utils.register_class(BA_OT_increase_backup)
    bpy.utils.register_class(BA_OT_overwrite_backup)
    bpy.types.OUTLINER_HT_header.prepend(draw_backup_assistant_button)



def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw_backup_assistant_button)
    bpy.utils.unregister_class(BA_OT_overwrite_backup)
    bpy.utils.unregister_class(BA_OT_increase_backup)
    load_custom_icons.clear_custom_icons()
    bpy.utils.unregister_class(BA_OT_preference)


if __name__ == "__main__":
    register()