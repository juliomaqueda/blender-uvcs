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

def execute(params, newline_separator = None):
    try:
        if __cm_shell_process is None:
            __initialize_uvcs_shell()

        cm_command = ' '.join(params) + "\n"

        __cm_shell_process.stdin.write(cm_command)

        command_output = ''
        command_return_code = 1

        while True:
            __cm_shell_process.stdin.flush()

            output_line = __cm_shell_process.stdout.readline() \
                .replace('\r', '')

            result_code = __extract_command_result_code(output_line)

            if result_code is not None:
                command_return_code = result_code
                break

            if output_line != '':
                command_output += output_line

        return CommandResult(command_return_code == 0, __format_output(command_output, newline_separator))
    except BaseException as ex:
        return CommandResult(False, ['Couldn\'t execute command ' + __cm_command_path])

def __initialize_uvcs_shell():
    global __cm_shell_process

    __cm_shell_process = subprocess.Popen(
        [__cm_command_path, 'shell', '--encoding=UTF-8'],
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
    match = re.search('^CommandResult (\d)\n$', output_line)

    return int(match.group(1)) if match else None

def __format_output(output, newline_separator):
    line_separator = newline_separator + '\n' if newline_separator is not None else '\n'

    return output \
        .rstrip(line_separator) \
        .split(line_separator)

def set_cm_location(path):
    global __cm_command_path, __cm_shell_process

    __cm_command_path = path

    if __cm_shell_process is not None:
        __cm_shell_process.terminate()
        __cm_shell_process = None
