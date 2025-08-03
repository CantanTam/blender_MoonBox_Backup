import bpy
from . import ADDON_NAME
from .func_detect_change import is_edit_change

def auto_backup():
    try:
        if bpy.context.preferences.addons[ADDON_NAME].preferences.use_auto_backup and is_edit_change():
            # 上面添加 is_edit_change() 函数判定
            bpy.ops.wm.start_backup()
    except:
        pass  # 安静地忽略所有错误，保持 timer 运转
    return bpy.context.preferences.addons[ADDON_NAME].preferences.auto_backup_interval

