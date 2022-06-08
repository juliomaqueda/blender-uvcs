from . import command
from ..models import changeset

__HISTORY_FORMAT_SEPARATOR = '#_#'

__history_entries = None
__history_loaded = False

def get_history():
    global __history_loaded

    if not __history_loaded:
        __history_loaded = True
        load_history()

    return __history_entries

def load_history():
    global __history_entries
    __history_entries = None

    command_result = command.get_history(__HISTORY_FORMAT_SEPARATOR)

    if command_result.success:
        __history_entries = []

        command_result.output.reverse()

        __populate_history(command_result.output)

    return None if command_result.success else command_result.output

def __populate_history(history_output):
    for history_line in history_output:
        history_info = history_line.split(__HISTORY_FORMAT_SEPARATOR)

        if len(history_info) == 4:
            history_info.append('')

        if len(history_info) == 5:
            __history_entries.append(changeset.ChangesetEntry(
                history_info[0],
                history_info[1],
                history_info[2],
                history_info[3],
                history_info[4]
            ))

def clear_cache():
    global __history_entries, __history_loaded
    __history_entries = None
    __history_loaded = False
