# Deleting a key on a B-tree in Python
from BTreeNode import BTreeNode
class BTree:
    def __init__(self,t):
        self.root = BTreeNode(True)
        self.t = t
    
    def split_child(self, x, i):
        t = self.t

        # y is a full child of x
        y = x.child[i]
        
        # create a new node and add it to x's list of child
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)

        # insert the median of the full child y into x
        x.keys.insert(i, y.keys[t - 1])

        # split apart y's keys into y & z
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]

        # if y is not a leaf, we reassign y's child to y & z
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    def insert(self, k):
        if self.search(k,self.root) != None:
            return
        t = self.t
        root = self.root

        # if root is full, create a new node - tree's height grows by 1
        if len(root.keys) == (2 * t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.child.insert(0, root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        t = self.t
        i = len(x.keys) - 1

        # find the correct spot in the leaf to insert the key
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        # if not a leaf, find the correct subtree to insert the key
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            # if child node is full, split it
            if len(x.child[i].keys) == (2 * t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.child[i], k)
    def bfs_traversal(self):
        if not self.root:
            return
        current_level = [self.root]
        while current_level:
            next_level = []
            for node in current_level:
                print(node.keys , end = " ")
                if not node.leaf:
                    next_level += node.child
            current_level = next_level
    def inOrder(self,node):
        # traverse all the nodes
        n = len(node.keys)
        for i in range(n):
            # traverse the ith child subtree
            if not node.leaf:
                self.inOrder(node.child[i])
            # print the ith key value
            print(node.keys[i], end=" ")
        # traverse the rightmost child subtree
        if not node.leaf:
            self.inOrder(node.child[n])
    def search(self, key, node=None):
        node = self.root if node == None else node
    
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(key, node.child[i])

    #Search key in the tree
    def search_key(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return x
            elif x.leaf:
                return None
            else:
                return self.search_key(k, x.child[i])
        else:
            return self.search_key(k, self.root)
    def find_parent(self,value,x = None):
        if x.leaf:
            return None
        if x is not None:
            i = 0
            while i < len(x.keys) and value > x.keys[i]:
                i += 1
            if i < len(x.keys) and value in x.child[i].keys:
                return x
            else:
                return self.find_parent(value,x.child[i])
    def left_brother_leaf(self,x,t,parent):
        l = len(parent.child[t-1].keys)
        #case 2
        if l>1:
            x.keys[0] = parent.keys[t-1]
            parent.keys[t-1] = parent.child[t-1].keys[l-1]
            parent.child[t-1].keys.pop(l-1) # xoa theo index
        #case 3
        else:
            parent.child.pop(t)
            parent.child[t-1].keys.insert(1,parent.keys[t-1])
            parent.keys.pop(t-1)
    def right_brother_leaf(self,x,t,parent):
        l = len(parent.child[t+1].keys)
        if l>1:
            x.keys[0] = parent.keys[t]
            parent.keys[t] = parent.child[t+1].keys[0]
            parent.child[t+1].keys.pop(0)
        else:
            parent.child.pop(t)
            parent.child[t+1].keys.insert(0,parent.keys[t])
            parent.keys.pop(t)
    def delete(self,node,value):
        if node is None:
            return
        x = self.search_key(value,node)
        if x is None:
            return 
        if x.leaf:
            parent = self.find_parent(value,node)
            #case 1:
            if len(x.keys)>1:
                x.keys.remove(value)
                return
            else:
                t = 0
                for i in range(len(parent.child)):
                    if parent.child[i] == x:
                        break
                    else:
                        t+=1
                if t == 0:
                    self.right_brother_leaf(x,0,parent)
                else:
                    self.left_brother_leaf(x,t,parent)
        # Not leaf
        else:
            #case 4+5
            a = x.keys.index(value)# vd 33 -> 1 -> a = 1
            if len(x.keys)>1:
                #case 4
                if len(x.child[a].keys)> 1 or len(x.child[a+1].keys)>1:
                    # left child 
                    if len(x.child[a].keys)> 1:
                        x.keys[a] = x.child[a].keys[len(x.child[a].keys)-1]
                        x.child[a].keys.remove(x.keys[a])
                    # right child
                    else:
                        x.keys[a] = x.child[a+1].keys[0]
                        x.child[a+1].keys.remove(x.keys[a])
                #case 5
                else:
                    x.keys.remove(x.keys[a]) # Xoa 30 
                    x.child[a].keys.append(x.child[a+1].keys[0])
                    x.child.remove(x.child[a+1])
            elif len(x.keys) == 1 and (len(x.child[a].keys)> 1 or len(x.child[a+1].keys)>1):
                if len(x.child[a].keys)> 1:
                    x.keys[a] = x.child[a].keys[len(x.child[a].keys)-1]
                    x.child[a].keys.remove(x.keys[a])
                else:
                    x.keys[a] = x.child[a+1].keys[0]
                    x.child[a+1].keys.remove(x.keys[a])
            #case 6
            else:
                # if node is root
                if x == node:
                    if len(x.child) == 1:
                        node = node.child[0]
                    else:
                        if len(x.child[0].child)==2 and len(x.child[1].child) == 2:
                            x.child[0].child[1].keys.append(x.child[1].child[0])
                            x.child[0].child.append(x.child[1].child[1])
                            x.child[0].keys.append(x.child[1].keys[0])
                            node = node.child[0]
                        else:
                            x.child[0].keys.append(x.child[1].keys[0])
                            for i in x.child[1].child:
                                x.child[0].child.append(i)
                            node = node.child[0]
                else:
                    if len(x.child) > 1:
                        x.child[0].keys.insert(1,x.child[1].keys[0])
                    parent = self.find_parent(value,node)
                    t = 0
                    for i in range(len(parent.child)):
                        if parent.child[i] == x:
                            break
                        else:
                            t+=1
                    if t == len(parent.child)-1:
                    # node is most right
                        parent.child[t-1].keys.append(parent.keys[t-1])
                        parent.child[t-1].child.append(x.child[0])
                        parent.keys.remove(parent.keys[t-1])
                        parent.child.remove(x)
                    else:
                        parent.child[t+1].keys.insert(0,parent.keys[t])
                        parent.child[t+1].child.insert(0,x.child[0])
                        parent.keys.remove(parent.keys[t])
                        parent.child.remove(x)

    # Print the tree
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)
# def insert_and_search_example():
#     B = BTree(2)
    
#     B.insert(5)
#     B.insert(10)
#     B.insert(15)
#     B.insert(4)
#     B.insert(14)
#     B.insert(22)
#     B.insert(23)
        

#     B.print_tree(B.root)
#     print()

#     keys_to_search_for = [2, 9, 11, 4]
#     for key in keys_to_search_for:
#         if B.search(key,B.root) is not None:
#             print(f'{key} is in the tree')
#         else:
#             print(f'{key} is NOT in the tree')
# insert_and_search_example()
