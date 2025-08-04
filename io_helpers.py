from huffman.encoder import get_file_header_from_histogram
from huffman.encoder import get_bit_seq_from_data_block
from huffman.encoder import get_write_buffer_from_bit_seq
from huffman.tree import build_lut_from_histogram

def get_byte_histogram_from_file(filename: str, blocksize: int = 1024) -> dict[int, int]:
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
        while data_block := file.read(blocksize):
            for byte in data_block:
                # Count occurrences of each byte (start at 0 if not seen before)
                byte_histogram[byte] = byte_histogram.get(byte, 0) + 1

    return byte_histogram


def encode_file(src_filename, dst_filename: str, blocksize: int = 1024) -> None:
    """
    Encodes the content of a source file using Huffman coding and writes the compressed output to a destination file.

    The function reads the input file block-wise, encodes each data block into a bit sequence based on a Huffman 
    lookup table derived from the file's byte histogram, and writes the resulting binary data along with a 
    decoding header into the destination file.

    Args:
        src_filename (str): Path to the source file that is to be encoded.
        dst_filename (str): Path where the encoded output file will be written.
        blocksize (int, optional): Number of bytes to read per block from the source file. Defaults to 1024.

    Returns:
        None

    Side Effects:
        - Creates a binary file at `dst_filename` containing Huffman-encoded data.
        - Prepends a file header containing metadata required for decoding (e.g., histogram info).

    Raises:
        - FileNotFoundError: If `src_filename` does not exist.
        - IOError: If reading from or writing to a file fails.
    """
    # Generate histogram: {byte_value: frequency} from source file
    histogram: dict[int, int] = get_byte_histogram_from_file(src_filename)

    # Build file header with metadata for decoding (e.g., magic number, histogram length, histogram itself)
    header: bytes = get_file_header_from_histogram(histogram)

    # Create Huffman encoding lookup table from histogram
    enc_lut: dict[int, str] = build_lut_from_histogram(histogram)

    with open(src_filename, "rb") as src, open(dst_filename, "wb") as dst:
        # Holds leftover bits between blocks as a string of 0s and 1s
        bit_seq = ""
        # Buffer to accumulate encoded bytes before writing
        write_buffer = bytearray()

        # Write file header first
        dst.write(header)

        # Process file block by block until EOF
        while data_block := src.read(blocksize):
            # Encode block to bit sequence using lookup table
            bit_seq += get_bit_seq_from_data_block(data_block, enc_lut)

            # Convert bits to byte buffer; preserve any remaining bits for next round
            bit_seq, write_buffer = get_write_buffer_from_bit_seq(bit_seq)
            
            # Write encoded bytes to output file
            dst.write(write_buffer)

        # Final padding if bits remain: pad to full byte and flush remaining buffer
        if bit_seq:
            bit_seq += (8 - len(bit_seq)) * "0"
            _, write_buffer = get_write_buffer_from_bit_seq(bit_seq)
            dst.write(write_buffer)


if __name__ == "__main__":
    pass
    # from huffman.encoder import get_file_header_from_histogram
    # filename = "./output.compressed"
    # histogram = {ord("A"): 100, ord("B"): 50, ord("C"): 25, ord("D"): 25}
    # header = get_file_header_from_histogram(histogram)
    # write_header_to_file(filename, header)