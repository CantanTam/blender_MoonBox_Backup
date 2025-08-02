import bpy
import os,re,datetime,random,string
from . import ADDON_NAME
from .func_detect_backup_folder import has_backup_folder
from .func_remove_unlinked import remove_all_unlinked
from .func_detect_backup_statu import is_in_backup_list
from .func_detect_change import is_edit_change
from .func_sync_name import sync_origin_backup_name
from .func_list_backup import list_all_backup,list_backup_with_origin
from .progress_notice import progress_notice

class BA_OT_start_backup(bpy.types.Operator):
    bl_idname = "wm.start_backup"
    bl_label = "启动备份"
    bl_description = "启动备份"
    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(cls, context):
        return is_in_backup_list() == 1 and len(context.selected_objects) == 1 and context.active_object in context.selected_objects

    def execute(self, context):
        # 函数含有写操作，而 poll 只允许不非写操作的判定，所以放到主 execute 进行操作
        #if not is_edit_change():
        #   return {'FINISHED'}

        prefs = context.preferences.addons[ADDON_NAME].preferences
        backup_object_infix = prefs.custom_suffix

        has_backup_folder()

        origin_edit_mode = context.object.mode
        origin_object = context.active_object

        origin_object_uuids = [
            item.ba_data.object_uuid
            for item in bpy.data.objects 
            if item.ba_data.object_type == 'ORIGIN']

        # 检测是否有相同 uuid 的原件
        if origin_object.ba_data.object_uuid == "":
            origin_object.ba_data.object_uuid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        elif origin_object != "" and origin_object_uuids.count(origin_object.ba_data.object_uuid) > 1:
            bpy.ops.bak.handler_repeat_uuid('INVOKE_DEFAULT')
            return {'FINISHED'}
            
        list_all_backup()

        sync_origin_backup_name()

        temp_object_name = context.active_object.name + "_" + backup_object_infix + "_"

        remove_all_unlinked()

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()

        context.active_object.name = temp_object_name

        temp_object = context.active_object

        bpy.ops.object.duplicate()

        # 生成 backup_uuid 区分每个备份件
        backup_uuids = {
            item.ba_data.object_uuid
            for item in bpy.data.objects 
            if item.ba_data.object_type == "ORIGIN" 
            and item.ba_data.object_uuid == origin_object.ba_data.object_uuid}
        
        while True:
            new_backup_uuid = ''.join(random.choices(string.ascii_letters, k=6))
            if new_backup_uuid not in backup_uuids:
                break
        
        # 副本指定为 DUPLICATE 类型，并添加备份时间，名字中缀
        context.active_object.ba_data.object_type = "DUPLICATE"
        context.active_object.ba_data.backup_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        context.active_object.ba_data.backup_infix = "_" + backup_object_infix + "_"
        context.active_object.ba_data.backup_uuid = new_backup_uuid
        
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

        # 以下是生成备份 snapshot ：
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
        snapshot_dir = os.path.join(addon_dir, "backup_snapshots")
        os.makedirs(snapshot_dir, exist_ok=True)

        snapshot_name = context.active_object.ba_data.object_uuid + "_" + new_backup_uuid + ".jpg"

        save_path = os.path.join(snapshot_dir,snapshot_name)

        context.scene.render.filepath = save_path

        bpy.ops.render.render(write_still=True,use_viewport=True)

        context.scene.render.engine = previous_render_engine

        context.scene.render.image_settings.file_format = previous_render_format

        context.scene.render.resolution_y = previous_resolution_y
        context.scene.render.resolution_x = previous_resolution_x

        context.scene.camera.location = previous_camera_location
        context.scene.camera.rotation_euler = previous_camera_euler
        # 以上是生成备份 snapshot：

        bpy.ops.object.mode_set(mode=origin_edit_mode)

        backup_count = prefs.backup_copies_count

        if backup_count > 0: # 备份数量不为零的时候，就需要删除多余备份，并删除相应的 snapshot
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

            # 清除多余备份
            remain_backup_names = {
                item.ba_data.object_uuid + "_" + item.ba_data.backup_uuid + ".jpg"
                for item in bpy.data.objects 
                if item.ba_data.object_uuid == context.active_object.ba_data.object_uuid}
            
            all_backup_names = {
                item 
                for item in os.listdir(snapshot_dir)
                if context.active_object.ba_data.object_uuid in item
            }

            delete_backup_names = all_backup_names - remain_backup_names

            for item in delete_backup_names:
                if os.path.exists(os.path.join(snapshot_dir, item)):
                    os.remove(os.path.join(snapshot_dir, item))


        list_backup_with_origin()

        bpy.ops.wm.show_backup()

        progress_notice("BACKUP.png")

        self.report({'INFO'}, "测试指定备份副本数")
        
        
        return {'FINISHED'}