#!/usr/bin/env python3

import os
from PIL import Image
import pyheif

def convert_heic_to_jpg(input_path, output_path=None):
    # Load the HEIC file using pyheif
    heif_file = pyheif.read(input_path)

    # Convert the HEIC file to a format suitable for PIL (Python Imaging Library)
    image = Image.frombytes(
        heif_file.mode,  # Image mode
        heif_file.size,  # Image size
        heif_file.data,  # Image data
        "raw",           # Raw data type
        heif_file.mode,  # Same mode as the HEIC file
        heif_file.stride,  # Number of bytes per row
    )

    # Set the default output path if not provided
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".jpg"

    # Save the image in JPG format
    image.save(output_path, "JPEG")
    print(f"Converted {input_path} to {output_path}")

def convert_all_heic_in_directory(directory_path):
    # Get all HEIC files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".heic"):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.splitext(input_path)[0] + ".jpg"
            
            # Convert the HEIC file to JPG
            convert_heic_to_jpg(input_path, output_path)

if __name__ == "__main__":
    # Specify the directory containing HEIC files
    heic_directory = "path/to/your/heic/files"
    
    # Convert all HEIC files in the specified directory to JPG
    convert_all_heic_in_directory(heic_directory)
