from .. import icons
from ...uvcs import client

def draw(layout, panel_settings):
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
        row.operator('uvcs.create_branch', text='', icon_value=icons.get_icon('CREATE'), translate=False)
        col.separator()
        row = col.row()

        if active_branch is not None:
            row.prop(panel_settings, 'is_child_branch', text='Is child branch?', translate=False)

        row.prop(panel_settings, 'switch_branch', text='Auto-switch', translate=False)
