import bpy

def get_addon_preferences(context):
    return context.preferences.addons['plasticscm'].preferences

def get_plastic_context(context):
    return context.window_manager.plastic_context

def show_info_message(title, messages):
    __show_message(title, messages, 'INFO')

def show_warning_message(title, messages):
    __show_message(title, messages, 'ERROR')

def show_error_message(title, messages):
    __show_message(title, messages, 'CANCEL')

def __show_message(title, messages, icon='INFO'):
    def draw(self, context):
        layout = self.layout

        for message in messages:
            message_lines = message.split('\n')

            for message_line in message_lines:
                row = layout.row()
                row.alignment = 'LEFT'
                row.label(text=message_line, translate=False)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def show_error_log(title, message, log):
    def draw(self, context):
        layout = self.layout
        layout.label(text=message, translate=False)

        layout.label(text=' ', translate=False)
        layout.label(text='Console output:', translate=False)

        for log_line in log:
            layout.label(text='> ' + log_line, translate=False)

    bpy.context.window_manager.popup_menu(draw, title=title, icon='CANCEL')
