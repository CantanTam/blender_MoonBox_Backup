import bpy
from . import ADDON_NAME

def auto_backup():
    try:
        if bpy.context.preferences.addons[ADDON_NAME].preferences.use_auto_backup \
            and bpy.context.preferences.addons[ADDON_NAME].preferences.show_auto_backup:
            bpy.ops.wm.start_backup()
    except:
        pass  # 安静地忽略所有错误，保持 timer 运转
    return bpy.context.preferences.addons[ADDON_NAME].preferences.auto_backup_interval

