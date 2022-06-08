import re

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
__mount_point = None

class FileStatus():
    repository = None
    server = None
    status = None

class MountPoint():
    name = None
    changeset = None
    head = None

def get_server(): return __file_status.server if __file_status is not None else None

def get_repository(): return __file_status.repository if __file_status is not None else None

def has_changes_available(): return __file_status is not None and __file_status.status is not None

def is_checked_out(): return __file_status is not None and __file_status.status == 'CO'

def get_mount_point(): return __mount_point.name if __mount_point is not None else None

def get_current_changeset(): return __mount_point.changeset if __mount_point is not None else None

def has_incoming_changes(): return __mount_point is not None and __mount_point.changeset != __mount_point.head

def get_status():
    file_status = __file_status.status

    if file_status is None:
        return 'No changes'

    return __STATUSES[file_status] if file_status in __STATUSES else 'Unknown (' + file_status + ')'

def load_status():
    global __file_status
    __file_status = None

    command_result = command.file_status()

    if not command_result.success:
        return False

    status_output = command_result.output

    __file_status = FileStatus()
    __file_status.repository = __extract_repository_from_status(status_output)
    __file_status.server = __extract_server_from_status(status_output)
    __file_status.status = __extract_changes_from_status(status_output)

    return True

def __extract_repository_from_status(status_output):
    item_info = status_output[0].split(' ')

    return item_info[2] if len(item_info) > 2 else None

def __extract_server_from_status(status_output):
    item_info = status_output[0].split(' ')

    return item_info[3] if len(item_info) > 3 else None

def __extract_changes_from_status(status_output):
    if len(status_output) > 1:
        return status_output[1].split(' ')[0]

    return None

def load_mount_point():
    global __mount_point
    __mount_point = None

    command_result = command.file_status_header()

    if command_result.success:
        header_line = command_result.output[0]

        __mount_point = MountPoint()
        __mount_point.name = header_line.split('@')[0]
        __mount_point.changeset = __extract_changeset_from_header(header_line)
        __mount_point.head = __extract_head_from_header(header_line)

def __extract_changeset_from_header(header_line):
    found_changeset = re.search('cs:(\d+)', header_line)

    if found_changeset is not None and len(found_changeset.groups()) >= 1:
        return int(found_changeset.group(1))

    return None

def __extract_head_from_header(header_line):
    found_head = re.search('head:(\d+)', header_line)

    if found_head is not None and len(found_head.groups()) >= 1:
        return int(found_head.group(1))

    return __mount_point.changeset

def clear_status_cache():
    global __file_status
    __file_status = None

def clear_mount_point_cache():
    global __mount_point
    __mount_point = None
