from . import add, branch, checkin, checkout, documentation, history, lock, undo, update

def register():
    add.register()
    branch.register()
    checkin.register()
    checkout.register()
    documentation.register()
    history.register()
    lock.register()
    undo.register()
    update.register()

def unregister():
    add.unregister()
    branch.unregister()
    checkin.unregister()
    checkout.unregister()
    documentation.unregister()
    history.unregister()
    lock.unregister()
    undo.unregister()
    update.unregister()
