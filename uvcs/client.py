import bpy

from .. import common
from .operations import branch as branch_operations
from .operations import checkin as checkin_operations
from .operations import checkout as checkout_operations
from .operations import history as history_operations
from .operations import location as location_operations
from .operations import status as status_operations
from .operations import update as update_operations

__initialized = False
__connected = False

def is_connected():
    global __initialized

    if not __initialized:
        __initialized = True

        addon_preferences = common.get_addon_preferences(bpy.context)

        set_cm_location(addon_preferences.uvcs_cm_path)

        if bpy.data.filepath != '':
            refresh_status()

    return __connected

def set_cm_location(path): location_operations.set_cm_location(path)

def has_changes_available(): return status_operations.has_changes_available()

def has_incoming_changes(): return status_operations.has_incoming_changes()

def refresh_status():
    global __initialized, __connected
    __initialized = True
    __connected = status_operations.load_status()

def refresh_file_info():
    refresh_status()

    if not __connected: return

    status_operations.load_file_info()

    mount_point = status_operations.get_mount_point()

    if mount_point is not None and mount_point.startswith('/'):
        branch_operations.set_active_branch(mount_point)

def get_status():
    if not __connected:
        return 'Not connected'

    return status_operations.get_status() if status_operations.has_changes_available() else 'No changes'

def is_private(): return status_operations.is_private()

def is_local_file(): return status_operations.is_local_file()

def get_repository_spec(): return status_operations.get_repository() + '@' + status_operations.get_server()

def get_mount_point():
    mount_point = status_operations.get_mount_point()

    if not mount_point.startswith('cs:'):
        current_changeset = status_operations.get_current_changeset()

        if current_changeset is not None:
            mount_point += ' (cs:' + str(current_changeset) + ')'

    return mount_point

def get_active_branch(): return branch_operations.get_active_branch()

def add():
    add_error_log = checkout_operations.add()

    if add_error_log is None:
        refresh_file_info()

    return add_error_log

def get_branches(): return branch_operations.get_branches()

def switch_to_branch(branch_name):
    switch_error_log = branch_operations.switch_to_branch(branch_name)

    if switch_error_log is None:
        refresh_file_info()

    return switch_error_log

def create_branch(branch_name): return branch_operations.create_branch(branch_name)

def checkin(comment):
    checkin_error_log = checkin_operations.checkin(comment)

    if checkin_error_log is None:
        checkout_operations.clear_cache()
        history_operations.clear_cache()
        refresh_file_info()

    return checkin_error_log

def undo():
    undo_error_log = checkin_operations.undo()

    if undo_error_log is None:
        refresh_status()

    return undo_error_log

def get_incoming_changes(): return update_operations.get_incoming_changes(status_operations.get_current_changeset())

def update(): return update_operations.update()

def is_checked_out(): return status_operations.is_checked_out()

def checkout():
    checkout_error_log = checkout_operations.checkout()

    if checkout_error_log is None:
        refresh_status()

    return checkout_error_log

def get_lock_info(): return checkout_operations.get_lock_info()

def unlock(): return checkout_operations.unlock()

def load_history(): return history_operations.load_history()

def get_history(): return history_operations.get_history()

def clear_cache():
    global __initialized
    __initialized = False

    status_operations.clear_status_cache()
    branch_operations.clear_cache()
    checkout_operations.clear_cache()
    update_operations.clear_cache()
    history_operations.clear_cache()
