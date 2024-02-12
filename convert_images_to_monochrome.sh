#!/bin/bash

#folder containing card images
cd "path-to-folder-containing-default-jpg-files" 

# Create a new folder for the converted files
mkdir -p converted_files

# Iterate through each JPG file and convert it to a rescaled monochrome bitmap
for file in *.jpg; do

    echo "Resizing and converting to grayscale for: $file"

    # Define the output filename by replacing the extension with bmp
    output_file="converted_files/$(basename -- "$file" .jpg).bmp"
    
    # Use ImageMagick's convert command to perform the conversion
    convert "$file" -resize 384x -colorspace Gray -monochrome "$output_file"
done