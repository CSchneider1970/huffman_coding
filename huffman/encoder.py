def build_byte_seq_from_histogram_entry(byte_value: int, count: int) -> bytes:
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


def build_file_header_from_byte_histogram(byte_histogram: dict[int, int]) -> bytes:
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
    file_header += b'HUFF'

    # Length of the histogram (number of unique byte values), stored in 2 bytes
    length = len(byte_histogram)
    file_header.append((length >> 8) & 0xFF)  # High byte
    file_header.append(length & 0xFF)         # Low byte

    # Serialize each histogram entry into the header
    for byte_value, count in byte_histogram.items():
        file_header += build_byte_seq_from_histogram_entry(byte_value, count)

    return bytes(file_header)


if __name__ == "__main__":
    # Simple sanity test with mock histogram
    simple_histogram = {65: 10, 66: 20, 67: 50}
    header = build_file_header_from_byte_histogram(simple_histogram)
    for byte in header:
        print(byte)
        