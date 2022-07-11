from typing import Iterable
from tree import Tree
from operations import *
import re

class InstructionSelector:

    def __init__(self, tree: Tree) -> None:
        self._tree: Tree = Tree._clone_tree(tree)
        self.i = 0
        self.leaves = self.tree.leaves()
        self.patterns = {
            '+': plus, '-': minus, '*': prod, '/': div, 'MEM': mem, 'MOVE': move
        }
    
    @property
    def tree(self) -> Tree:
        return self._tree


    def apply_patterns(self):
        """
        Find and apply the patterns of tree
        """
        self._check_tree(self.leaves)


    def _check_tree(self, level: Iterable[Tree]):
        if level:
            for node in level:
                self.find_pattern(node)
            self._check_tree({node._father for node in level if node._father})


    def find_pattern(self, tree: Tree):
        if tree.value not in self.patterns:
            if(re.match(r'CONST.*?', tree.value)):
                const(tree)
            else: temp(tree)
        else: self.patterns[tree.value](tree)