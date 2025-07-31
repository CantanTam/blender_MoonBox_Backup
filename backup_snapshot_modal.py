import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader





class BA_OT_backup_snapshot_modal(bpy.types.Operator):
    bl_idname = "view3d.backup_snapshot_modal"
    bl_label = "实时查看备份快照"
    bl_description = "查看上一个备份"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def draw_text_background(self,context):
        # view3d 视窗当前的宽度
        width = bpy.context.area.width

        if width < 1000:
            text_info = "short"
            background = (0, 1, 1, 0.1)
        else:
            text_info = "long"
            background = (1, 0, 1, 0.1)

        # 定义规形参数
        vertices = [
            (0, 0),           # 左下角
            (width, 0),       # 右下角
            (0, 70),         # 左上角（高度 100）
            (width, 70)      # 右上角
        ]

        indices = [(0, 1, 2), (2, 1, 3)]
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

        # 定义文本参数
        text_width, _ = blf.dimensions(0, "abc")
        draw_text_width = (width - text_width)/2
        blf.size(0, 17*(bpy.context.preferences.system.dpi/72))
        blf.position(0, draw_text_width, 18, 0)

        gpu.state.blend_set('ALPHA')

        shader.bind()
        shader.uniform_float("color",  background)
        batch.draw(shader)
        blf.draw(0, text_info)

        gpu.state.blend_set('NONE')

    @staticmethod
    def draw_type_2d(color, text, size=17):
        blf.position(0, 20, 70, 0)
        blf.color(0, *color)
        blf.size(0, size*(bpy.context.preferences.system.dpi/72))
        blf.draw(0, text)

    @staticmethod
    def draw_callback_2d(self,context):
        gpu.state.blend_set('ALPHA')

        hud = "Hello Word {} {}".format(len(self.mouse_path), self.mouse_path[-1])
        self.draw_type_2d((1.0, 0.5, 0.0, 0.8), hud)

        gpu.state.line_width_set(1.0)
        gpu.state.blend_set('NONE')

    def invoke(self, context, event):

        if context.area.type == 'VIEW_3D':
            #args = (self,context)
            args = (self,context)
            self.handle_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_text_background, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'LEFTMOUSE':

            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type in {'RIGHTMOUSE','ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self.handle_2d, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}