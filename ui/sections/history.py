from .. import icons
from ...plastic import client

def draw(layout, panel_settings):
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

                op = row.operator('plastic.changeset_details', text='', icon='HIDE_OFF', emboss=False, translate=False)
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

