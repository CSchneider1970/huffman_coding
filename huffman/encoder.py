"""
Huffman Encoder Module

This module defines the data structures and functions used to
encode a file using the Huffman codes associated with the file.
"""

def get_bytes_from_histogram_entry(byte_value: int, count: int) -> bytes:
    """
    Constructs a byte sequence representing a histogram entry.

    The resulting sequence consists of:
    - 1 byte representing the actual byte value (0-255)
    - 4 bytes representing the frequency count of that byte in big-endian order

    Args:
        byte_value (int): The byte value to encode (0-255).
        count (int): The frequency count associated with the byte.

    Returns:
        bytes: A 5-byte sequence combining the byte value and its count.
    """
    # Initialize bytearray for building the byte sequence of an entry
    byte_seq = bytearray()

    # Encode 1 byte for the byte value (ensure it's in the valid range)
    byte_seq.append(byte_value & 0xFF)

    # Encode 4 bytes for the frequency count in big-endian format
    byte_seq.append((count >> 24) & 0xFF)   # Most significant byte
    byte_seq.append((count >> 16) & 0xFF)
    byte_seq.append((count >> 8) & 0xFF)
    byte_seq.append(count & 0xFF)           # Least significant byte

    return bytes(byte_seq)


def get_file_header_from_histogram(byte_histogram: dict[int, int]) -> bytes:
    """
    Constructs a binary file header from a byte histogram.

    The header consists of:
    - A 4-byte magic number ("HUFF") to identify the file format.
    - A 2-byte length field indicating the number of entries in the histogram.
    - A sequence of encoded histogram entries, each converted to bytes.

    Args:
        byte_histogram (dict[int, int]): A dictionary mapping byte values (0-255) to their frequencies.

    Returns:
        bytes: The resulting file header as a byte sequence.
    """
    # Initialize bytearray for building the header
    file_header = bytearray()

    # Magic number (4 bytes) to identify the file format
    file_header += b"HUFF"

    # Length of the histogram (number of unique byte values), stored in 2 bytes
    length = len(byte_histogram)
    file_header.append((length >> 8) & 0xFF)  # High byte
    file_header.append(length & 0xFF)         # Low byte

    # Serialize each histogram entry into the header
    for byte_value, count in byte_histogram.items():
        file_header += get_bytes_from_histogram_entry(byte_value, count)

    return bytes(file_header)


def get_bit_seq_from_data_block(data_block: bytes, encoding_table: dict[int, str]) -> str:
    """
    Converts a block of bytes into a bit string using a Huffman encoding table.

    Each byte in `data_block` is mapped to its corresponding bit representation 
    using the `encoding_table`, and the results are concatenated into a single string.

    Args:
        data_block (bytes): Sequence of bytes to encode.
        encoding_table (dict[int, str]): Mapping of byte values (0-255) to Huffman-encoded bit strings.

    Returns:
        str: The concatenated bit sequence.

    Raises:
        ValueError: If a byte in `data_block` is missing from the `encoding_table`.
    """
    # Using a list is more memory-efficient than string concatenation.
    bit_sequence = []

    # Map each byte to its encoded bit string using the table.
    for byte in data_block:
        encoded_bits = encoding_table.get(byte)
        if encoded_bits is None:
            raise ValueError(f"Byte {byte} not included in encoding table.")
        bit_sequence.append(encoded_bits)

    # Finally, create a string from the list of strings and return it.
    return ''.join(bit_sequence)


def get_write_buffer_from_bit_seq(bit_seq: str) -> tuple[str, bytearray]:
    """
    Encodes a bit sequence into a byte-oriented write buffer.

    Splits the input bit sequence into 8-bit chunks, converts each chunk into a byte,
    and appends it to a write buffer. Any remaining bits (fewer than 8) are returned.

    Args:
        bit_seq (str): A string of bits (e.g., "10101000...").

    Returns:
        tuple[str, bytearray]: A tuple containing:
            - The remaining bits that didn't form a complete byte.
            - The write buffer with encoded bytes.
    """
    write_buffer = bytearray()

    # Encode full 8-bit segments as bytes
    while len(bit_seq) >= 8:
        bit_str = bit_seq[:8]               # Extract the next 8 bits
        byte_val = int(bit_str, 2)          # Convert bit string to integer
        write_buffer.append(byte_val)       # Append to buffer
        bit_seq = bit_seq[8:]               # Discard processed bits

    # Return remaining bits and byte buffer
    return bit_seq, write_buffer


if __name__ == "__main__":
    # Sanity test: mock histogram with sample frequencies
    simple_histogram = {65: 255, 66: 254, 67: 253}
    file_header = get_file_header_from_histogram(simple_histogram)

    print(f"\n📦 File header for histogram: {simple_histogram}\n")

    fields = {
        "Magic number": file_header[:4],
        "Header length": file_header[4:6],
    }

    # Each entry is 5 bytes: 1 for symbol, 4 for frequency
    for i in range(3):
        offset = 6 + i * 5
        symbol = file_header[offset:offset + 1]
        frequency = file_header[offset + 1:offset + 5]
        fields[f"Entry {i + 1} (symbol)"] = symbol
        fields[f"Entry {i + 1} (frequency)"] = frequency

    for label, value in fields.items():
        print(f"{label}: {value}")
