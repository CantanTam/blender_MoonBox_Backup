import bpy

# 大纲视窗调用恢复，需要回到view3d 获取宽度显示恢复提示
def get_view3d_override_for_active_object(context):
    active_obj = context.active_object
    wm = context.window_manager

    for window in wm.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                # 这里可以根据需要精细匹配物体是否显示在该区域
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {
                            "window": window,
                            "screen": screen,
                            "area": area,
                            "region": region,
                            "scene": context.scene,
                            "blend_data": bpy.data,
                            "object": active_obj,
                        }
                        return override
    return None