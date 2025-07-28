import bpy

class BA_OT_test_preview_snapshot(bpy.types.Operator):
    bl_idname = "wm.test_preview_snapshot"
    bl_label = "测试预览快照功能"
    bl_description = "测试预览快照功能"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        previous_camera_location = context.scene.camera.location.copy()
        previous_camera_euler = context.scene.camera.rotation_euler.copy()

        previous_resolution_x = context.scene.render.resolution_x
        previous_resolution_y = context.scene.render.resolution_y

        previous_render_format = context.scene.render.image_settings.file_format

        context.scene.render.resolution_x = 500
        context.scene.render.resolution_y = 500

        context.scene.render.image_settings = 'JPEG'

        bpy.ops.view3d.camera_to_view_selected()



        



        
        self.report({'INFO'}, f"{bpy.context.active_object.name}测试snapshot预览功能")
        return {'FINISHED'}