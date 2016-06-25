
class Symbol:
    def __init__(self, val, attr):
        self.nullable = False
        self.first = set([])
        self.follow = set([])
        self.attr = attr
        self.val = val
