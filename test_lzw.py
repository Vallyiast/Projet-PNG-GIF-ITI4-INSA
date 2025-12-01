#!/usr/bin/env python3
"""
Test script for LZW Compression and Decompression

This script tests LZW compression and decompression on image files.
It reads an image file, compresses it using LZW, decompresses it, and displays
the original and reconstructed images for comparison.
"""

import sys
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from lzw import compress, uncompress


def compress_and_decompress_image(image_path: str) -> int:
    """
    Compress and decompress an image using LZW algorithm.
    
    Args:
        image_path: Path to the input image file.
        
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    try:
        # Read the original image file as binary data
        print(f"Reading image file: {image_path}")
        with open(image_path, 'rb') as f:
            original_data = f.read()
        
        original_size = len(original_data)
        print(f"Original file size: {original_size} bytes")
        
        # Convert binary data to string for LZW compression
        # Each byte becomes a character (0-255)
        uncompressed = ''.join(chr(b) for b in original_data)
        print(f"Data prepared for compression: {len(uncompressed)} characters")
        
        # Compress using LZW
        print("\nCompressing with LZW algorithm...")
        compressed_codes = compress(uncompressed)
        num_codes = len(compressed_codes)
        max_code = max(compressed_codes) if compressed_codes else 0
        bits_needed = max(9, max_code.bit_length()) if max_code > 0 else 9
        approx_compressed_size = (num_codes * bits_needed) // 8 + ((num_codes * bits_needed) % 8 > 0)
        
        print(f"Compression complete!")
        print(f"  Number of codes: {num_codes}")
        print(f"  Maximum code value: {max_code}")
        print(f"  Bits per code: {bits_needed}")
        print(f"  Approximate compressed size: {approx_compressed_size} bytes")
        print(f"  Compression ratio: {original_size / approx_compressed_size:.2f}:1")
        print(f"  Space saved: {(1 - approx_compressed_size / original_size) * 100:.2f}%")
        
        # Decompress using LZW
        print("\nDecompressing with LZW algorithm...")
        decompressed = uncompress(compressed_codes)
        decompressed_size = len(decompressed)
        print(f"Decompression complete: {decompressed_size} characters")
        
        # Convert back to binary data
        decompressed_bytes = bytes(ord(c) for c in decompressed)
        
        # Verify data integrity
        data_matches = original_data == decompressed_bytes
        print(f"\nData integrity check: {'✓ PASSED' if data_matches else '✗ FAILED'}")
        if not data_matches:
            print(f"  Original size: {original_size} bytes")
            print(f"  Decompressed size: {len(decompressed_bytes)} bytes")
            # Find first difference
            for i in range(min(original_size, len(decompressed_bytes))):
                if original_data[i] != decompressed_bytes[i]:
                    print(f"  First difference at byte {i}: original={original_data[i]}, decompressed={decompressed_bytes[i]}")
                    break
            return 1
        
        # Load and display images
        print("\nLoading images for display...")
        
        # Load original image
        original_img = Image.open(image_path)
        original_array = np.array(original_img)
        
        # Save decompressed data to a temporary file and load it
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(decompressed_bytes)
        
        try:
            decompressed_img = Image.open(tmp_path)
            decompressed_array = np.array(decompressed_img)
        except Exception as e:
            print(f"Warning: Could not display decompressed image: {e}")
            print("This might be because the decompressed data is not a valid image format.")
            print("However, the binary data matches perfectly, which is what matters for LZW.")
            os.unlink(tmp_path)
            return 0
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        # Calculate difference
        if original_array.shape == decompressed_array.shape:
            difference = np.abs(original_array.astype(int) - decompressed_array.astype(int))
            max_diff = np.max(difference)
            sum_diff = np.sum(difference)
            images_match = np.array_equal(original_array, decompressed_array)
        else:
            difference = None
            max_diff = None
            sum_diff = None
            images_match = False
            print(f"Warning: Image shapes don't match!")
            print(f"  Original shape: {original_array.shape}")
            print(f"  Decompressed shape: {decompressed_array.shape}")
        
        # Display images
        fig, axes = plt.subplots(1, 3, figsize=(18, 7))
        # Maximize window if possible (works on some backends)
        try:
            manager = plt.get_current_fig_manager()
            if hasattr(manager, 'window'):
                if hasattr(manager.window, 'state'):
                    manager.window.state('zoomed')  # Windows
                elif hasattr(manager.window, 'wm_attributes'):
                    manager.window.wm_attributes('-zoomed', True)  # Linux
        except:
            pass  # Fallback if maximization is not supported
        
        # Original image
        axes[0].imshow(original_array)
        axes[0].set_title(f'Original Image')
        axes[0].axis('off')
        
        # Reconstructed image
        axes[1].imshow(decompressed_array)
        axes[1].set_title('Reconstructed Image')
        axes[1].axis('off')
        
        # Difference between images
        if difference is not None:
            axes[2].imshow(difference, cmap='hot')
            axes[2].set_title(f'Difference (sum: {sum_diff:,})')
        else:
            axes[2].text(0.5, 0.5, 'Shape mismatch', 
                        ha='center', va='center', transform=axes[2].transAxes)
            axes[2].set_title('Difference')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Final verification
        print(f"\nPerfect image reconstruction: {images_match}")
        if not images_match and max_diff is not None:
            print(f"Maximum pixel difference: {max_diff}")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main() -> int:
    """
    Main function for LZW compression test script.
    
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description='Compress and decompress an image using LZW algorithm'
    )
    parser.add_argument(
        'image_path',
        nargs='?',
        default='rose.bmp',
        help='Path to the input image file (default: rose.bmp)'
    )
    
    args = parser.parse_args()
    
    return compress_and_decompress_image(args.image_path)


if __name__ == "__main__":
    sys.exit(main())

