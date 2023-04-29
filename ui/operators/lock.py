import bpy
from bpy.types import Operator

from ... import common
from ...uvcs import client

class UVCS_OT_lock(Operator):
    bl_idname = 'uvcs.lock'
    bl_label = 'Lock'
    bl_description = 'Lock the current file'

    def execute(self, context):
        checkout_error_log = client.checkout()

        if checkout_error_log is None:
            if client.get_lock_owner() is None:
                common.show_error_message('Lock failed', ['The current file doesn\'t meet the locking criteria.'])
        else:
            common.show_error_log('Checkout failed', 'It was not possible to checkout the file.', checkout_error_log)

        return {'FINISHED'}

class UVCS_OT_unlock(Operator):
    bl_idname = 'uvcs.unlock'
    bl_label = 'Unlock'
    bl_description = 'Remove the current lock'

    def execute(self, context):
        unlock_error_log = client.unlock()

        if unlock_error_log is not None:
            common.show_error_log('Lock removal failed', 'It was not possible to remove the lock.', unlock_error_log)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(UVCS_OT_lock)
    bpy.utils.register_class(UVCS_OT_unlock)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_lock)
    bpy.utils.unregister_class(UVCS_OT_unlock)
