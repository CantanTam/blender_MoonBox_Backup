import bpy
import os

class BA_OT_test_preview_snapshot(bpy.types.Operator):
    bl_idname = "wm.test_preview_snapshot"
    bl_label = "测试预览快照功能"
    bl_description = "测试预览快照功能"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        previous_render_engine = context.scene.render.engine

        previous_camera_location = context.scene.camera.location.copy()
        previous_camera_euler = context.scene.camera.rotation_euler.copy()

        previous_resolution_x = context.scene.render.resolution_x
        previous_resolution_y = context.scene.render.resolution_y

        previous_render_format = context.scene.render.image_settings.file_format

        context.scene.render.resolution_x = 500
        context.scene.render.resolution_y = 500

        context.scene.render.image_settings.file_format = 'JPEG'

        context.scene.render.engine = 'BLENDER_EEVEE_NEXT'

        bpy.ops.view3d.camera_to_view_selected()

        addon_dir = os.path.dirname(__file__)
        save_dir = os.path.join(addon_dir, "backup_snapshots")
        os.makedirs(save_dir, exist_ok=True)

        snapshot_name = "abcd.jpg"
        save_path = os.path.join(save_dir,snapshot_name)

        context.scene.render.filepath = save_path

        bpy.ops.render.render(write_still=True)

        context.scene.render.engine = previous_render_engine

        context.scene.render.image_settings.file_format = previous_render_format

        context.scene.render.resolution_y = previous_resolution_y
        context.scene.render.resolution_x = previous_resolution_x

        context.scene.camera.location = previous_camera_location
        context.scene.camera.rotation_euler = previous_camera_euler

        
        self.report({'INFO'}, f"{bpy.context.active_object.name}测试snapshot预览功能")
        return {'FINISHED'}