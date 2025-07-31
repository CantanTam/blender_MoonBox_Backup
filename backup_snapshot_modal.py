import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader


def draw_type_2d(color, text, size=17):
    blf.position(0, 20, 70, 0)
    blf.color(0, *color)
    blf.size(0, size*(bpy.context.preferences.system.dpi/72))
    blf.draw(0, text)

def draw_callback_2d(self, context):
    gpu.state.blend_set('ALPHA')

    hud = "Hello Word {} {}".format(len(self.mouse_path), self.mouse_path[-1])
    draw_type_2d((1.0, 0.5, 0.0, 0.8), hud)

    gpu.state.line_width_set(1.0)
    gpu.state.blend_set('NONE')


class BA_OT_backup_snapshot_modal(bpy.types.Operator):
    bl_idname = "view3d.backup_snapshot_modal"
    bl_label = "实时查看备份快照"
    bl_description = "查看上一个备份"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self.handle_2d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_2d, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self.handle_2d, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}