import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from ... import common
from ...uvcs import client

class UVCS_OT_update(Operator):
    bl_idname = 'uvcs.update'
    bl_label = 'Update'
    bl_description = 'Update to latest version'

    @classmethod
    def poll(cls, context):
        return client.has_incoming_changes()

    def execute(self, context):
        update_error_log = client.update()

        if update_error_log is None:
            bpy.ops.wm.revert_mainfile()
        else:
            common.show_error_log('Update failed', 'It was not possible to update the file.', update_error_log)

        return {'FINISHED'}

class UVCS_OT_changeset_details(Operator):
    bl_idname = 'uvcs.changeset_details'
    bl_label = 'Show changeset details'
    bl_description = 'Get detailed information about this changeset'

    date: StringProperty()
    owner: StringProperty()
    branch: StringProperty()
    changeset: StringProperty()
    comment: StringProperty()

    def execute(self, context):
        title = 'Changeset detailed information'

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


def register():
    bpy.utils.register_class(UVCS_OT_update)
    bpy.utils.register_class(UVCS_OT_changeset_details)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_update)
    bpy.utils.unregister_class(UVCS_OT_changeset_details)
