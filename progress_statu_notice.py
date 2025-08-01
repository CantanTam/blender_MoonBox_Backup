import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import os

class BackupNotice:
    def __init__(self, image_path):
        self.image_path = image_path
        self.handler = None
        self.needs_redraw = False
        self.draw_handler = None

        # 固定缩放系数
        self.scale_factor = 1.0

        # 使用固定 notices 文件夹
        if not os.path.isabs(self.image_path):
            script_dir = os.path.dirname(os.path.realpath(__file__))
            script_dir = os.path.normpath(script_dir)
            self.image_path = os.path.normpath(
                os.path.join(script_dir, "notices", self.image_path)
            )

        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Image file not found: {self.image_path}")

        self.image = bpy.data.images.load(self.image_path)
        self.texture = gpu.texture.from_image(self.image)

        if bpy.app.version <= (4, 0, 0):
            self.shader = gpu.shader.from_builtin('2D_IMAGE')
        else:
            self.shader = gpu.shader.from_builtin('IMAGE')

        area_width = bpy.context.area.width
        area_height = bpy.context.area.height

        self.left = (area_width - 480) // 2
        self.right = self.left + 480

        asset_shelf_height = self.get_asset_shelf_height()
        height = asset_shelf_height + 15

        self.vertices = {
            "pos": [
                (self.left, height),
                (self.right, height),
                (self.right, 80 + height),
                (self.left, 80 + height)
            ],
            "texCoord": [(0, 0), (1, 0), (1, 1), (0, 1)],
        }
        self.batch = batch_for_shader(self.shader, 'TRI_FAN', self.vertices)

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.view3d_draw_callback, (), 'WINDOW', 'POST_PIXEL'
        )

        bpy.app.timers.register(self.check_redraw, persistent=True)

        self.show()

    def get_asset_shelf_height(self):
        asset_shelf_height = 0
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == "ASSET_SHELF":
                        asset_shelf_height = region.height
                        break
        return asset_shelf_height

    def update_asset_shelf_height(self):
        asset_shelf_height = self.get_asset_shelf_height()
        area_height = bpy.context.area.height
        height = asset_shelf_height + 15

        new_pos = [
            (self.left, height),
            (self.right, height),
            (self.right, 80 + height),
            (self.left, 80 + height),
        ]
        self.vertices["pos"] = new_pos
        self.batch = batch_for_shader(self.shader, 'TRI_FAN', self.vertices)

    def draw(self):
        self.update_asset_shelf_height()
        gpu.state.blend_set('ALPHA')
        self.shader.bind()
        self.shader.uniform_sampler("image", self.texture)
        self.batch.draw(self.shader)
        gpu.state.blend_set('NONE')

    def show(self):
        if self.handler is None:
            self.handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw, (), 'WINDOW', 'POST_PIXEL'
            )

    def hide(self):
        if self.handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            self.handler = None

    def view3d_draw_callback(self):
        self.needs_redraw = True

    def check_redraw(self):
        if self.needs_redraw:
            self.hide()
            self.needs_redraw = False
        return 1.0

    def cleanup(self):
        self.hide()
        if self.draw_handler:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
            except Exception:
                pass
            self.draw_handler = None

        try:
            bpy.app.timers.unregister(self.check_redraw)
        except Exception:
            pass

        if hasattr(self, 'texture'):
            del self.texture
        if hasattr(self, 'image'):
            del self.image

# 全局控制变量
current_notice = None

def progress_notice(image_name):
    global current_notice
    if current_notice:
        current_notice.cleanup()
        current_notice = None
        bpy.app.timers.register(lambda: None, first_interval=0.1)
    
    current_notice = BackupNotice(image_name)


def register():
    pass

def unregister():
    global current_notice
    if current_notice:
        current_notice.cleanup()
        current_notice = None
