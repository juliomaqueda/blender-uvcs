import bpy

from .. import common
from .operations import branch as branch_operations
from .operations import checkin as checkin_operations
from .operations import checkout as checkout_operations
from .operations import history as history_operations
from .operations import location as location_operations
from .operations import status as status_operations

__initialized = False
__connected = False

def is_connected():
    global __initialized

    if not __initialized:
        __initialized = True

        addon_preferences = common.get_addon_preferences(bpy.context)

        set_cm_location(addon_preferences.plastic_cm_path)

        if bpy.data.filepath != '':
            refresh_status()

    return __connected

def set_cm_location(path): location_operations.set_cm_location(path)

def has_changes_available(): return status_operations.has_changes_available()

def refresh_status():
    status_operations.clear_cache()

    global __initialized, __connected
    __initialized = True
    __connected = status_operations.load_status()

def refresh_info():
    refresh_status()

    if __connected:
        mount_point = status_operations.load_mount_point()

        if mount_point.startswith('/'):
            branch_operations.set_active_branch(mount_point)

def get_status():
    if not __connected:
        return 'Not connected'

    return status_operations.get_status() if status_operations.has_changes_available() else 'No changes'

def get_repository_spec(): return status_operations.get_repository() + '@' + status_operations.get_server()

def get_mount_point(): return status_operations.get_mount_point()

def get_active_branch(): return branch_operations.get_active_branch()

def get_branches(): return branch_operations.get_branches()

def switch_to_branch(branch_name): return branch_operations.switch_to_branch(branch_name)

def create_branch(branch_name): return branch_operations.create_branch(branch_name)

def checkin(comment): return checkin_operations.checkin(comment)

def is_checked_out(): return status_operations.is_checked_out()

def checkout(): return checkout_operations.checkout()

def undo_checkout(): return checkout_operations.undo_checkout()

def get_lock_owner(): return checkout_operations.get_lock_owner()

def unlock(): return checkout_operations.unlock()

def load_history(): return history_operations.load_history()

def get_history(): return history_operations.get_history()

def clear_cache():
    global __initialized
    __initialized = False

    status_operations.clear_cache()
    branch_operations.clear_cache()
    checkout_operations.clear_cache()
    history_operations.clear_cache()
