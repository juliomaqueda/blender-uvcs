import bpy
from bpy.types import Operator

from . import icons
from .sections import branch as branch_section
from .sections import checkin as checkin_section
from .sections import checkout as checkout_section
from .sections import fileinfo as fileinfo_section
from .sections import history as history_section
from .sections import update as update_section
from .. import common
from ..uvcs import client

class UVCS_OT_panel_popup(Operator):
    bl_idname = 'uvcs.panel_popup'
    bl_label = 'Unity Version Control'
    bl_description = 'Open the version control panel'

    def invoke(self, context, event):
        client.clear_cache()
        client.refresh_file_info()

        self.__reset_settings(context)

        preferences = common.get_addon_preferences(context)
        wm = context.window_manager
        return wm.invoke_popup(self, width=preferences.popup_width)

    def draw(self, context):
        if not client.is_connected():
            common.show_error_message('Connection to Unity Version Control failed', ['Couldn\'t connect to the Unity Version Control server. Check your credentials and try again'])
            return

        panel_settings = common.get_uvcs_context(context)

        layout = self.layout

        # Header
        layout.label(text='Unity Version Control', icon_value=icons.get_icon('LOGO_VERSION_CONTROL'), translate=False)

        # Sections
        fileinfo_section.draw(layout, panel_settings)
        checkin_section.draw(layout, panel_settings)
        update_section.draw(layout, panel_settings)
        checkout_section.draw(layout, panel_settings)
        branch_section.draw(layout, panel_settings)
        history_section.draw(layout, panel_settings)

        layout.separator()

        # Preferences
        layout.operator('preferences.addon_show', text='Open add-on settings', icon='PREFERENCES', translate=False).module = common.ADDON_NAME

        layout.separator()

        # Footer
        row = layout.row(align=True)
        row.alignment = 'RIGHT'
        row.enabled = False
        row.label(text='Created by the Unity community', translate=False)

    def execute(self, context):
        return {'INTERFACE'}

    def __reset_settings(self, context):
        panel_settings = common.get_uvcs_context(context)
        panel_settings.info_menu_active = True
        panel_settings.pending_changes_menu_active = client.has_changes_available()
        panel_settings.incoming_changes_menu_active = client.has_incoming_changes()
        panel_settings.show_incoming_changes = False
        panel_settings.checkout_menu_active = False
        panel_settings.branch_menu_active = False
        panel_settings.history_menu_active = False


def register():
    bpy.utils.register_class(UVCS_OT_panel_popup)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_panel_popup)
