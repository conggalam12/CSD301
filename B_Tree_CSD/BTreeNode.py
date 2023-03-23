class BTreeNode:
    def __init__(self, leaf=False,keys=None, child=None,):
        self.leaf = leaf
        self.keys = keys or []
        self.child = child or []
