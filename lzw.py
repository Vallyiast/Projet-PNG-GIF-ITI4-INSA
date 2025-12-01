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
