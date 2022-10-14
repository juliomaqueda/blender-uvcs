import bpy
import os
import re
import subprocess

__cm_command_path = None
__cm_shell_process = None

class CommandResult():
    success = False
    output = []

    def __init__(self, succeded, output):
        self.success = succeded
        self.output = output

def __execute(params, newline_separator = None):
    try:
        if __cm_shell_process is None:
            __initialize_plastic_shell()

        cm_command = ' '.join(params) + "\n"

        __cm_shell_process.stdin.write(cm_command)

        command_output = ''
        command_return_code = 1

        while True:
            __cm_shell_process.stdin.flush()
            output_line = __cm_shell_process.stdout.readline()

            if 'CommandResult' in output_line:
                command_return_code = __extract_command_result_code(output_line)
                break

            if output_line != '':
                command_output += output_line

        return CommandResult(command_return_code == 0, __format_output(command_output, newline_separator))
    except BaseException as ex:
        return CommandResult(False, ['Couldn\'t execute command ' + __cm_command_path])

def __initialize_plastic_shell():
    global __cm_shell_process

    __cm_shell_process = subprocess.Popen(
        [__cm_command_path, 'shell'],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        cwd = __get_command_cwd(),
        encoding = 'utf8')

def __get_command_cwd():
    command_cwd = None

    if hasattr(bpy.data, 'filepath'):
        command_cwd = os.path.dirname(os.path.realpath(bpy.data.filepath))

    return command_cwd

def __extract_command_result_code(output_line):
    match = re.search('CommandResult (\d)\n', output_line)

    if match:
        return int(match.group(1))

    return None

def __format_output(output, newline_separator):
    line_separator = newline_separator + '\n' if newline_separator is not None else '\n'

    return output \
        .replace('\r', '') \
        .rstrip(line_separator) \
        .split(line_separator)

def __quote(text):
    return '"' + text + '"'

def set_cm_location(path):
    global __cm_command_path, __cm_shell_process

    __cm_command_path = path

    if __cm_shell_process is not None:
        __cm_shell_process.terminate()
        __cm_shell_process = None

def file_status():
    return __execute(['status', '--machinereadable', __quote(bpy.data.filepath)])

def file_status_header():
    return __execute(['status', '--header', __quote(bpy.data.filepath)])

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
        params.append(__quote(comment))

    params.append(__quote(bpy.data.filepath))

    return __execute(params)

def checkout():
    return __execute(['checkout', '--silent', __quote(bpy.data.filepath)])

def undo():
    return __execute(['undo', '--silent', __quote(bpy.data.filepath)])

def get_changeset_branch(changeset):
    return __execute([
        'find',
        'changeset',
        'where changesetid = ' + str(changeset),
        '--format={branch}',
        '--nototal'
    ])

def get_incoming_changes(changeset, changeset_branch, format_separator):
    incoming_changes_fields = ['{date}', '{owner}', '{branch}', '{changesetid}', '{comment}']

    return __execute([
        'find',
        'changeset',
        'where changesetid > ' + str(changeset) + ' and branch = "' + changeset_branch + '"',
        '--format=' + format_separator.join(incoming_changes_fields) + '#__#',
        '--nototal'
    ], '#__#')

def update():
    return __execute(['update', '--silent'])

def get_lock(field_separator):
    return __execute([
        'lock',
        'list',
        '--machinereadable',
        '--fieldseparator=' + field_separator,
        __quote(bpy.data.filepath)
    ])

def unlock(guid):
    return __execute(['lock', 'unlock', guid])

def get_history(format_separator: str):
    history_fields = ['{date}', '{owner}', '{branch}', '{changesetid}', '{comment}']

    return __execute([
        'history',
        '--format=' + format_separator.join(history_fields) + '#__#',
        __quote(bpy.data.filepath)
    ], '#__#')
