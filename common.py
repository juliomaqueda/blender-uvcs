import bpy

ADDON_NAME = 'blender-plasticscm'

def get_addon_preferences(context):
    return context.preferences.addons[ADDON_NAME].preferences

def get_plastic_context(context):
    return context.window_manager.plastic_context

def show_info_message(title, messages):
    __show_message(title, messages, 'INFO')

def show_warning_message(title, messages):
    __show_message(title, messages, 'ERROR')

def show_error_message(title, messages):
    __show_message(title, messages, 'CANCEL')

def show_error_log(title, message, log):
    messages = [message, ' ', 'PlasticSCM output:']

    for log_line in log:
        messages.append('> ' + log_line)

    __show_message(title, messages, 'CANCEL')

def __show_message(title, messages, icon='INFO'):
    def draw(self, context):
        layout = self.layout

        for message in messages:
            for limited_line in __limit_line_chars(message):
                layout.label(text=limited_line, translate=False)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def __limit_line_chars(line_text):
    max_chars = 100

    limited_lines = []

    line_words = line_text.split(' ')

    i = 0
    line_text = ''

    while i < len(line_words):
        if len(line_text) < max_chars:
            line_text += (line_words[i] + ' ')
            i += 1
        else:
            limited_lines.append(line_text)
            line_text = ''

    limited_lines.append(line_text)

    return limited_lines
