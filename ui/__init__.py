from . import icons, handlers, operators, panel, preferences, settings, toolbar

def register():
    icons.register()
    handlers.register()
    operators.register()
    panel.register()
    preferences.register()
    settings.register()
    toolbar.register()

def unregister():
    icons.unregister()
    handlers.unregister()
    operators.unregister()
    panel.unregister()
    preferences.unregister()
    settings.unregister()
    toolbar.unregister()
