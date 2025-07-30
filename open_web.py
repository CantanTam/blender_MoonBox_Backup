import bpy
import webbrowser


class BAK_OT_open_website(bpy.types.Operator):
    bl_idname = "bak.open_website"
    bl_label = "打开官方网站"
    bl_description = "点击后打开指定网址"
    
    url: bpy.props.StringProperty(
        name="URL",
        default="https://www.blender.org",
    )

    def execute(self, context):
        webbrowser.open(self.url)
        self.report({'INFO'}, f"已打开网址: {self.url}")
        return {'FINISHED'}