import re

class Stack(list):
    def push(self, __object):
        self.append(__object)

    def isempty(self): return not self

class Tree:

    def __init__(self, value, left: 'Tree' = None, right: 'Tree' = None, father: 'Tree' = None, color: int = None):
        self.value = value
        self._left: Tree = self.__totree(left) if left else None 
        self._right: Tree = self.__totree(right) if right else None
        self._father: Tree = self.__totree(father) if father else None

        if self._left:
            self._left._father = self
        
        if self._right:
            self._right._father = self

        self._color = color

        left_len = len(self._left) if self._left else 0
        right_len = len(self._right) if self._right else 0
        self._len = max(left_len, right_len) + 1

    def __len__(self) -> int:
        return self._len


    @staticmethod
    def __totree(__object: 'Tree'): return __object if isinstance(__object, Tree) else Tree(__object)


    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Tree):
            return Tree.__isequeal(self, __o)
        return False

    @staticmethod
    def __isequeal(t1: 'Tree', t2: 'Tree'):
        if t1 is None and t2 is None:
            return True
    
        if t1 is not None and t2 is not None:
            return (
                (t1.value == t2.value) and
                Tree.__isequeal(t1.left, t2.left)
                and
                Tree.__isequeal(t1.right, t2.right)
            )
        
        return False        


    @staticmethod
    def _clone_tree(root: 'Tree'):
        if root is None:
            return None
        copy = Tree(
            root.value,
            left=Tree._clone_tree(root.left),
            right=Tree._clone_tree(root.right),
            father=root._father,
            color=root._color
        )
        # if root.left:
        #     copy.left = Tree._clone_tree(root.left) 
        # if root.right:
        #     copy.right = Tree._clone_tree(root.right)
        
        return copy


    def printtree(self, sep='\n'):
        print(self.value)
        if self.left:
            self.left.printtree()
        if self.right:
            self.right.printtree()


    @property
    def left(self) -> 'Tree': return self._left

    @property
    def right(self) -> 'Tree': return self._right

    @left.setter
    def left(self, other: 'Tree'):
        self._left = self.__totree(other) 

    @right.setter
    def right(self, other: 'Tree'):
        self._right = self.__totree(other)


    def bshow(self):
        return self._bshow(self, '')

    
    @staticmethod
    def _bshow(node: 'Tree', heritage: str):
        if node and (node.left or node.right):
            Tree._bshow(node.right, heritage + "r")
        
        i = 0
        while i < (len(heritage) - 1):
            print("│   " if heritage[i] != heritage[i+1] else "    ", end='')
            i += 1
        
        if heritage != '':
            print("┌───" if heritage[-1] == 'r' else "└───", end='')
        
        if not node:
            print()
            return
        father = node._father.value if node._father else None
        print(f'|{node.value}|{father}|', end='')
        color = f'({node._color})' if node._color else ''
        print(color)

        if node and (node.left or node.right):
            Tree._bshow(node.left, heritage + "l")


    @staticmethod
    def from_expression(input_: str, verbose=False) -> 'Tree':
        
        main_stack = Stack()
        worker_stack = Stack()
        op = ''

        def unstack():
            while not main_stack.isempty():
                son = main_stack.pop()
                if son == '(':
                    father = main_stack.pop()
                    left = worker_stack.pop() if worker_stack else None
                    right = worker_stack.pop() if worker_stack else None

                    worker_stack.push(Tree(value=father, left=left, right=right))
                    break
                worker_stack.push(son)
            main_stack.push(worker_stack.pop())

        for char in input_:    
            if char in ['(', ',', ')']:
                if op: main_stack.push(op)
                if char == '(': main_stack.push(char)
                elif char == ')': unstack()
                op = '' 
            else: op += char  
        
        return main_stack.pop()


    def subtrees(self):
        subtrees_ = []
        if self.left:
            subtrees_.append(self._clone_tree(self.left))
        if self.right:
            subtrees_.append(self._clone_tree(self.right))
        return subtrees_


    def leaves(self):
        leafs = []
        def _get_leaf_nodes(node: 'Tree'):
            if node is not None:
                if node.left or node.right:
                    if node.left: _get_leaf_nodes(node.left)
                    if node.right: _get_leaf_nodes(node.right)
                else:
                    leafs.append(node)
        _get_leaf_nodes(self)
        return leafs

