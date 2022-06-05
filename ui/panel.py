import bpy
from bpy.types import Operator
import ntpath

from . import icons
from .. import common
from ..plastic import client

class PLASTIC_OT_panel_popup(Operator):
    bl_idname = 'plastic.panel_popup'
    bl_label = 'PlasticSCM Version Control Panel'
    bl_description = 'Open the version control panel for PlasticSCM'

    def invoke(self, context, event):
        client.clear_cache()
        client.refresh_info()

        self.__reset_settings(context)

        preferences = common.get_addon_preferences(context)
        wm = context.window_manager
        return wm.invoke_popup(self, width=preferences.popup_width)

    def draw(self, context):
        if not client.is_connected():
            common.show_error_message('Connection to PlasticSCM failed', ['Couldn\'t connect to the PlasticSCM server. Check your credentials and try again'])
            return

        panel_settings = common.get_plastic_context(context)

        layout = self.layout

        # Header
        layout.label(text='PlasticSCM version control', icon_value=icons.get_icon('LOGO_PLASTIC'), translate=False)

        # File info
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

        # Pending changes
        row = layout.row()
        row.enabled = client.has_changes_available()

        changes_text = 'Pending changes' if client.has_changes_available() else 'No pending changes'
        icon = 'DOWNARROW_HLT' if panel_settings.pending_changes_menu_active else 'RIGHTARROW'
        row.prop(panel_settings, 'pending_changes_menu_active', text=changes_text, icon=icon, translate=False)

        if panel_settings.pending_changes_menu_active:
            comments = panel_settings.checkin_comments

            if len(comments) == 0:
                new_line = panel_settings.checkin_comments.add()
                new_line.line = 'Checkin comment...'

            box = layout.box()

            for comment_index, comment_line in enumerate(comments):
                row = box.row(align=True)

                row.prop(comment_line, 'line', text='', translate=False)

                if comment_index == (len(comments) - 1):
                    row.operator('plastic.add_comment_line', text='', icon='ADD', translate=False)

                    if comment_index != 0:
                        row.operator('plastic.remove_comment_line', text='', icon='PANEL_CLOSE', translate=False).index = comment_index
                else:
                    row.operator('plastic.remove_comment_line', text='', icon='PANEL_CLOSE', translate=False).index = comment_index

            row = box.row()

            row.operator('plastic.checkin', text='Checkin', icon='EXPORT', translate=False)
            row.operator('plastic.undo', text='Undo changes', icon='LOOP_BACK', translate=False)

        # Checkout
        row = layout.row()
        icon = 'DOWNARROW_HLT' if panel_settings.checkout_menu_active else 'RIGHTARROW'
        row.prop(panel_settings, 'checkout_menu_active', text='Checkout / Locking', icon=icon, translate=False)

        if panel_settings.checkout_menu_active:
            box = layout.box()

            row = box.row()
            row.label(text='Checkout status: ' + ('Checked-out' if client.is_checked_out() else 'Not checked-out'), translate=False)

            row = box.row()
            row.label(text='Lock status: ' +  ('Locked' if client.get_lock_owner() is not None else 'Not locked'), translate=False)

            if client.get_lock_owner() is not None:
                row = box.row()
                row.label(text='Lock owner: ' + client.get_lock_owner(), translate=False)

            row = box.row()

            row.operator('plastic.checkout', text='Checkout' if not client.is_checked_out() else 'Checked-out', icon='IMPORT', translate=False)

            if client.get_lock_owner() is not None:
                row.operator('plastic.unlock', text='Unlock', icon='UNLOCKED', translate=False)
            else:
                row.operator('plastic.lock', text='Lock', icon='LOCKED', translate=False)

        # Branching
        row = layout.row()
        icon = 'DOWNARROW_HLT' if panel_settings.branch_menu_active else 'RIGHTARROW'
        row.prop(panel_settings, 'branch_menu_active', text='Branching', icon=icon, translate=False)

        if panel_settings.branch_menu_active:
            active_branch = client.get_active_branch()
            panel_settings.branches = active_branch if active_branch is not None else '-'

            box = layout.box()
            row = box.row()

            col = row.column()
            col.alignment = 'LEFT'
            col.label(text='Switch to', translate=False)
            col.separator()
            col.label(text='Create', translate=False)

            col = row.column()
            col.prop(panel_settings, 'branches', text='', translate=False)
            col.separator()
            row = col.row(align=True)
            row.prop(panel_settings, 'new_branch_name', text='', translate=False)
            row.operator('plastic.create_branch', text='', icon_value=icons.get_icon('CREATE'), translate=False)
            col.separator()
            row = col.row()

            if active_branch is not None:
                row.prop(panel_settings, 'is_child_branch', text='Is child branch?', translate=False)

            row.prop(panel_settings, 'switch_branch', text='Auto-switch', translate=False)

        # History
        row = layout.row()
        icon = 'DOWNARROW_HLT' if panel_settings.history_menu_active else 'RIGHTARROW'
        row.prop(panel_settings, 'history_menu_active', text='Show history', icon=icon, translate=False)

        if panel_settings.history_menu_active:
            history = client.get_history()

            box = layout.box()

            if history is not None:
                for history_entry in history:
                    row = box.row()
                    col_date = row.split(align=True)
                    col_date.label(text=history_entry.date, translate=False)

                    row.label(text=history_entry.owner, translate=False)

                    op = row.operator('plastic.show_history', text='', icon='HIDE_OFF', emboss=False, translate=False)
                    op.date = history_entry.date
                    op.owner = history_entry.owner
                    op.branch = history_entry.branch
                    op.changeset = history_entry.changeset
                    op.comment = history_entry.comment
            else:
                row = box.row()
                row.enabled = False
                row.label(text='Couldn\'t get the file history', translate=False)

            row = layout.row()
            row.alignment = 'RIGHT'
            row.operator('plastic.reload_history', text='Reload history', icon_value=icons.get_icon('REFRESH'), emboss=False, translate=False)

        layout.separator()

        # Preferences
        layout.operator('preferences.addon_show', text='Open add-on settings', icon='PREFERENCES', translate=False).module = common.ADDON_NAME

        layout.separator()

        # Footer
        row = layout.row(align=True)
        col = row.split()
        col.alignment = 'RIGHT'
        col.enabled = False
        col.label(text='PlasticSCM is a product powered by Unity', translate=False)
        row.operator('plastic.open_unity_documentation', text='', icon_value=icons.get_icon('LOGO_UNITY'), emboss=False, translate=False)

    def execute(self, context):
        return {'INTERFACE'}

    def __reset_settings(self, context):
        panel_settings = common.get_plastic_context(context)
        panel_settings.info_menu_active = True
        panel_settings.pending_changes_menu_active = client.has_changes_available()
        panel_settings.checkout_menu_active = False
        panel_settings.branch_menu_active = False
        panel_settings.history_menu_active = False


def register():
    bpy.utils.register_class(PLASTIC_OT_panel_popup)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_panel_popup)
