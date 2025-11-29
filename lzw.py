#!/usr/bin/env python3
"""
LZW (Lempel-Ziv-Welch) Compression and Decompression Implementation

This module implements the LZW algorithm for lossless data compression.
It includes functions for compressing and decompressing strings.

The LZW algorithm works by building a dictionary of character sequences
during compression and using numerical codes to represent repeated patterns,
resulting in data compression for files with repetitive content.
"""

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


def gif_compress_codes(data, min_code_size=8):
    """
    Compress data using LZW algorithm adapted for GIF format.
    
    GIF LZW uses variable-width codes and includes Clear code and End code.
    This function returns the list of codes that can be packed with pack_gif_codes.
    
    Args:
        data: list of pixel values (0-255) or string of characters
        min_code_size: minimum code size in bits (usually 8 for 256 colors)
        
    Returns:
        list: A list of integer codes including Clear and End codes
    """
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    
    # Initialize dictionary: map sequence (as tuple) to code
    dictionary = {}
    # Add single pixel/character values to dictionary
    for i in range(clear_code):
        dictionary[(i,)] = i
    
    next_code = end_code + 1
    
    result = []
    w = tuple()
    
    # Start with clear code
    result.append(clear_code)
    
    # Convert data to list of integers if it's a string
    if isinstance(data, str):
        data_list = [ord(c) for c in data]
    else:
        data_list = data
    
    for pixel in data_list:
        wc = w + (pixel,)
        
        if wc in dictionary:
            w = wc
        else:
            # Output code for w
            if w in dictionary:
                result.append(dictionary[w])
            
            # Add new sequence to dictionary
            if next_code <= 4095:  # GIF max code value
                dictionary[wc] = next_code
                next_code += 1
            
            w = (pixel,)
    
    # Output code for remaining w
    if w and w in dictionary:
        result.append(dictionary[w])
    
    # End code
    result.append(end_code)
    
    return result


def pack_gif_codes(codes, min_code_size):
    """
    Pack LZW codes into bytes using GIF's variable-width code encoding.
    
    In GIF LZW, code size starts at (min_code_size + 1) bits and increases
    when we've used all codes of the current size. Code size increases when
    the next dictionary code would exceed the current maximum.
    
    Args:
        codes: list of integer codes (from gif_compress_codes)
        min_code_size: minimum code size in bits
        
    Returns:
        bytes: packed codes as bytes for GIF format
    """
    if not codes:
        return b''
    
    code_size = min_code_size + 1
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    
    bit_buffer = 0
    bits_in_buffer = 0
    output = []
    
    # Track the maximum code we expect to see based on dictionary growth
    max_expected_code = clear_code + 1  # Initially just clear and end codes
    next_dict_code = end_code + 1
    
    for code in codes:
        # Determine current maximum code for this code size
        max_code_for_size = (1 << code_size) - 1
        
        # If the code we're about to write exceeds current capacity, increase code size
        if code > max_code_for_size and code_size < 12:
            code_size += 1
            max_code_for_size = (1 << code_size) - 1
        
        # Track dictionary growth: when we see a data code, it means a new entry was added
        if code != clear_code and code != end_code:
            # The code we're writing represents a dictionary entry
            # After writing this, the next dictionary code will be max(code + 1, next_dict_code)
            max_expected_code = max(max_expected_code, code + 1)
            
            # Check if we need to increase code size before the next code
            if max_expected_code > max_code_for_size and code_size < 12:
                code_size += 1
        
        # Add code to buffer (LSB first, little-endian bit packing)
        bit_buffer |= (code << bits_in_buffer)
        bits_in_buffer += code_size
        
        # Write complete bytes
        while bits_in_buffer >= 8:
            output.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bits_in_buffer -= 8
    
    # Write remaining bits (if any)
    if bits_in_buffer > 0:
        output.append(bit_buffer & 0xFF)
    
    return bytes(output)
