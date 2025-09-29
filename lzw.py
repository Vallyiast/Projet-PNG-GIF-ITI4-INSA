#!/usr/bin/env python3
"""
LZW (Lempel-Ziv-Welch) Compression and Decompression Implementation

This module implements the LZW algorithm for lossless data compression.
It includes functions for compressing and decompressing strings, with
demonstration code for image compression and visualization.

The LZW algorithm works by building a dictionary of character sequences
during compression and using numerical codes to represent repeated patterns,
resulting in data compression for files with repetitive content.
"""

import numpy as np
import sys
import matplotlib.pyplot as plt

def compress(uncompressed):
    """
    Compress a string using the LZW (Lempel-Ziv-Welch) algorithm.
    
    Args:
        uncompressed (str): The input string to compress.
        
    Returns:
        list: A list of integer codes representing the compressed data.
        
    Note:
        The algorithm builds a dictionary of character sequences during compression,
        starting with all possible single characters (0-255) and expanding as
        repeated patterns are found.
    """
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def uncompress(compressed):
    """
    Decompress a list of LZW codes back to the original string.
    
    Args:
        compressed (list): A list of integer codes from LZW compression.
        
    Returns:
        str: The decompressed string.
        
    Raises:
        ValueError: If an invalid compressed code is encountered.
        
    Note:
        This function reverses the LZW compression process by rebuilding the
        dictionary and converting codes back to character sequences.
        It handles the special case where a code references a dictionary entry
        that hasn't been created yet.
    """
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    result = []
    
    if not compressed:
        return ""
    
    # Initialize with first code
    w = chr(compressed[0])
    result.append(w)
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            # Special case: code not yet in dictionary
            entry = w + w[0]
        else:
            raise ValueError(f"Invalid compressed code: {code}")
        
        result.append(entry)
        
        # Add new entry to dictionary
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        
        w = entry
    
    return ''.join(result)

def main() -> int:
    """
    Main function demonstrating LZW compression and decompression.
    
    Creates a test image, compresses it using LZW, decompresses it back,
    and visualizes the results. Also tests compression on a simple string.
    
    Returns:
        int: Exit code (0 for success).
    """
	# Image generation
    height, width = 100, 100
    image = np.zeros((height, width), dtype=np.uint8)
    image[20:80, 20:80] = 200
    image[40:60, 40:60] = 100
    flat_image = image.flatten()
    uncompressed = ''.join(chr(p) for p in flat_image)  # As bytes
    print(f"Approximate size without compression: {len(uncompressed)} bits")

    compressed_codes = compress(uncompressed)
    num_codes = len(compressed_codes)
    max_code = max(compressed_codes)
    bits_needed = max(9, (max_code.bit_length()))
    approx_size = (num_codes * bits_needed) // 8 + ((num_codes * bits_needed) % 8 > 0)

    print(f"Number of codes: {num_codes}")
    print(f"Approximate size with compression: {approx_size} bits")
    
    # Test decompression
    decompressed = uncompress(compressed_codes)
    print(f"Compression/decompression successful: {uncompressed == decompressed}")
    
    # Image reconstruction
    decompressed_image = np.array([ord(c) for c in decompressed], dtype=np.uint8)
    reconstructed_image = decompressed_image.reshape((height, width))
    
    # Test with a simple string
    test_string = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"\nTest with string: '{test_string}'")
    compressed_test = compress(test_string)
    decompressed_test = uncompress(compressed_test)
    print(f"Compressed codes: {compressed_test}")
    print(f"Decompressed: '{decompressed_test}'")
    print(f"Test successful: {test_string == decompressed_test}")
    
    # Display images
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original image')
    axes[0].axis('off')
    
    # Reconstructed image
    axes[1].imshow(reconstructed_image, cmap='gray')
    axes[1].set_title('Reconstructed image')
    axes[1].axis('off')
    
    # Difference between images
    difference = np.abs(image.astype(int) - reconstructed_image.astype(int))
    axes[2].imshow(difference, cmap='hot')
    axes[2].set_title('Difference (should be black)')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Reconstruction verification
    images_match = np.array_equal(image, reconstructed_image)
    print(f"\nPerfect image reconstruction: {images_match}")
    if not images_match:
        max_diff = np.max(difference)
        print(f"Maximum difference: {max_diff}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
