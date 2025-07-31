import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader



operator_info = None

def init():
    global operator_info
    operator_info = bpy.types.SpaceView3D.draw_handler_add(draw_text_and_background, (None, None), 'WINDOW', 'POST_PIXEL')

def draw_text_and_background(self, context):
    
    width = 0

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    width = region.width
                    break

    # 字体绘制设置
    text = "左键:恢复备份  |  滚轮:切换快照  |  右键:退出预览"
    blf.size(0, 40)
    text_width, _ = blf.dimensions(0, text)
    x = (width - text_width) / 2
    blf.position(0, x, 18, 0)

    # 规形相关参数
    vertices = [
        (0, 0),           # 左下角
        (width, 0),       # 右下角
        (0, 70),         # 左上角（高度 100）
        (width, 70)      # 右上角
    ]

    indices = [(0, 1, 2), (2, 1, 3)]
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    
    gpu.state.blend_set('ALPHA')

    shader.bind()
    shader.uniform_float("color", (0, 1, 1, 0.1))
    batch.draw(shader)
    blf.draw(0, text)

    gpu.state.blend_set('NONE')

def remove_operator_info():
    global operator_info
    if operator_info is not None:
        bpy.types.SpaceView3D.draw_handler_remove(operator_info, 'WINDOW')
        operator_info = None

# 运行脚本时初始化
if __name__ == "__main__":
    remove_operator_info()  # 防止重复注册
    init()

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw()











import bpy
import gpu
from gpu_extras.batch import batch_for_shader

def draw():
    # 获取当前 VIEW_3D 区域的宽度和高度（像素）
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    width = region.width
                    break

    # 四个顶点，组成一个矩形：从左下角到右下角，高度 100px
    vertices = [
        (0, 0),           # 左下角
        (width, 0),       # 右下角
        (0, 70),         # 左上角（高度 100）
        (width, 70)      # 右上角
    ]

    indices = [(0, 1, 2), (2, 1, 3)]

    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", (0, 1, 1, 0.1))
    batch.draw(shader)
    gpu.state.blend_set('NONE')

# 注册绘制函数
bpy.types.SpaceView3D.draw_handler_remove(draw,'WINDOW')

bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')

# 强制刷新视图
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw()