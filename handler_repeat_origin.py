import bpy

class BA_OT_handle_repeat_uuid(bpy.types.Operator):
    bl_idname = "bak.handler_repeat_uuid"
    bl_label = "自定义对话框"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="文件含有重复uuid，需处理后备份", icon="ERROR")
        
        row = layout.row()
        row.operator("bak.remove_other_uuid", text="清除其它uuid", icon="TRASH")
        row.operator("bak.remove_self_uuid", text="清除自身uuid", icon="TRASH")

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=210)

class BA_OT_remove_other_uuid(bpy.types.Operator):
    bl_idname = "bak.remove_other_uuid"
    bl_label = "清除其它文件重复的uuid，然后执行备份"
    bl_description = "清除其它原文件中重复的uuid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "你点击了按钮 A")
        return {'FINISHED'}

class BA_OT_remove_self_uuid(bpy.types.Operator):
    bl_idname = "bak.remove_self_uuid"
    bl_label = "清除文件自身内部的uuid"
    bl_description = "清除其它文件重复的uuid，然后执行备份"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "你点击了按钮 B")
        return {'FINISHED'}

