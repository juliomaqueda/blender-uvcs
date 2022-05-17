from . import command

__STATUSES = {
    'AD': 'Added',
    'CO': 'Checked-out',
    'CP': 'Copied',
    'RP': 'Replaced',
    'MV': 'Moved',
    'DE': 'Deleted',
    'CH': 'Changed locally',
    'LD': 'Deleted locally',
    'LM': 'Moved locally',
    'PR': 'Private',
    'IG': 'Ignored'
}

__file_status = None

class FileStatus():
    repository = None
    server = None
    status = None
    mount_point = None

def get_server(): return __file_status.server if __file_status is not None else None

def get_repository(): return __file_status.repository if __file_status is not None else None

def get_mount_point(): return __file_status.mount_point if __file_status is not None else None

def has_changes_available(): return __file_status is not None and __file_status.status is not None

def is_checked_out(): return __file_status is not None and __file_status.status == 'CO'

def get_status():
    file_status = __file_status.status

    if file_status is None:
        return 'No changes'

    return __STATUSES[file_status] if file_status in __STATUSES else 'Unknown (' + file_status + ')'

def load_status():
    global __file_status, __server, __repository, __status

    command_result = command.file_status()

    if not command_result.success:
        return False

    __file_status = FileStatus()

    status_output = command_result.output

    item_info = status_output[0].split(' ')

    if len(item_info) > 2:
        __file_status.repository = item_info[2]

    if len(item_info) > 3:
        __file_status.server = item_info[3]

    if len(status_output) > 1:
        __file_status.status = status_output[1].split(' ')[0]

    return True

def load_mount_point():
    command_result = command.file_status_header()

    if command_result.success:
        mount_point = command_result.output[0].split('@')[0]
        __file_status.mount_point = mount_point

        return mount_point

    return None

def clear_cache():
    global __file_status
    __file_status = None
