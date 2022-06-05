import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, StringProperty
import os

from .. import common
from ..plastic import client

class CommentLine(bpy.types.PropertyGroup):
    line: StringProperty(
        name='Including a comment is optional but recommended.',
        description='Keeping track of your changes is one of the greatest advantages of version control systems'
    )

class PlasticPanelSettings(PropertyGroup):
    def __get_branches(self, context):
        branches = []

        client_branches = client.get_branches()

        if client.get_active_branch() is None:
            branches.append(('-', '', ''))

        for branch_name in client_branches:
            branches.append((branch_name, branch_name, ''))

        return branches

    def __update_branch(plastic_context, self):
        selected_branch = plastic_context.branches

        if selected_branch != '-' and selected_branch != client.get_active_branch():
            switch_error_log = client.switch_to_branch(selected_branch)

            if switch_error_log is None:
                if os.path.exists(bpy.data.filepath):
                    bpy.ops.wm.revert_mainfile()
                else:
                    common.show_warning_message('Branch switched', ['The workspace was switched to a branch where the current file doesn\'t exist'])
            else:
                common.show_error_log('Branch switch failed', 'It was not possible to switch to the selected branch.', switch_error_log)

        return None

    info_menu_active: BoolProperty(default=True)
    pending_changes_menu_active: BoolProperty()
    checkout_menu_active: BoolProperty()
    branch_menu_active: BoolProperty()
    history_menu_active: BoolProperty()
    new_branch_name: StringProperty(
        name='Name of the new branch.'
    )
    is_child_branch: BoolProperty(
        description='Create the new branch under the current branch.\n\nEnabling this option will create the new branch as a child of the current branch.\nTake into account the select name will be concatenated to the name of the parent branch'
    )
    switch_branch: BoolProperty(
        description='Switch workspace to the new branch automatically after creation'
    )
    branches: EnumProperty(
        description='Select a branch to switch to',
        items=__get_branches,
        update=__update_branch,
        default=None
    )
    checkin_comments: CollectionProperty(type=CommentLine)


def register():
    bpy.utils.register_class(CommentLine)
    bpy.utils.register_class(PlasticPanelSettings)

    if not hasattr(bpy.types.WindowManager, 'plastic_context'):
        setattr(bpy.types.WindowManager, 'plastic_context', bpy.props.PointerProperty(type=PlasticPanelSettings))

def unregister():
    if hasattr(bpy.types.WindowManager, 'plastic_context'):
        delattr(bpy.types.WindowManager, 'plastic_context')

    bpy.utils.unregister_class(CommentLine)
    bpy.utils.unregister_class(PlasticPanelSettings)
