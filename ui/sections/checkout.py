from ...plastic import client

def draw(layout, panel_settings):
    row = layout.row()
    icon = 'DOWNARROW_HLT' if panel_settings.checkout_menu_active else 'RIGHTARROW'
    row.prop(panel_settings, 'checkout_menu_active', text='Checkout / Locking', icon=icon, translate=False)

    if panel_settings.checkout_menu_active:
        box = layout.box()

        row = box.row()
        row.label(text='Checkout status: ' + ('Checked-out' if client.is_checked_out() else 'Not checked-out'), translate=False)

        row = box.row()
        row.label(text='Lock status: ' +  ('Locked' if client.get_lock_owner() is not None else 'Not locked'), translate=False)

        if client.get_lock_owner() is not None:
            row = box.row()
            row.label(text='Lock owner: ' + client.get_lock_owner(), translate=False)

        row = box.row()

        row.operator('plastic.checkout', text='Checkout' if not client.is_checked_out() else 'Checked-out', icon='IMPORT', translate=False)

        if client.get_lock_owner() is not None:
            row.operator('plastic.unlock', text='Unlock', icon='UNLOCKED', translate=False)
        else:
            row.operator('plastic.lock', text='Lock', icon='LOCKED', translate=False)
