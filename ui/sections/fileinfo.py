import bpy
import ntpath

from ...plastic import client

def draw(layout, panel_settings):
    row = layout.row()
    icon = 'DOWNARROW_HLT' if panel_settings.info_menu_active else 'RIGHTARROW'
    row.prop(panel_settings, 'info_menu_active', text='File info', icon=icon, translate=False)

    if panel_settings.info_menu_active:
        box = layout.box()
        row = box.row()
        row.alignment = 'LEFT'
        row.label(text='Name: ' + ntpath.basename(bpy.data.filepath), translate=False)

        row = box.row()
        row.alignment = 'LEFT'
        row.label(text='Status: ' + client.get_status(), translate=False)

        row = box.row()
        row.alignment = 'LEFT'
        row.label(text='Repository: ' + client.get_repository_spec(), translate=False)

        row = box.row()
        row.alignment = 'LEFT'
        row.label(text='Mount point: ' + client.get_mount_point(), translate=False)
