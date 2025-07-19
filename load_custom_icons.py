import bpy
import os
import bpy.utils.previews

custom_icons = None

def load_custom_icons():
    global custom_icons
    if custom_icons is None:
        custom_icons = bpy.utils.previews.new()
    
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # 扫描 icons 目录中的所有 PNG 文件
    for filename in os.listdir(icons_dir):
        if filename.lower().endswith(".png"):
            icon_name = os.path.splitext(filename)[0]  # 去掉扩展名作为键
            icon_path = os.path.join(icons_dir, filename)
            custom_icons.load(icon_name, icon_path, 'IMAGE')

def clear_custom_icons():
    global custom_icons
    if custom_icons:
        bpy.utils.previews.remove(custom_icons)
        custom_icons = None
