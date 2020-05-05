## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    left, right = 0, x

    while left <= right:
        mid = (left + right) // 2

        if mid ** 2 > x:
            right = mid - 1
        elif mid ** 2 < x:
            left = mid + 1
        else:
            return mid
    return right



################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    if MAX_ITER == 0:
        return x_0
    x_new = x_0 - (f(x_0) / fprime(x_0))
    if abs(x_new - x_0) < EPSILON:
        return x_new
    return find_root(f, fprime, x_new, EPSILON, MAX_ITER-1)

################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    tree = Tree(tokens.pop(0))
    parent, child = tree, tree
    parentsStack = []
    for item in tokens:
        if item is '[':
            parentsStack.append(parent)
            parent = child
        elif item is ']':
            parent = parentsStack.pop()
        else:
            child = Tree(item)
            parent.add_child(child)
    return tree

def max_depth(root): # do not change the heading of the function
    if len(root.children) == 0:
        return 1;
    depth = []
    for node in root.children:
        depth.append(max_depth(node) + 1)
    return max(depth)
