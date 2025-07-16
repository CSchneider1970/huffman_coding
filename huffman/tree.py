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
    Represents an internal (non-leaf) node in a Huffman tree.

    This node combines two child nodes (left and right) and accumulates
    their frequencies to build the Huffman encoding structure.

    Attributes:
        left (HuffmanNode | None): The left child node.
        right (HuffmanNode | None): The right child node.
    """

    def __init__(self, byte_counter: int, left: HuffmanNode | None = None, right: HuffmanNode | None = None):
        super().__init__(byte_counter)
        self.left: HuffmanNode | None = left
        self.right: HuffmanNode | None = right


class HuffmanLeaf(HuffmanNode):
    """
    Represents a leaf node in a Huffman tree.

    This node holds a specific byte value and its frequency,
    as part of the final encoding output.

    Attributes:
        byte_value (int | None): The byte value this leaf represents.
    """

    def __init__(self, byte_counter: int, byte_value: int | None = None):
        super().__init__(byte_counter)
        self.byte_value: int | None = byte_value


def build_sorted_huffman_leaves(byte_histogram: dict[int, int]) -> list[HuffmanLeaf]:
    """
    Builds a sorted list of HuffmanLeaf nodes from a byte frequency histogram.

    Args:
        byte_histogram (dict[int, int]): Mapping of byte values to their frequency.

    Returns:
        list[HuffmanLeaf]: Huffman leaves sorted by ascending frequency.
    """

    # Edge case: Add dummy entry to ensure the tree has a branch node
    if len(byte_histogram) == 1:
        byte_histogram[None] = 0  # Dummy byte with zero frequency

    # Sort histogram items by frequency (value)
    sorted_tuples = sorted(byte_histogram.items(), key=lambda item: item[1])

    # Create and return HuffmanLeaf nodes from sorted frequency tuples
    return [HuffmanLeaf(count, byte) for byte, count in sorted_tuples]


def build_huffman_tree_from_leaves(nodes: list[HuffmanLeaf]) -> HuffmanBranch | None:
    """
    Creates a Huffman tree from a list of leaf nodes sorted by ascending frequency.

    This function repeatedly combines the two nodes with the smallest byte_counter
    into a new HuffmanBranch node. The process continues until only one node—
    the root of the Huffman tree—remains.

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


def build_huffman_tree(byte_histogram: dict[int, int]) -> HuffmanBranch | None:
    """
    High-level function to construct a Huffman tree from a byte frequency histogram.

    This function first creates sorted HuffmanLeaf nodes from the input histogram,
    and then builds the Huffman tree by repeatedly combining the lowest-frequency nodes.

    Args:
        byte_histogram (dict[int, int]): A mapping from byte values (0–255) to their frequency counts.

    Returns:
        HuffmanNode | None: The root node of the constructed Huffman tree,
                            or None if the histogram is empty.
    """

    # Convert the histogram into sorted leaf nodes
    leaves = build_sorted_huffman_leaves(byte_histogram)

    # Build and return the Huffman tree from the leaves
    return build_huffman_tree_from_leaves(leaves)


# Traversing a tree iteratively
def create_encoding_table_from_tree(huffman_tree: HuffmanBranch) -> dict[int, str]:
    """
    Generates a lookup table for Huffman encoding from a Huffman tree.

    This function traverses the Huffman tree and assigns each byte value (found in leaf nodes)
    a unique binary string based on its position in the tree. The resulting dictionary maps each
    byte to its Huffman code as a string of '0's and '1's.

    Args:
        huffman_tree (HuffmanBranch): The root of a Huffman tree containing branches and leaves.

    Returns:
        dict[int, str]: A dictionary mapping each byte value to its corresponding Huffman code.
    """

    encoding_table = {}  # Mapping table as a dictionary (Key = Byte to encode, Value = Bit-Sequence for encoding)
    position_as_node_list = [huffman_tree]  # The root of the tree

    while position_as_node_list:
        pass

    return encoding_table


# A recursive approach
def build_huffman_encoding_table_from_tree(huffman_tree):
    def traverse(node, prefix, table):
        if isinstance(node, HuffmanLeaf):
            table[node.byte_value] = prefix
        elif isinstance(node, HuffmanBranch):
            traverse(node.left, prefix + "0", table)
            traverse(node.right, prefix + "1", table)

    huffman_encoding_table = {}
    traverse(huffman_tree, "", huffman_encoding_table)
    return huffman_encoding_table


if __name__ == "__main__":
    import random
    testdaten = {byte: random.randint(1, 100) for byte in range(65, 91)}
    testdaten[100] = 2000
    # testdaten = {65: 100}
    print(testdaten)

    print(build_huffman_encoding_table_from_tree(build_huffman_tree(testdaten)))
