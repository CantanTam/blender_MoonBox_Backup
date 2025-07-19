from . import load_custom_icons

def draw_backup_assistant_button(self, context):
    layout = self.layout

    if context.area.type == 'OUTLINER':
        row = layout.row(align=True) 
        row.operator("bak.increase_backup", text="", icon='CUBE')
        row.operator("bak.increase_backup", text="自定图标", icon_value=load_custom_icons.custom_icons["INCREASE_BACKUP"].icon_id)