#!/bin/bash

# Folder containing cmc folders which contain card images
IMAGE_ROOT="path-to-folder-containing-cmc-image-folders"

# Iterate through all subdirectories
for dir in "${IMAGE_ROOT}"/*; do
    # Check if directory is empty
    if [ -d "$dir" ] && [ "$(ls -A "$dir")" ]; then
        # Create a new folder for the converted files
        mkdir -p "${dir}/converted_files"
        
        # Iterate through each JPG file and convert it to a rescaled monochrome bitmap
        for jpg_file in "${dir}"/*.jpg; do
            if [ -f "$jpg_file" ]; then
                echo "Resizing and converting to grayscale for: $jpg_file"
                
                # Define the output filename by replacing the extension with bmp
                output_file="${dir}/converted_files/$(basename -- "$jpg_file" .jpg).bmp"
                
                # Use ImageMagick's convert command to perform the conversion
                convert "$jpg_file" -resize 384x -colorspace Gray -monochrome "$output_file"
                
                # Check if conversion was successful
                if [ $? -eq 0 ]; then
                    echo "Conversion successful: $jpg_file"
                else
                    echo "Error converting: $jpg_file"
                fi
            fi
        done
    else
        echo "No JPG files found in directory: $dir"
    fi
done
