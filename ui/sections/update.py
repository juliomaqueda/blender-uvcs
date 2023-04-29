from ...uvcs import client

def draw(layout, panel_settings):
    row = layout.row()
    row.enabled = client.has_incoming_changes()

    incoming_changes_text = 'Incoming changes' if client.has_incoming_changes() else 'No incoming changes'
    icon = 'DOWNARROW_HLT' if panel_settings.incoming_changes_menu_active else 'RIGHTARROW'
    row.prop(panel_settings, 'incoming_changes_menu_active', text=incoming_changes_text, icon=icon, translate=False)

    if panel_settings.incoming_changes_menu_active:
        box = layout.box()

        row = box.row()
        row.label(text='There are incoming changes available', icon='ERROR', translate=False)

        if panel_settings.show_incoming_changes:
            incoming_changes = client.get_incoming_changes()

            if incoming_changes is not None:
                for incoming_change_entry in incoming_changes:
                    row = box.row()

                    col_changeset = row.split()
                    col_changeset.scale_x = 0.5
                    col_changeset.label(text=incoming_change_entry.changeset, translate=False)

                    col_date = row.split()
                    col_date.scale_x = 1.2
                    col_date.label(text=incoming_change_entry.date, translate=False)

                    row.label(text=incoming_change_entry.owner, translate=False)

                    op = row.operator('uvcs.changeset_details', text='', icon='HIDE_OFF', emboss=False, translate=False)
                    op.date = incoming_change_entry.date
                    op.owner = incoming_change_entry.owner
                    op.branch = incoming_change_entry.branch
                    op.changeset = incoming_change_entry.changeset
                    op.comment = incoming_change_entry.comment
            else:
                row = box.row()
                row.enabled = False
                row.label(text='Couldn\'t get the incoming changes', translate=False)

        row = box.row()
        row.prop(panel_settings, 'show_incoming_changes', text='View changes', icon='HIDE_OFF', translate=False)
        row.operator('uvcs.update', text='Update', icon='IMPORT', translate=False)
