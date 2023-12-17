import re
from typing import Optional

CHARSET = [ord(x) for x in sorted("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}.,:")]

with open('output', 'r', encoding='utf-8') as f:
    forest = f.read().strip()

print(forest.count('🌴'), len(CHARSET))
forest = forest.replace('🌴', '🌴\n').replace('🎄', '🎄\n').strip().split('\n')
print(forest)

class Node:
    def __init__(self, idx: int) -> None:
        self.idx = [idx]
        self.left: Optional[Node] = None
