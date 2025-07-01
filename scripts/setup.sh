#!/bin/bash

# Update package list and install required tools
sudo apt-get update
sudo apt-get install -y exiftool zsteg steghide binwalk

# Install Python dependencies
pip install -r ../requirements.txt

# Create necessary directories if they don't exist
mkdir -p ../src/metadata
mkdir -p ../src/iris
mkdir -p ../src/utils

echo "Setup completed successfully."