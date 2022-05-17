from . import command

__LOCK_FIELD_SEPARATOR = ','

__lock_owner = None
__locked_file_guid = None
__lock_loaded = False

def __load_active_lock():
    global __lock_owner, __locked_file_guid
    __lock_owner = None
    __locked_file_guid = None

    lock_result = command.get_lock(__LOCK_FIELD_SEPARATOR)

    if lock_result.success and lock_result.output[0] != '':
        lock_info = lock_result.output[0].split(__LOCK_FIELD_SEPARATOR)

        if len(lock_info) == 4:
            __lock_owner = lock_info[1]
            __locked_file_guid = lock_info[0]

def checkout():
    command_result = command.checkout()

    if command_result.success:
        __load_active_lock()

    return None if command_result.success else command_result.output

def undo_checkout():
    command_result = command.undo_checkout()

    if command_result.success:
        __load_active_lock()

    return None if command_result.success else command_result.output

def get_lock_owner():
    global __lock_loaded

    if not __lock_loaded:
        __lock_loaded = True
        __load_active_lock()

    return __lock_owner

def unlock():
    command_result = command.unlock(__locked_file_guid)

    if command_result.success:
        clear_cache()

    return None if command_result.success else command_result.output

def clear_cache():
    global __lock_owner, __locked_file_guid, __lock_loaded
    __lock_owner = None
    __locked_file_guid = None
    __lock_loaded = False
