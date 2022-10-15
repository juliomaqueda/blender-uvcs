import bpy
from bpy.types import Operator

from ... import common
from ...plastic import client

class PLASTIC_OT_undo(Operator):
    bl_idname = 'plastic.undo'
    bl_label = 'Undo changes'
    bl_description = 'Undo the current changes'

    @classmethod
    def poll(cls, context):
        return client.has_changes_available()

    def execute(self, context):
        undo_error_log = client.undo()

        if undo_error_log is None:
            bpy.ops.wm.revert_mainfile()
        else:
            common.show_error_log('Undo failed', 'It was not possible to undo the changes.', undo_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PLASTIC_OT_undo)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_undo)
