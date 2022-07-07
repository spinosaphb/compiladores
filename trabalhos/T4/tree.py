class Stack(list):
    def push(self, __object):
        self.append(__object)

    def isempty(self): return not self

class Tree:

    def __init__(self, value, left: 'Tree' = None, right: 'Tree' = None):
        self.value = value
        self._left: Tree = self.__totree(left) if left else None 
        self._right: Tree = self.__totree(right) if right else None
        

    @staticmethod
    def __totree(__object: 'Tree'): return __object if isinstance(__object, Tree) else Tree(__object)


    @staticmethod
    def _clone_tree(root: 'Tree'):
        if root is None:
            return None
        copy = Tree(root.value)
        if root.left:
            copy.left = Tree._clone_tree(root.left) 
        if root.right:
            copy.right = Tree._clone_tree(root.right)
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

        print(node.value)

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
            
            exp = worker_stack.pop()
            main_stack.push(exp)
            
            if verbose: exp.bshow()

        for char in input_:    
            if char in ['(', ',', ')']:
                if op: main_stack.push(op)
                if char == '(': main_stack.push(char)
                elif char == ')': unstack()
                op = '' 
            else: op += char  
        return main_stack.pop()      
