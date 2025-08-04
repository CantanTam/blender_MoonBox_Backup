import bpy
import webbrowser


class BAK_OT_open_bilibili(bpy.types.Operator):
    bl_idname = "bak.open_bilibili"
    bl_label = "打开官方网站"
    bl_description = "点击后打开指定网址"
    
    url: bpy.props.StringProperty(
        name="URL",
        default="https://www.bilibili.com/video/BV15MtGzCEVr/",
    )

    def execute(self, context):
        webbrowser.open(self.url)
        self.report({'INFO'}, f"已打开网址: {self.url}")
        return {'FINISHED'}