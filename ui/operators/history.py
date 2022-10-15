import bpy
from bpy.types import Operator

from ... import common
from ...plastic import client

class PLASTIC_OT_reload_history(Operator):
    bl_idname = 'plastic.reload_history'
    bl_label = 'Reload history'
    bl_description = 'Reload the history for this file'

    def execute(self, context):
        history_error_log = client.load_history()

        if history_error_log is None:
            common.show_info_message('History reloaded', ['The file history was reloaded successfully.'])
        else:
            common.show_error_log('History failed', 'It was not possible to get the file history.', history_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PLASTIC_OT_reload_history)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_reload_history)
