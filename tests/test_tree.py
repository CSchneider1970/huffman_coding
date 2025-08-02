import unittest
from huffman.tree import HuffmanBranch, HuffmanLeaf

class TestTree(unittest.TestCase):

    def test_leaf_initialization(self):
        leaf = HuffmanLeaf(byte_counter=5, byte_value=42)
        assert leaf.byte_counter == 5
        assert leaf.byte_value == 42

    def test_branch_initialization(self):
        left = HuffmanLeaf(2, 10)
        right = HuffmanLeaf(3, 20)
        branch = HuffmanBranch(5, left, right)
        assert branch.byte_counter == 5
        assert branch.left == left
        assert branch.right == right


if __name__ == '__main__':
    unittest.main()
