import bpy

from . import icons
from ..uvcs import client

__draw_right_builtin = None

def draw_right(self, context):
    if client.is_connected():
        icon_name = 'LOGO_VERSION_CONTROL_CHANGES' if client.has_changes_available() == True else 'LOGO_VERSION_CONTROL'

        row = self.layout.row(align=True)
        row.operator('uvcs.panel_popup', text='', icon_value=icons.get_icon(icon_name), emboss=False, translate=False)

    __draw_right_builtin(self, context)


def register():
    global __draw_right_builtin
    __draw_right_builtin = bpy.types.TOPBAR_HT_upper_bar.draw_right

    bpy.types.TOPBAR_HT_upper_bar.draw_right = draw_right

def unregister():
    bpy.types.TOPBAR_HT_upper_bar.draw_right = __draw_right_builtin
