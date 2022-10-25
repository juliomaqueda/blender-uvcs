import bpy
from bpy.types import Operator

from ... import common
from ...plastic import client

class PLASTIC_OT_add(Operator):
    bl_idname = 'plastic.add'
    bl_label = 'Add file to source control'
    bl_description = 'Add file to source control'

    @classmethod
    def poll(cls, context):
        return client.is_private()

    def execute(self, context):
        add_error_log = client.add()

        if add_error_log is not None:
            common.show_error_log('Add to source control failed', 'It was not possible to add the current file to source control.', add_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PLASTIC_OT_add)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_add)
