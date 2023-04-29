import bpy
from bpy.types import Operator
from bpy.props import IntProperty

from ... import common
from ...uvcs import client

class UVCS_OT_checkin(Operator):
    bl_idname = 'uvcs.checkin'
    bl_label = 'Checkin'
    bl_description = 'Submit checkin with the current changes'

    @classmethod
    def poll(cls, context):
        return client.has_changes_available()

    def execute(self, context):
        panel_settings = common.get_uvcs_context(context)

        comment_lines = []

        for checkin_comment in panel_settings.checkin_comments:
            comment_lines.append(checkin_comment.line)

        checkin_error_log = client.checkin('\n'.join(comment_lines))

        if checkin_error_log is None:
            panel_settings.checkin_comments.clear()
            panel_settings.pending_changes_menu_active = False

            common.show_info_message('Checkin completed', ['Checkin completed successfully.'])
        else:
            common.show_error_log('Checkin failed', 'It was not possible to complete the checkin.', checkin_error_log)

        return {'FINISHED'}

class UVCS_OT_add_comment_line(Operator):
    bl_idname = 'uvcs.add_comment_line'
    bl_label = 'Add line'
    bl_description = 'Add a new comment line'

    def execute(self, context):
        panel_settings = common.get_uvcs_context(context)

        comment_line = panel_settings.checkin_comments.add()
        comment_line.line = ''

        return {'FINISHED'}

class UVCS_OT_remove_comment_line(Operator):
    bl_idname = 'uvcs.remove_comment_line'
    bl_label = 'Remove line'
    bl_description = 'Remove this comment line'

    index: IntProperty()

    def execute(self, context):
        panel_settings = common.get_uvcs_context(context)

        if len(panel_settings.checkin_comments) >= (self.index + 1):
            panel_settings.checkin_comments.remove(self.index)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(UVCS_OT_checkin)
    bpy.utils.register_class(UVCS_OT_add_comment_line)
    bpy.utils.register_class(UVCS_OT_remove_comment_line)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_checkin)
    bpy.utils.unregister_class(UVCS_OT_add_comment_line)
    bpy.utils.unregister_class(UVCS_OT_remove_comment_line)
