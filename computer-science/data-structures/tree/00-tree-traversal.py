import math
from typing import Deque, List, Optional
from collections import deque


class Node:
    def __init__(self, k: int):
        self.k = k
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self):
        return "{}".format(self.k)


tree_1 = Node(10)
tree_1.left = Node(20)
tree_1.right = Node(30)
tree_1.right.left = Node(40)
tree_1.right.right = Node(50)


def inorder(root: Node) -> List[int]:
    lyst: List[int] = []

    def recursive(node: Optional[Node]):
        if node is None:
            return

        recursive(node.left)
        lyst.append(node.k)
        recursive(node.right)

    recursive(root)

    return lyst


assert(inorder(tree_1) == [20, 10, 40, 30, 50])


def preorder(root: Node) -> List[int]:
    lyst: List[int] = []

    def recursive(node: Optional[Node]):
        if node is None:
            return

        lyst.append(node.k)
        recursive(node.left)
        recursive(node.right)

    recursive(root)

    return lyst


assert(preorder(tree_1) == [10, 20, 30, 40, 50])


def postorder(root: Node) -> List[int]:
    lyst: List[int] = []

    def recursive(node: Optional[Node]):
        if node is None:
            return

        recursive(node.left)
        recursive(node.right)
        lyst.append(node.k)

    recursive(root)

    return lyst


assert(postorder(tree_1) == [20, 40, 50, 30, 10])


def is_leaf_node(node: Node) -> bool:
    return node.left is None and node.right is None


tree_2 = Node(10)
tree_2.right = Node(20)
tree_2.right.right = Node(30)


def size(node: Optional[Node]) -> int:
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)


assert(size(tree_1) == 5)
assert(size(tree_2) == 3)


tree_3 = Node(10)
tree_3.left = Node(50)
tree_3.left.left = Node(40)
tree_3.left.right = Node(25)
tree_3.right = Node(30)
tree_3.right.left = Node(80)


def get_maximum(node: Optional[Node]) -> float:
    if node is None:
        return -math.inf

    return max(node.k, get_maximum(node.left), get_maximum(node.right))


assert(get_maximum(tree_1) == 50)
assert(get_maximum(tree_2) == 30)
assert(get_maximum(tree_3) == 80)


def key_in(node: Optional[Node], key: int) -> bool:
    if node is None:
        return False

    return node.k == key or key_in(node.left, key) or key_in(node.right, key)


assert(key_in(tree_1, 50) == True)
assert(key_in(tree_1, 5) == False)
assert(key_in(tree_2, 30) == True)
assert(key_in(tree_2, 40) == False)
assert(key_in(tree_3, 80) == True)
assert(key_in(tree_3, 20) == False)

tree_4 = Node(10)
tree_4.left = Node(8)
tree_4.right = Node(30)
tree_4.right.left = Node(40)
tree_4.right.right = Node(50)
tree_4.right.right.right = Node(70)


tree_5 = Node(30)
tree_5.left = Node(40)
tree_5.left.left = Node(70)
tree_5.left.left.right = Node(80)
tree_5.right = Node(20)

tree_6 = Node(10)
tree_6.left = Node(20)
tree_6.left.left = Node(30)


def height(node: Optional[Node]) -> int:
    """" Calculates the height of a tree considering the number of nodes in the
    longest path """
    if node is None:
        return 0

    return 1 + max(height(node.left), height(node.right))


assert(height(tree_4) == 4)
assert(height(Node(10)) == 1)
assert(height(tree_5) == 4)
assert(height(tree_6) == 3)
assert(height(None) == 0)


def height_alt(node: Optional[Node]) -> int:
    """" Calculates the height of a tree considering the number of edges in the
    longest path """

    if node is None:
        return -1

    return max(height_alt(node.left), height_alt(node.right)) + 1


assert(height_alt(None) == -1)
assert(height_alt(Node(10)) == 0)
assert(height_alt(tree_4) == 3)
assert(height_alt(tree_5) == 3)
assert(height_alt(tree_6) == 2)

tree_7 = Node(10)
tree_7.left = Node(20)
tree_7.left.left = Node(40)
tree_7.left.right = Node(50)
tree_7.right = Node(30)
tree_7.right.right = Node(60)


def inorder_it(node: Optional[Node]) -> List[int]:
    lyst: List[int] = []

    visited_nodes: List[Node] = []
    current_node = node
    while current_node is not None:
        visited_nodes.append(current_node)
        current_node = current_node.left

    while len(visited_nodes) > 0:
        current_node = visited_nodes.pop()
        lyst.append(current_node.k)
        current_node = current_node.right
        while current_node is not None:
            visited_nodes.append(current_node)
            current_node = current_node.left

    return lyst


assert(inorder_it(tree_1) == [20, 10, 40, 30, 50])


def preorder_it(node: Optional[Node]) -> List[int]:
    lyst: List[int] = []

    if node is not None:
        visited_nodes = [node]
        while len(visited_nodes):
            current_node = visited_nodes.pop()
            lyst.append(current_node.k)
            if current_node.right:
                visited_nodes.append(current_node.right)
            if current_node.left:
                visited_nodes.append(current_node.left)

    return lyst


assert(preorder_it(tree_7) == [10, 20, 40, 50, 30, 60])


def level_order_it(node: Optional[Node]) -> List[int]:
    lyst: List[int] = []
    if node is not None:
        visited_nodes = [node]

        while len(visited_nodes):
            current_node = visited_nodes.pop(0)
            lyst.append(current_node.k)
            if current_node.left:
                visited_nodes.append(current_node.left)
            if current_node.right:
                visited_nodes.append(current_node.right)

    return lyst


assert(level_order_it(tree_7) == [10, 20, 30, 40, 50, 60])
assert(level_order_it(Node(10)) == [10])
assert(level_order_it(None) == [])


def level_order_it_deque(node: Optional[Node]) -> List[int]:
    """
    Return the items of a tree in leve-order. Considerably faster than the list
    implementation since the Deque collection is optimized for the popleft
    operation O(1) vs O(n).
    """
    lyst: List[int] = []
    if node is not None:
        visited_nodes: Deque[Node] = deque()
        visited_nodes.append(node)
        while len(visited_nodes) > 0:
            current_node = visited_nodes.popleft()
            lyst.append(current_node.k)
            if current_node.left is not None:
                visited_nodes.append(current_node.left)
            if current_node.right is not None:
                visited_nodes.append(current_node.right)
    return lyst


assert(level_order_it_deque(tree_7) == [10, 20, 30, 40, 50, 60])
assert(level_order_it_deque(Node(10)) == [10])
assert(level_order_it_deque(None) == [])
