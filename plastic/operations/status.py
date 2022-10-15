import bpy
import re

from . import command
from ... import common

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

class MountPoint():
    name = None
    changeset = None
    head = None

class FileInfo():
    repository = None
    server = None
    status = None
    mount_point = MountPoint()

__file_info = FileInfo()

def get_server(): return __file_info.server

def get_repository(): return __file_info.repository

def has_changes_available(): return __file_info.status is not None

def is_checked_out(): return __file_info.status == 'CO'

def get_mount_point(): return __file_info.mount_point.name

def get_current_changeset(): return __file_info.mount_point.changeset

def has_incoming_changes(): return __file_info.mount_point.changeset != __file_info.mount_point.head

def get_status():
    file_status = __file_info.status

    if file_status is None:
        return 'No changes'

    return __STATUSES[file_status] if file_status in __STATUSES else 'Unknown (' + file_status + ')'

def load_status():
    command_result = command.execute(['status', '--machinereadable', common.quote(bpy.data.filepath)])

    if not command_result.success:
        return False

    __file_info.status = __extract_status_from_status_output(command_result.output)

    return True

def __extract_status_from_status_output(status_output):
    if len(status_output) > 1:
        return status_output[1].split(' ')[0]

    return None

def load_file_info():
    global __file_info
    __file_info.mount_point = MountPoint()

    command_result = command.execute(['status', '--header', common.quote(bpy.data.filepath)])

    if command_result.success:
        header_line = command_result.output[0]

        __file_info.repository = __extract_repository_from_header(header_line)
        __file_info.server = __extract_server_from_header(header_line)

        __file_info.mount_point.name = header_line.split('@')[0]
        __file_info.mount_point.changeset = __extract_changeset_from_header(header_line)
        __file_info.mount_point.head = __extract_head_from_header(header_line)

def __extract_repository_from_header(header_line):
    item_info = header_line.split(' ')[0]

    return item_info.split('@')[1]

def __extract_server_from_header(header_line):
    item_info = header_line.split(' ')[0]

    return item_info.split('@')[2]

def __extract_changeset_from_header(header_line):
    found_changeset = re.search('cs:(\d+)', header_line)

    if found_changeset is not None and len(found_changeset.groups()) >= 1:
        return int(found_changeset.group(1))

    return None

def __extract_head_from_header(header_line):
    found_head = re.search('head:(\d+)', header_line)

    if found_head is not None and len(found_head.groups()) >= 1:
        return int(found_head.group(1))

    return __file_info.mount_point.changeset

def clear_status_cache():
    global __file_info
    __file_info = FileInfo()
