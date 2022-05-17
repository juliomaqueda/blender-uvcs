from . import command

__active_branch = None
__branches = []
__branches_loaded = False

def set_active_branch(branch_name):
    global __active_branch
    __active_branch = branch_name

def get_active_branch(): return __active_branch

def get_branches():
    global __branches_loaded, __branches

    if not __branches_loaded:
        __branches_loaded = True
        __branches = []

        command_result = command.get_branches()

        if command_result.success:
            __branches = command_result.output

    return __branches

def switch_to_branch(branch_name):
    command_result = command.switch_to_branch(branch_name)

    if command_result.success:
        global __active_branch
        __active_branch = branch_name

        return None

    return command_result.output

def create_branch(branch_name):
    command_result = command.create_branch(branch_name)

    if command_result.success:
        __branches.append(branch_name)
        return None

    return command_result.output

def clear_cache():
    global __active_branch, __branches, __branches_loaded

    __active_branch = None
    __branches = []
    __branches_loaded = False
