from ...uvcs import client

def draw(layout, panel_settings):
    row = layout.row()
    icon = 'DOWNARROW_HLT' if panel_settings.checkout_menu_active else 'RIGHTARROW'
    row.prop(panel_settings, 'checkout_menu_active', text='Checkout / Locking', icon=icon, translate=False)

    if panel_settings.checkout_menu_active:
        lock_info = client.get_lock_info()

        box = layout.box()

        row = box.row()
        row.label(text='Checkout status: ' + ('Checked-out' if client.is_checked_out() else 'Not checked-out'), translate=False)

        if lock_info is not None:
            row = box.row()
            row.label(text='Lock status: ' + lock_info.type, translate=False)

            row = box.row()
            row.label(text='Lock owner: ' + lock_info.owner, translate=False)

            row = box.row()
            row.label(text='Lock branch: ' + lock_info.branch, translate=False)
        else:
            row = box.row()
            row.label(text='Lock status: Not locked', translate=False)

        row = box.row()

        row.operator('uvcs.checkout', text='Checkout' if not client.is_checked_out() else 'Checked-out', icon='IMPORT', translate=False)

        if lock_info is not None:
            row.operator('uvcs.unlock', text='Unlock', icon='UNLOCKED', translate=False)
        else:
            row.operator('uvcs.lock', text='Lock', icon='LOCKED', translate=False)
