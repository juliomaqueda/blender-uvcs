class LockEntry():
    guid = None
    owner = None
    branch = None
    type = None

    def __init__(self, guid, owner, branch, type):
        self.guid = guid
        self.owner = owner
        self.branch = branch
        self.type = type
