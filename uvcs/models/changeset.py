class ChangesetEntry():
    date = None
    owner = None
    branch = None
    changeset = None
    comment = None

    def __init__(self, date, owner, branch, changeset, comment):
        self.date = date
        self.owner = owner
        self.branch = branch
        self.changeset = changeset
        self.comment = comment
