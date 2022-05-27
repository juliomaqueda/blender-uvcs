import bpy
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
import os

from .. import common
from ..plastic import client

class PLASTIC_OT_create_branch(Operator):
    bl_idname = 'plastic.create_branch'
    bl_label = 'Create branch'
    bl_description = 'Create a new branch with the supplied name'

    @classmethod
    def poll(cls, context):
        panel_settings = common.get_plastic_context(context)
        return panel_settings.new_branch_name != ''

    def execute(self, context):
        panel_settings = common.get_plastic_context(context)
        is_child_branch = panel_settings.is_child_branch
        branch_name = panel_settings.new_branch_name if not is_child_branch else client.get_active_branch() + '/' + panel_settings.new_branch_name

        create_branch_error_log = client.create_branch(branch_name)

        if create_branch_error_log is None:
            panel_settings.new_branch_name = ''
            panel_settings.is_child_branch = False

            if panel_settings.switch_branch:
                panel_settings.switch_branch = False

                switch_error_log = client.switch_to_branch(branch_name)

                if switch_error_log is None:
                    if os.path.exists(bpy.data.filepath):
                        bpy.ops.wm.revert_mainfile()
                    else:
                        common.show_warning_message('Branch switched', ['The workspace was switched to a branch where the current file doesn\'t exist'])
                else:
                    common.show_error_log('Branch switch failed', 'Although the new branch was created successfully, it was not possible to switch to it.', switch_error_log)
            else:
                common.show_info_message('Branch creation completed', ['The new branch ' + branch_name + ' was created successfully'])
        else:
            common.show_error_log('Branch creation failed', create_branch_error_log)

        return {'FINISHED'}

class PLASTIC_OT_add_comment_line(Operator):
    bl_idname = 'plastic.add_comment_line'
    bl_label = 'Add line'
    bl_description = 'Add a new comment line'

    def execute(self, context):
        panel_settings = common.get_plastic_context(context)

        comment_line = panel_settings.checkin_comments.add()
        comment_line.line = ''

        return {'FINISHED'}

class PLASTIC_OT_remove_comment_line(Operator):
    bl_idname = 'plastic.remove_comment_line'
    bl_label = 'Remove line'
    bl_description = 'Remove this comment line'

    index: IntProperty()

    def execute(self, context):
        panel_settings = common.get_plastic_context(context)

        if len(panel_settings.checkin_comments) >= (self.index + 1):
            panel_settings.checkin_comments.remove(self.index)

        return {'FINISHED'}

class PLASTIC_OT_checkin(Operator):
    bl_idname = 'plastic.checkin'
    bl_label = 'Checkin'
    bl_description = 'Submit checkin with the current changes'

    @classmethod
    def poll(cls, context):
        return client.has_changes_available()

    def execute(self, context):
        panel_settings = common.get_plastic_context(context)

        comment_lines = []

        for checkin_comment in panel_settings.checkin_comments:
            comment_lines.append(checkin_comment.line)

        checkin_error_log = client.checkin('\n'.join(comment_lines))

        if checkin_error_log is None:
            panel_settings.checkin_comments.clear()
            panel_settings.checkin_menu_active = False

            common.show_info_message('Checkin completed', ['Checkin completed successfully.'])
        else:
            common.show_error_log('Checkin failed', 'It was not possible to complete the checkin.', checkin_error_log)

        return {'FINISHED'}

class PLASTIC_OT_checkout(Operator):
    bl_idname = 'plastic.checkout'
    bl_label = 'Checkout'
    bl_description = 'Checkout the file'

    @classmethod
    def poll(cls, context):
        return not client.is_checked_out()

    def execute(self, context):
        checkout_error_log = client.checkout()

        if checkout_error_log is None:
            common.show_info_message('Checkout completed', ['Checkout completed successfully.'])
        else:
            common.show_error_log('Checkout failed', 'It was not possible to complete the checkout.', checkout_error_log)

        return {'FINISHED'}

class PLASTIC_OT_undo(Operator):
    bl_idname = 'plastic.undo'
    bl_label = 'Undo changes'
    bl_description = 'Undo the current changes'

    def execute(self, context):
        undo_error_log = client.undo()

        if undo_error_log is None:
            bpy.ops.wm.revert_mainfile()
        else:
            common.show_error_log('Undo failed', 'It was not possible to undo the changes.', undo_error_log)

        return {'FINISHED'}

class PLASTIC_OT_lock(Operator):
    bl_idname = 'plastic.lock'
    bl_label = 'Lock'
    bl_description = 'Lock the current file'

    def execute(self, context):
        checkout_error_log = client.checkout()

        if checkout_error_log is None:
            if client.get_lock_owner() is not None:
                common.show_info_message('Lock completed', ['The file was successfully locked.'])
            else:
                common.show_error_message('Lock failed', ['The current file doesn\'t meet the locking criteria.'])
        else:
            common.show_error_log('Checkout failed', 'It was not possible to checkout the file.', checkout_error_log)

        return {'FINISHED'}

class PLASTIC_OT_unlock(Operator):
    bl_idname = 'plastic.unlock'
    bl_label = 'Unlock'
    bl_description = 'Remove the current lock'

    def execute(self, context):
        unlock_error_log = client.unlock()

        if unlock_error_log is None:
            common.show_info_message('Lock removed', ['Lock removed successfully.'])
        else:
            common.show_error_log('Lock removal failed', 'It was not possible to remove the lock.', unlock_error_log)

        return {'FINISHED'}

class PLASTIC_OT_show_history(Operator):
    bl_idname = 'plastic.show_history'
    bl_label = 'Show history'
    bl_description = 'Get detailed information about this history entry'

    date: StringProperty()
    owner: StringProperty()
    branch: StringProperty()
    changeset: StringProperty()
    comment: StringProperty()

    def execute(self, context):
        title = 'History entry detailed information'

        comments = []
        comments.append('Created: ' + self.date)
        comments.append('Owner: ' + self.owner)
        comments.append('Located on branch: ' + self.branch)
        comments.append('Changeset number: ' + self.changeset)
        comments.append(' ')

        if self.comment == '':
            comments.append('Comment: No comment')
        else:
            comment_lines = self.comment.split('\n')

            comments.append('Comment: ' + comment_lines[0])

            for extra_comment_line in comment_lines[1:]:
                comments.append(extra_comment_line)

        common.show_info_message(title, comments)

        return {'FINISHED'}

class PLASTIC_OT_reload_history(Operator):
    bl_idname = 'plastic.reload_history'
    bl_label = 'Reload history'
    bl_description = 'Reload the history for this file'

    def execute(self, context):
        history_error_log = client.load_history()

        if history_error_log is None:
            common.show_info_message('History reloaded', ['The file history was reloaded successfully.'])
        else:
            common.show_error_log('History failed', 'It was not possible to get the file history.', history_error_log)

        return {'FINISHED'}

class PLASTIC_OT_open_unity_documentation(Operator):
    bl_idname = 'plastic.open_unity_documentation'
    bl_label = 'PlasticSCM website'
    bl_description = 'Open the PlasticSCM documentation in Unity\'s website'

    def execute(self, context):
        bpy.ops.wm.url_open(url='https://unity.com/products/plastic-scm')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PLASTIC_OT_create_branch)
    bpy.utils.register_class(PLASTIC_OT_add_comment_line)
    bpy.utils.register_class(PLASTIC_OT_remove_comment_line)
    bpy.utils.register_class(PLASTIC_OT_checkin)
    bpy.utils.register_class(PLASTIC_OT_undo)
    bpy.utils.register_class(PLASTIC_OT_checkout)
    bpy.utils.register_class(PLASTIC_OT_lock)
    bpy.utils.register_class(PLASTIC_OT_unlock)
    bpy.utils.register_class(PLASTIC_OT_reload_history)
    bpy.utils.register_class(PLASTIC_OT_show_history)
    bpy.utils.register_class(PLASTIC_OT_open_unity_documentation)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_create_branch)
    bpy.utils.unregister_class(PLASTIC_OT_add_comment_line)
    bpy.utils.unregister_class(PLASTIC_OT_remove_comment_line)
    bpy.utils.unregister_class(PLASTIC_OT_checkin)
    bpy.utils.unregister_class(PLASTIC_OT_undo)
    bpy.utils.unregister_class(PLASTIC_OT_checkout)
    bpy.utils.unregister_class(PLASTIC_OT_lock)
    bpy.utils.unregister_class(PLASTIC_OT_unlock)
    bpy.utils.unregister_class(PLASTIC_OT_reload_history)
    bpy.utils.unregister_class(PLASTIC_OT_show_history)
    bpy.utils.unregister_class(PLASTIC_OT_open_unity_documentation)
