import bpy
import re
from . import ADDON_NAME
from .func_remove_unlinked import remove_all_unlinked

class BA_OT_increase_backup(bpy.types.Operator):
    bl_idname = "bak.increase_backup"
    bl_label = "增量备份"
    bl_description = "增量备份"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) and bpy.context.active_object in bpy.context.selected_objects

    def execute(self, context):
        prefs = context.preferences.addons[ADDON_NAME].preferences
        backup_object_infix = prefs.custom_suffix

        bpy.ops.bak.detect_backup_folder()

        origin_edit_mode = context.object.mode
        origin_object = context.active_object

        temp_object_name = context.active_object.name + "_" + backup_object_infix + "_"

        remove_all_unlinked()

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()

        context.active_object.name = temp_object_name

        temp_object = context.active_object

        bpy.ops.object.duplicate()

        bpy.context.active_object.data.name = bpy.context.active_object.name

        backup_object = context.active_object

        for coll in backup_object.users_collection:
            coll.objects.unlink(backup_object)
        bpy.data.collections["BACKUP"].objects.link(backup_object)


        bpy.ops.object.select_all(action='DESELECT')
        temp_object.select_set(True)
        bpy.context.view_layer.objects.active = temp_object
        bpy.ops.object.delete()

        bpy.context.view_layer.objects.active = origin_object
        origin_object.select_set(True)

        bpy.ops.object.mode_set(mode=origin_edit_mode)

        backup_count = prefs.backup_copies_count

        if backup_count == 0:
            return {'FINISHED'}
        else:
            backup_collection = bpy.data.collections["BACKUP"]
            pattern = re.compile(rf"^{re.escape(temp_object_name)}\.(\d+)$")

            while True:
                matched_objs = []
                for obj in backup_collection.objects:
                    match = pattern.match(obj.name)
                    if match:
                        num = int(match.group(1))
                        matched_objs.append((num, obj))

                if len(matched_objs) <= backup_count:
                    break  # 数量已符合条件，退出循环

                # 删除编号最小的那个
                matched_objs.sort(key=lambda x: x[0])
                obj_to_remove = matched_objs[0][1]
                backup_collection.objects.unlink(obj_to_remove)
                bpy.data.objects.remove(obj_to_remove)

            remove_all_unlinked()

            matched_objs = []
            for obj in backup_collection.objects:
                match = pattern.match(obj.name)
                if match:
                    num = int(match.group(1))
                    matched_objs.append((num, obj))

            matched_objs.sort(key=lambda x: x[0])

            # 重新编号，从1开始
            for i, (old_num, obj) in enumerate(matched_objs, start=1):
                new_num_str = f"{i:03d}"  # 格式化为3位数字，不足补0
                # 这里根据你备份名字的规则构造新名字
                # 假设备份名格式是 temp_object_name + "." + 编号
                new_name = f"{temp_object_name}.{new_num_str}"

                if obj.name != new_name:
                    print(f"重命名：{obj.name} -> {new_name}")
                    obj.name = new_name
                    obj.data.name = new_name

            self.report({'INFO'}, "测试指定备份副本数")
        
        return {'FINISHED'}