from . import command

def checkin(comment):
    command_result = command.checkin(comment)

    if command_result.success:
        return None

    return command_result.output
