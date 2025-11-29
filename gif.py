#!/usr/bin/env python3
"""
GIF Image Encoder using LZW Compression

This script converts an image file to GIF format using LZW compression.
It reads an image, quantizes colors to 256 or fewer, and creates a proper GIF file.
"""

import sys
import argparse
from PIL import Image
import numpy as np
from lzw import gif_compress_codes, pack_gif_codes


def quantize_colors(image_array, max_colors=256):
    """
    Quantize image colors to at most max_colors.
    
    Args:
        image_array: numpy array of the image
        max_colors: maximum number of colors (default 256 for GIF)
        
    Returns:
        tuple: (quantized_image, color_palette)
    """
    if len(image_array.shape) == 2:
        # Grayscale image
        img = Image.fromarray(image_array, mode='L')
        img_quantized = img.quantize(colors=max_colors)
        palette = img_quantized.getpalette()
        if palette is None:
            # Create a grayscale palette
            palette = []
            for i in range(256):
                palette.extend([i, i, i])
        quantized_array = np.array(img_quantized, dtype=np.uint8)
        return quantized_array, palette[:max_colors * 3]
    else:
        # Color image
        img = Image.fromarray(image_array)
        img_quantized = img.quantize(colors=max_colors)
        palette = img_quantized.getpalette()
        quantized_array = np.array(img_quantized, dtype=np.uint8)
        return quantized_array, palette[:max_colors * 3]


def gif_lzw_compress(data, min_code_size=8):
    """
    Compress data using LZW algorithm adapted for GIF format.
    
    This function uses the GIF-compatible LZW compression from lzw.py.
    
    Args:
        data: list of pixel values (0-255)
        min_code_size: minimum code size in bits (usually 8 for 256 colors)
        
    Returns:
        bytes: compressed data as bytes
    """
    codes = gif_compress_codes(data, min_code_size)
    return pack_gif_codes(codes, min_code_size)


def write_gif_file(image_array, palette, output_path):
    """
    Write a GIF file with the given image data and palette.
    
    Args:
        image_array: numpy array of quantized image (indexed colors)
        palette: color palette (list of RGB values)
        output_path: path to output GIF file
    """
    height, width = image_array.shape[:2]
    
    with open(output_path, 'wb') as f:
        # GIF Header (6 bytes)
        f.write(b'GIF89a')
        
        # Logical Screen Descriptor (7 bytes)
        f.write(width.to_bytes(2, 'little'))  # Width
        f.write(height.to_bytes(2, 'little'))  # Height
        
        # Packed fields
        num_colors = len(palette) // 3
        color_table_size = 0
        if num_colors > 0:
            # Calculate size of color table (2^(n+1) colors)
            color_table_size = (num_colors - 1).bit_length() - 1
            if color_table_size < 1:
                color_table_size = 1
            if color_table_size > 7:
                color_table_size = 7
        
        packed = 0x80  # Global color table flag
        packed |= (color_table_size << 4)
        packed |= 0x07  # Color resolution
        packed |= 0x00  # Sort flag (not sorted)
        f.write(packed.to_bytes(1, 'little'))
        
        f.write(b'\x00')  # Background color index
        f.write(b'\x00')  # Pixel aspect ratio
        
        # Global Color Table
        num_table_colors = 1 << (color_table_size + 1)
        for i in range(num_table_colors):
            if i * 3 < len(palette):
                f.write(palette[i * 3].to_bytes(1, 'little'))      # R
                f.write(palette[i * 3 + 1].to_bytes(1, 'little'))  # G
                f.write(palette[i * 3 + 2].to_bytes(1, 'little'))  # B
            else:
                f.write(b'\x00\x00\x00')  # Fill with black
        
        # Image Descriptor (10 bytes)
        f.write(b',')  # Image separator
        f.write((0).to_bytes(2, 'little'))  # Left position
        f.write((0).to_bytes(2, 'little'))  # Top position
        f.write(width.to_bytes(2, 'little'))  # Width
        f.write(height.to_bytes(2, 'little'))  # Height
        
        # Packed fields (no local color table)
        f.write(b'\x00')
        
        # LZW Minimum Code Size (usually 8 for 256 colors)
        min_code_size = max(2, (num_colors - 1).bit_length()) if num_colors > 1 else 2
        if min_code_size > 8:
            min_code_size = 8
        f.write(min_code_size.to_bytes(1, 'little'))
        
        # Image Data (LZW compressed)
        # Convert 2D image to 1D array (row by row)
        pixel_data = image_array.flatten().tolist()
        compressed_data = gif_lzw_compress(pixel_data, min_code_size)
        
        # Write data in sub-blocks (max 255 bytes per block)
        data_length = len(compressed_data)
        offset = 0
        
        while offset < data_length:
            block_size = min(255, data_length - offset)
            f.write(block_size.to_bytes(1, 'little'))
            f.write(compressed_data[offset:offset + block_size])
            offset += block_size
        
        # End of image data
        f.write(b'\x00')
        
        # GIF Trailer
        f.write(b';')


def convert_to_gif(input_path: str, output_path: str) -> int:
    """
    Convert an image file to GIF format.
    
    Args:
        input_path: path to input image file
        output_path: path to output GIF file
        
    Returns:
        int: exit code (0 for success, 1 for error)
    """
    try:
        # Read and process image
        print(f"Reading image: {input_path}")
        img = Image.open(input_path)
        img_array = np.array(img)
        
        print(f"Original image size: {img_array.shape}")
        print(f"Original image mode: {img.mode}")
        
        # Quantize colors
        print("Quantizing colors...")
        quantized_array, palette = quantize_colors(img_array, max_colors=256)
        
        num_colors = len(set(quantized_array.flatten()))
        print(f"Quantized to {num_colors} colors")
        
        # Write GIF file
        print(f"Writing GIF file: {output_path}")
        write_gif_file(quantized_array, palette, output_path)
        
        print(f"Successfully created GIF file: {output_path}")
        
        # Verify the file was created
        import os
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"Output file size: {file_size} bytes")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main() -> int:
    """
    Main function for GIF converter script.
    
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description='Convert an image to GIF format using LZW compression'
    )
    parser.add_argument(
        'input_path',
        help='Path to the input image file'
    )
    parser.add_argument(
        'output_path',
        help='Path to the output GIF file'
    )
    
    args = parser.parse_args()
    
    return convert_to_gif(args.input_path, args.output_path)


if __name__ == "__main__":
    sys.exit(main())

