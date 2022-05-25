from . import command

def checkin(comment):
    command_result = command.checkin(comment)

    return None if command_result.success else command_result.output

def undo():
    command_result = command.undo()

    return None if command_result.success else command_result.output
