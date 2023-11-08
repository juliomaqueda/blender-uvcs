import bpy

from . import command
from ..models import lock
from ... import common

__LOCK_FIELD_SEPARATOR = ','

__lock_info = None
__lock_loaded = False

def __load_active_lock():
    global __lock_info
    __lock_info = None

    lock_result = command.execute([
        'lock',
        'list',
        '--machinereadable',
        '--anystatus',
        '--smartlocks',
        '--fieldseparator=' + __LOCK_FIELD_SEPARATOR,
        common.quote(bpy.data.filepath)
    ])

    if lock_result.success and lock_result.output[0] != '':
        lock_info = lock_result.output[0].split(__LOCK_FIELD_SEPARATOR)

        if len(lock_info) == 12:
            __lock_info = lock.LockEntry(
                lock_info[2],
                lock_info[9],
                lock_info[6],
                lock_info[8]
            )

def add():
    command_result = command.execute(['add', '--silent', common.quote(bpy.data.filepath)])

    return None if command_result.success else command_result.output

def checkout():
    command_result = command.execute(['checkout', '--silent', common.quote(bpy.data.filepath)])

    if command_result.success:
        __load_active_lock()

    return None if command_result.success else command_result.output

def get_lock_info():
    global __lock_loaded

    if not __lock_loaded:
        __lock_loaded = True
        __load_active_lock()

    return __lock_info

def unlock():
    if __lock_info is not None:
        command_result = command.execute(['lock', 'unlock', __lock_info.guid])

        if command_result.success:
            clear_cache()

        return None if command_result.success else command_result.output

    clear_cache()

    return None

def clear_cache():
    global __lock_info, __lock_loaded
    __lock_info = None
    __lock_loaded = False
