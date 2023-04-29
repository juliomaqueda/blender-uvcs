import bpy
from bpy.types import Operator

from ... import common
from ...uvcs import client

class UVCS_OT_checkout(Operator):
    bl_idname = 'uvcs.checkout'
    bl_label = 'Checkout'
    bl_description = 'Checkout the file'

    @classmethod
    def poll(cls, context):
        return not client.is_checked_out()

    def execute(self, context):
        checkout_error_log = client.checkout()

        if checkout_error_log is not None:
            common.show_error_log('Checkout failed', 'It was not possible to complete the checkout.', checkout_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(UVCS_OT_checkout)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_checkout)
