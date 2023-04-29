from ...uvcs import client

def draw(layout, panel_settings):
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
                row.operator('uvcs.add_comment_line', text='', icon='ADD', translate=False)

                if comment_index != 0:
                    row.operator('uvcs.remove_comment_line', text='', icon='PANEL_CLOSE', translate=False).index = comment_index
            else:
                row.operator('uvcs.remove_comment_line', text='', icon='PANEL_CLOSE', translate=False).index = comment_index

        row = box.row()

        row.operator('uvcs.checkin', text='Checkin', icon='EXPORT', translate=False)
        row.operator('uvcs.undo', text='Undo changes', icon='LOOP_BACK', translate=False)
