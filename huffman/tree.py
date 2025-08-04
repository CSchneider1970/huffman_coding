"""
Huffman Tree Construction Module

This module provides the data structures and utilities needed to construct Huffman trees
from byte frequency histograms. It defines the building blocks of the tree—including leaf
and branch nodes—and exposes functions for generating the tree and creating lookup tables
used for Huffman encoding.

Core functionality includes:
- Representing tree nodes for both leaves and branches
- Constructing a Huffman tree from sorted leaf nodes
- Generating encoding lookup tables via tree traversal (iterative and recursive)
- Providing high-level interfaces for tree and LUT construction from histograms

Classes:
- HuffmanNode: Base class representing a node with byte frequency
- HuffmanLeaf: Leaf node representing a specific byte value
- HuffmanBranch: Internal node combining two child nodes

Functions:
- get_leaves_from_histogram: Converts frequency histogram into sorted leaf nodes
- get_tree_from_leaves: Builds Huffman tree from leaf nodes using greedy merging
- get_lut_from_tree: Generates a byte-to-bit mapping by traversing the tree (iterative)
- get_lut_from_tree_recursive: Generates the same mapping using a recursive strategy
- build_tree: High-level wrapper that constructs a Huffman tree from a histogram
- build_lut_from_histogram: Convenience method to create an encoding table in one step
"""

class HuffmanNode:
    """
    Base class for nodes in a Huffman tree.

    Each node tracks the frequency of a byte or combination of bytes
    used during the construction of the Huffman tree.

    Attributes:
        byte_counter (int): Frequency count of the byte(s) represented by this node.
    """
    def __init__(self, byte_counter: int):
        self.byte_counter: int = byte_counter


class HuffmanBranch(HuffmanNode):
    """
    Represents an internal node in a Huffman tree.

    This node combines two child nodes (left and right) and accumulates
    their frequencies to build the Huffman encoding structure.

    Attributes:
        left (HuffmanNode): The left child node.
        right (HuffmanNode): The right child node.
    """
    def __init__(self, byte_counter: int, left: HuffmanNode, right: HuffmanNode):
        super().__init__(byte_counter)
        self.left: HuffmanNode = left
        self.right: HuffmanNode = right


class HuffmanLeaf(HuffmanNode):
    """
    Represents a leaf node in a Huffman tree.

    This node holds a specific byte value and its frequency,
    as part of the final encoding output.

    Attributes:
        byte_value (int): The byte value this leaf represents.
    """
    def __init__(self, byte_counter: int, byte_value: int):
        super().__init__(byte_counter)
        self.byte_value: int = byte_value


def get_leaves_from_histogram(byte_histogram: dict[int, int]) -> list[HuffmanLeaf]:
    """
    Builds a sorted list of HuffmanLeaf nodes from a byte frequency histogram.

    Args:
        byte_histogram (dict[int, int]): Mapping of byte values to their frequency.

    Returns:
        list[HuffmanLeaf]: Huffman leaves sorted by ascending frequency.
    """
    # Sort histogram items by frequency (value)
    sorted_tuples = sorted(byte_histogram.items(), key=lambda item: item[1])

    # Create and return HuffmanLeaf nodes from sorted frequency tuples
    return [HuffmanLeaf(count, byte) for byte, count in sorted_tuples]


def get_tree_from_leaves(nodes: list[HuffmanLeaf]) -> HuffmanNode | None:
    """
    Creates a Huffman tree from a list of leaf nodes sorted by ascending frequency.

    This function repeatedly combines the two nodes with the smallest byte_counter
    into a new HuffmanBranch node. The process continues until only one node,
    the root of the Huffman tree, remains.

    Args:
        nodes (list[HuffmanLeaf]): Sorted list of leaf nodes by frequency.

    Returns:
        HuffmanNode | None: Root node of the Huffman tree, or None if input is empty.
    """
    # As long as there is more than one node, combine two to form a new subtree.
    while len(nodes) > 1:
        # Combine two nodes with the smallest frequency to preserve optimal prefix encoding.
        # The frequency of the new node results from the sum of the two.
        left = nodes.pop(0)
        right = nodes.pop(0)

        combined = HuffmanBranch(left.byte_counter + right.byte_counter, left, right)

        # Insert the new node back into the list and sort it again by frequency.
        nodes.append(combined)
        nodes.sort(key=lambda node: node.byte_counter)

    return nodes[0] if nodes else None  # Return the root node, or None if no nodes were provided.


def get_lut_from_tree(huffman_tree: HuffmanNode | None) -> dict[int, str]:
    """
    Generates a lookup table for Huffman encoding from a Huffman tree.

    This function traverses the Huffman tree and assigns each byte value (found in leaf nodes)
    a unique binary string based on its position in the tree. The resulting dictionary maps each
    byte to its Huffman code as a string of '0's and '1's.

    Args:
        huffman_tree (HuffmanNode | None): The root of a Huffman tree containing branches and leaves.

    Returns:
        dict[int, str]: A dictionary mapping each byte value to its corresponding Huffman code.
    """
    # Edge case: Huffman tree is None
    if huffman_tree == None:
        return {}
    
    # Edge case: Huffman tree consists of only one leaf
    if isinstance(huffman_tree, HuffmanLeaf):
        return {huffman_tree.byte_value: "0"}

    # Dictionary to store Huffman codes: {byte_value: bit_string}
    lookup_table: dict[int, str] = {}

    # Stack to traverse the tree: [(node, bit_string_so_far)]
    # Starts with the root node and an empty bit string
    traversal_stack: list[tuple[HuffmanNode, str]] = [(huffman_tree, "")]

    # Iterative tree traversal
    while traversal_stack:
        node, bit_string = traversal_stack.pop()

        if isinstance(node, HuffmanLeaf):
            # Store the accumulated bit string as the Huffman code
            lookup_table[node.byte_value] = bit_string
        elif isinstance(node, HuffmanBranch):
            # Traverse left child, add '0' to bit string
            traversal_stack.append((node.left, bit_string + "0"))
            # Traverse right child, add '1' to bit string
            traversal_stack.append((node.right, bit_string + "1"))

    return lookup_table


def get_lut_from_tree_recursive(huffman_tree: HuffmanBranch | HuffmanLeaf | None) -> dict[int, str]:
    """
    Generates a lookup table for Huffman encoding from a Huffman tree.

    This function traverses the Huffman tree and assigns each byte value (found in leaf nodes)
    a unique binary string based on its position in the tree. The resulting dictionary maps each
    byte to its Huffman code as a string of '0's and '1's. This function uses a recursive
    approach to traverse the Huffman tree.

    Args:
        huffman_tree (HuffmanBranch | HuffmanLeaf | None): 
            The root node of the Huffman tree used to generate encoding lookup values.

    Returns:
        dict[int, str]: A dictionary mapping each byte value to its corresponding Huffman code.
    """
    # Edge case: Huffman tree is None
    if huffman_tree == None:
        return {}
    
    # Edge case: Huffman tree consists of only one leaf
    if isinstance(huffman_tree, HuffmanLeaf):
        return {huffman_tree.byte_value: "0"}

    # Dictionary to store Huffman codes: {byte_value: bit_string}
    lookup_table: dict[int, str] = {}

    # Recursive tree traversal
    def traverse_tree(node: HuffmanBranch | HuffmanLeaf, lut: dict[int, str], bit_string: str) -> None:
        if isinstance(node, HuffmanLeaf):
            # Store the accumulated bit string as the Huffman code
            lut[node.byte_value] = bit_string
        else:
            # Traverse left child, add '0' to bit string
            traverse_tree(node.left, lut, bit_string + "0")
            # Traverse left child, add '1' to bit string
            traverse_tree(node.right, lut, bit_string + "1")

    traverse_tree(huffman_tree, lookup_table, "")

    return lookup_table


def build_tree(byte_histogram: dict[int, int]) -> HuffmanNode | None:
    """
    High-level function to construct a Huffman tree from a byte frequency histogram.

    This function first creates sorted HuffmanLeaf nodes from the input histogram,
    and then builds the Huffman tree by repeatedly combining the lowest-frequency nodes.

    Args:
        byte_histogram (dict[int, int]): A mapping from byte values (0-255) to their frequency counts.

    Returns:
        HuffmanNode | None: The root node of the constructed Huffman tree,
                            or None if the histogram is empty.
    """
    # Convert the histogram into sorted leaf nodes
    leaves = get_leaves_from_histogram(byte_histogram)

    # Build and return the Huffman tree from the leaves
    return get_tree_from_leaves(leaves)


def build_lut_from_histogram(byte_histogram: dict[int, int]) -> dict[int, str]:
    """
    High-level function to generate a Huffman encoding lookup table from a byte histogram.

    This function abstracts away tree construction and encoding traversal,
    providing a one-step interface for generating Huffman codes.

    Args:
        byte_histogram (dict[int, int]): A mapping from byte values (0-255) to their frequency counts.

    Returns:
        dict[int, str]: Lookup table that maps each byte to its Huffman code.
                        If the histogram is empty, an empty dictionary is returned.
    """
    # Construct the Huffman tree from frequency histogram
    tree = build_tree(byte_histogram)

    # Generate and return the encoding table from the tree
    return get_lut_from_tree(tree) if tree else {}


if __name__ == "__main__":
    print("Simple sanity test with mock histogram")
    histogram = {ord('A'): 5, ord('B'): 2, ord('C'): 1}
    print("Mock histogram :", histogram)
    lookup_table = build_lut_from_histogram(histogram)
    print("Lookup table:", lookup_table)
