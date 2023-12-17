import re
from typing import Optional

CHARSET = [ ord(x) for x in sorted("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{.,}: ")]

with open('output', 'r', encoding='utf-8') as f:
    forest = f.read().strip()

print(forest.count('🌴'), len(CHARSET))
forest = forest.replace('🌴', '🌴\n').replace('🎄', '🎄\n').strip().split('\n')
print(forest)

class Node:
    def __init__(self, idx: int) -> None:
        self.idx = [idx]
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None

class Tree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def _recursive_set_node(self, cur: Node, idx: int, route: str) -> None:
        if route[0] == '🎄':
            cur.idx.append(idx)
        elif route[1] == '🌴':
            new_node = Node(idx)
            new_node.parent = cur
            if route[0] == '🌳':
                cur.left = new_node
            elif route[0] == '🌲':
                cur.right = new_node
        else:
            if route[0] == '🌳' and cur.left is not None:
                self._recursive_set_node(cur.left, idx, route[1:])
            elif route[0] == '🌲' and cur.right is not None:
                self._recursive_set_node(cur.right, idx, route[1:])
            else:
                print('something wrong')
                exit()

    def set_node(self, idx:int, route:str) -> None:
        if self.root is None:
            self.root = Node(idx)
        else:
            self._recursive_set_node(self.root, idx, route)

    def _recursive_inorder_walk(self, cur: Node)->list[list[int]]:
        left, right = [], []
        if cur.left is not None:
            left = self._recursive_inorder_walk(cur.left)
        if cur.right is not None:
            right = self._recursive_inorder_walk(cur.right)
        return left+[cur.idx]+right

    def inorder_tree_walk(self) -> list[list[int]]:
        res = []
        if self.root is not None:
            res = self._recursive_inorder_walk(self.root)
        return res

def solve():
    tree = Tree()
    for i,route in enumerate(forest):
        tree.set_node(i, route)
    res = tree.inorder_tree_walk()
    print(res)

    pattern = re.compile('DH{[a-f0-9]{64}}')

    for genkey in range(0,0x100):
        new_charset = sorted([x^genkey for x in CHARSET])
        tmpflag = [-1 for _ in range(len(forest))]

        for i, idxs in enumerate(res):
            for idx in idxs:
                tmpflag[idx] = new_charset[i]^genkey
        tmpflag_str = ''.join([chr(x) for x in tmpflag])
        if pattern.search(tmpflag_str) is not None:
            print(tmpflag_str)

solve()
