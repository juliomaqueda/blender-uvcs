import bpy
from bpy.types import Operator
import os

from ... import common
from ...uvcs import client

class UVCS_OT_create_branch(Operator):
    bl_idname = 'uvcs.create_branch'
    bl_label = 'Create branch'
    bl_description = 'Create a new branch with the supplied name'

    @classmethod
    def poll(cls, context):
        panel_settings = common.get_uvcs_context(context)
        return panel_settings.new_branch_name != ''

    def execute(self, context):
        panel_settings = common.get_uvcs_context(context)
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
                    if not os.path.exists(bpy.data.filepath):
                        common.show_warning_message('Branch switched', ['The workspace was switched to a branch where the current file doesn\'t exist'])
                else:
                    common.show_error_log('Branch switch failed', 'Although the new branch was created successfully, it was not possible to switch to it.', switch_error_log)
            else:
                common.show_info_message('Branch creation completed', ['The new branch ' + branch_name + ' was created successfully'])
        else:
            common.show_error_log('Branch creation failed', create_branch_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(UVCS_OT_create_branch)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_create_branch)
