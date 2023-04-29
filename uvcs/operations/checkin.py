import bpy

from . import command
from ... import common

def checkin(comment):
    params = ['checkin', '--all', '--private']

    if comment is not None and comment != '':
        params.append('-c')
        params.append(common.quote(comment))

    params.append(common.quote(bpy.data.filepath))

    command_result = command.execute(params)

    return None if command_result.success else command_result.output

def undo():
    command_result = command.execute(['undo', '--silent', common.quote(bpy.data.filepath)])

    return None if command_result.success else command_result.output
