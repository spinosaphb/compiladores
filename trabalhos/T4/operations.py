from tree import Tree
import re
from utils import JOUETTE_PATTERNS

def move(node: Tree) -> None:
    """
    Get move operation
    """

    pattern = 14
    if (not node.left) or (node.left.value != "MEM"):
        return
    
    if node.left.pattern == 10:
        tile = [node] + node.left.tile_pattern
        pattern = 14
        node.pattern = pattern
        for tile_member in node.left.tile_pattern:
            tile_member.tile_root = False
            tile_member.tile_pattern = tile
        node.tile_root = True
        node.tile_pattern = tile
    elif(node.left.pattern == 11):
        tile = [node] + node.left.tile_pattern
        pattern = 15 
        node.pattern = pattern
        for tile_member in node.left.tile_pattern:
            tile_member.tile_root = False
            tile_member.tile_pattern = tile
        node.tile_root = True
        node.tile_pattern = tile
    elif(node.left.pattern == 12):
        tile = [node] + node.left.tile_pattern
        pattern = 16
        node.pattern = pattern
        for tile_member in node.left.tile_pattern:
            tile_member.tile_root = False
            tile_member.tile_pattern = tile
        node.tile_root = True
        node.tile_pattern = tile
    elif(node.left.pattern == 13):
        if (node.left is not None and node.right.pattern == 13):
            tile = [node, node.left, node.right]                  
            pattern = 18 
            node.pattern = pattern
            node.tile_pattern = tile
            node.left.tile_pattern = tile
            node.right.tile_pattern = tile
            node.tile_root = True
            node.left.tile_root = False
            node.right.tile_root = False
        else:
            tile = [node, node.left]
            pattern = 17 
            node.pattern = pattern
            node.tile_pattern = tile
            node.left.tile_pattern = tile
            node.tile_root = True
            node.left.tile_root = False
    

def mem(node: Tree) -> None:
    """
    Get move operation
    """
    pattern = 13
    if not node.left: return
    if (node.left.value == "+"):
        if node.left.pattern == 6:
            tile = [node, node.left, node.left.right]
            pattern = 10 
            node.tile_pattern = tile
            node.left.tile_pattern = tile
            node.left.right.tile_pattern = tile
            node.tile_root = True
            node.left.tile_root = False
            node.left.right.tile_root = False
        elif(node.left.pattern == 7):
            tile = [node, node.left, node.left.left]
            pattern = 11 
            node.tile_pattern = tile
            node.left.tile_pattern = tile
            node.left.left.tile_pattern = tile
            node.tile_root = True
            node.left.tile_root = False
            node.left.left.tile_root = False
        node.pattern = pattern
    elif (re.match(r'CONST.*?', node.left.value)):
        tile = [node, node.left]
        node.pattern = 12 
        node.tile_pattern = tile
        node.left.tile_pattern = tile
        node.tile_root = True
        node.left.tile_root = False
    else:
        tile = [node]
        node.pattern = 13 
        node.tile_pattern = tile
        node.tile_root = True

def prod(node: Tree) -> None: 
    """
    Get prod operation
    """
    if (not node.left) or (not node.right):
        return
    node.pattern = 3
    node.tile_pattern = [node]
    node.tile_root = True

def div(node: Tree) -> None:
    """
    Get div operation
    """
    if (not node.left) or (not node.right): return
    node.pattern = 5
    node.tile_pattern = [node]
    node.tile_root = True

def minus(node: Tree) -> None:
    """
    Get minus operation
    """
    if(node.right is not None and re.match(r'CONST.*?', node.right.value)):
        tile = [node, node.right]
        node.pattern = 9 
        node.tile_pattern = tile
        node.tile_root = True
        node.right.tile_pattern = tile
        node.right.tile_root = False
    elif(node.left is not None and node.right is not None):
        tile = [node]
        node.pattern = 4
        node.tile_pattern = tile
        node.tile_root = True

def plus(node: Tree):
    """
    Get plus operation
    """
    if (node.left is not None and re.match(r'CONST.*?', node.left.value)):
        tile = [node, node.left]
        node.pattern = 7
        node.tile_pattern = tile
        node.tile_root = True 
        node.left.tile_pattern = tile
        node.left.tile_root = False
    elif(node.right is not None and re.match(r'CONST.*?', node.right.value)):
        tile = [node, node.right]
        node.pattern = 6
        node.tile_pattern = tile
        node.tile_root = True
        node.right.tile_pattern = tile
        node.right.tile_root = False
    elif(node.left is not None and node.right is not None):
        tile = [node]
        node.pattern = 2
        node.tile_pattern = tile
        node.tile_root = True

def const(node: Tree):
    """
    Get const operation
    """
    tile = [node]
    node.pattern = 8
    node.tile_pattern = tile
    node.tile_root = True

def temp(node: Tree):
    """
    Get temp operation
    """
    tile = [node]
    node.pattern = 1
    node.tile_pattern = tile
    node.tile_root = True


def get_instructions(patterns):
    a = 1 
    b = 1
    c = 1
    patterns = patterns[::-1]
    instructions_ = []
    for i in range(len(patterns)):
        node = patterns[i][0] 
        option = patterns[i][1]
        instruction = JOUETTE_PATTERNS.get(option, None)
        
        if (option == 1):
            b = a
            a += 1
        
        elif (option in [2, 3, 4, 5]):
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=node.left.get_value_view(a), k=b)}'
            )
        
        elif (option in [6, 7, 9]):
            r1 = node.right.get_value_view(a) 
            r2 = node.left.get_value_view(a+1)
            j, c = (r2, r1) if option in [6, 9] else (r1, r2)  
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=j, c=c)}'
            )
                
        if (option == 8):
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=0, c=node.get_value_view(a))}'
            )
        
        if (option in [10, 11]):
            child = node.left
            r1 = child.right.get_value_view(a) 
            r2 = child.left.get_value_view(a+1)
            j, c = (r2, r1) if option == 10 else (r1, r2)

            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=j, c=c)}'
            )
            
        if (option == 12):
            child = node.left
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=0, c=child.get_value_view(a))}'
            )

        if (option == 13):
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=b, c=0)}'
            )

        if (option in [14, 15]): 
            child = node.left.left
            r1 = child.right.get_value_view(a) 
            r2 = child.left.get_value_view(a+1)
            j, c = (r2, r1) if option == 14 else (r1, r2)
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=j, c=c)}'
            )
            
        if (option == 16):
            child = node.left.left
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=0, c=child.get_value_view(a))}'
            )

        if (option == 17):
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=a, c=0)}'
            )
        
        if (option == 18):
            instructions_.append(
                f'{i+1} {instruction.format(i=b, j=a)}'
            )
    return instructions_