import bpy
import os
import subprocess

__cm_command_path = None

class CommandResult():
    success = False
    output = []

    def __init__(self, succeded, output):
        self.success = succeded
        self.output = output

def __execute(params, newline_separator = None):
    command_arguments = [__cm_command_path]
    command_arguments += params

    try:
        p = subprocess.Popen(
            command_arguments,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            cwd = __get_command_cwd()
        )

        output_data = p.communicate()[0]

        return CommandResult(p.returncode == 0, __format_output(output_data, newline_separator))
    except BaseException:
        return CommandResult(False, ['Couldn\'t execute command ' + __cm_command_path])

def __get_command_cwd():
    command_cwd = None

    if hasattr(bpy.data, 'filepath'):
        command_cwd = os.path.dirname(os.path.realpath(bpy.data.filepath))

    return command_cwd

def __format_output(output, newline_separator):
    line_separator = newline_separator + '\n' if newline_separator is not None else '\n'

    return output \
        .decode('utf-8') \
        .replace('\r', '') \
        .rstrip(line_separator) \
        .split(line_separator)

def set_cm_location(path):
    global __cm_command_path
    __cm_command_path = path

def file_status():
    return __execute(['status', '--machinereadable', bpy.data.filepath])

def file_status_header():
    return __execute(['status', '--header', bpy.data.filepath])

def get_relative_path():
    return __execute(['fileinfo', '--format={RelativePath}', bpy.data.filepath])

def get_branches():
    return __execute(['find', 'branches', '--format={name}', '--nototal'])

def switch_to_branch(branch_name):
    return __execute(['switch', branch_name])

def create_branch(branch_name):
    return __execute(['branch', 'create', branch_name])

def checkin(comment):
    params = ['checkin', '--all', '--private']

    if comment is not None and comment != '':
        params.append('-c')
        params.append(comment)

    params.append(bpy.data.filepath)

    return __execute(params)

def checkout():
    return __execute(['checkout', '--silent', bpy.data.filepath])

def undo():
    return __execute(['undo', '--silent', bpy.data.filepath])

def get_lock(field_separator):
    return __execute(['lock', 'list', '--machinereadable', '--fieldseparator=' + field_separator, bpy.data.filepath])

def unlock(guid):
    return __execute(['lock', 'unlock', guid])

def get_history(format_separator: str):
    history_fields = ['{date}', '{owner}', '{branch}', '{changesetid}', '{comment}']

    return __execute(['history', '--format=' + format_separator.join(history_fields) + '#__#', bpy.data.filepath], '#__#')
