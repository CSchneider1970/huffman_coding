def build_byte_histogram_from_file(filename: str, blocksize: int = 1024) -> dict[int, int]:
    """
    Reads a file in binary mode in small blocks and counts the occurrence of each byte.

    This function processes the file block-by-block, which is memory-efficient and suitable 
    for large files. It returns a frequency histogram of all byte values found.

    Args:
        filename (str): Path to the file to be read.
        blocksize (int, optional): Number of bytes to read per block. Defaults to 1024.

    Returns:
        dict[int, int]: A dictionary mapping each byte (0-255) to its frequency in the file.
    """

    # Initialize byte frequency dictionary
    byte_histogram: dict[int, int] = {}

    # Read file in binary mode block by block
    with open(filename, "rb") as file:
        while byte_block := file.read(blocksize):
            for byte in byte_block:
                # Count occurrences of each byte (start at 0 if not seen before)
                byte_histogram[byte] = byte_histogram.get(byte, 0) + 1

    return byte_histogram
