import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader

class BA_OT_backup_snapshot_modal(bpy.types.Operator):
    bl_idname = "view3d.backup_snapshot_modal"
    bl_label = "实时查看备份快照"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object.ba_data.object_uuid != ""

    @staticmethod
    def draw_text_background(self,context):
        # view3d 视窗当前的宽度
        width = bpy.context.area.width

        if bpy.context.active_object.ba_data.object_type == "ORIGIN":
            text_info = "原件"
            background = (0, 1, 1, 0.1)
        elif bpy.context.active_object.ba_data.object_type == "DUPLICATE":
            text_info = "备份文字信息占位符"
            background = (1, 0, 1, 0.1)

        # 定义规形参数
        vertices = [(0, 0),(width, 0),(0, 70),(width, 70)]

        indices = [(0, 1, 2), (2, 1, 3)]
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

        # 定义文本参数
        text_width, _ = blf.dimensions(0, text_info)
        draw_text_width = (width - text_width)/2
        blf.size(0, 30*(bpy.context.preferences.system.dpi/72))
        blf.position(0, draw_text_width, 10, 0)

        gpu.state.blend_set('ALPHA')

        shader.bind()
        shader.uniform_float("color",  background)
        batch.draw(shader)
        blf.draw(0, text_info)

        gpu.state.blend_set('NONE')

    def invoke(self, context, event):

        self.realtime_previews = {
            int(item.name.rsplit(".", 1)[-1]): item
            for item in bpy.data.objects
            if item.ba_data.object_uuid == bpy.context.active_object.ba_data.object_uuid
            and item.ba_data.object_type == "DUPLICATE"
        }

        # 把原件也列入预览列表
        self.preview_count = len(self.realtime_previews) + 1

        self.realtime_previews[self.preview_count] = context.active_object

        bpy.context.view_layer.layer_collection.children['BACKUP'].hide_viewport = False

        for item in self.realtime_previews.values():
            if item.ba_data.object_type == "DUPLICATE":
                item.hide_set(True)

        self.current_object_index = self.preview_count

        if context.area.type == 'VIEW_3D':
            self.handle_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_text_background, (self,context), 'WINDOW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'WHEELUPMOUSE' and event.ctrl == True:
            self.current_object_index -= 1

            if self.current_object_index < 1:
                self.current_object_index = 1

            if self.current_object_index > self.preview_count:
                self.current_object_index = self.preview_count

            for index,object in self.realtime_previews.items():
                if index == self.current_object_index:
                    object.hide_set(False)
                else:
                    object.hide_set(True)

            self.report({'INFO'},f"{self.current_object_index}")

        if event.type == 'WHEELDOWNMOUSE' and event.ctrl == True:
            self.current_object_index += 1

            if self.current_object_index > self.preview_count:
                self.current_object_index = self.preview_count

            for index,object in self.realtime_previews.items():
                if index == self.current_object_index:
                    object.hide_set(False)
                else:
                    object.hide_set(True)

            self.report({'INFO'},f"{self.current_object_index}")

        if event.type in {'RIGHTMOUSE','ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self.handle_2d, 'WINDOW')
            self.report({'INFO'},'YES')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}