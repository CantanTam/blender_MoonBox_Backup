import bpy

def is_in_backup_list():
    detect_objects = [item.ba_data.use_backup for item in bpy.context.selected_objects]

    if len(detect_objects) == 1 and all(detect_objects): # 单个选项为 True
        return 1
    
    elif len(detect_objects) == 1 and not any(detect_objects): # 单个选项为 False
        return 2
    
    elif len(detect_objects) > 1 and all(detect_objects): # 全部选项为 True
        return 3 
    
    elif len(detect_objects) > 1 and not any(detect_objects): # 全部选项为 False
        return 4
    
    elif len(detect_objects) > 1 and any(detect_objects) and not all(detect_objects): # 选项为 True 混合
        return 5