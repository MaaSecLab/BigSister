#!/bin/bash
# filepath: /home/lambda/Desktop/BigSister/BigSister/src/steganography/run_zsteg.sh

#Check if an image path was provided
if [ $# -eq 0 ]; then #This line checks if no arguments were passed to the script
    echo "Error: No image path provided!"
    echo "Usage: $0 <image_path>"
    echo "Please provide a valid image file path."
    exit 1
fi

IMAGE_PATH="$1" # This line gives the first command line argument to a variable

#Check if given image file exists
if [ ! -f "$IMAGE_PATH" ]; then #This line checks if the file does not exist. (-f checks if the file exists and is a regular file)
    echo "Error: File '$IMAGE_PATH' does not exist or was not found!"
    echo "Please provide a valid image file path."
    exit 1
fi

#Check if zsteg is installed
#command -v checks if a command is available in the system's PATH (exists and is executable)
#command -v zsteg = checks if the zsteg command is available
#&> /dev/null redirects both stdout and stderr to /dev/null, resulting in no output (silently checking)

if ! command -v zsteg &> /dev/null; then 
    echo "Error: zsteg is not installed."
    echo "Please install zsteg using 'gem install zsteg'."
    exit 1
fi

# Function to run basic zsteg scan
run_basic() {
    echo "Running basic zsteg scan..."
    echo "========================================="
    zsteg "$IMAGE_PATH"
    echo ""
}

# Function to run verbose scan
run_verbose() {
    echo "Running verbose zsteg scan..."
    echo "========================================="
    zsteg -v "$IMAGE_PATH"
    echo ""
}

# Function to run detailed scan with all options
run_detailed() {
    echo "Running detailed analysis with all options..."
    echo "========================================="
    zsteg -a "$IMAGE_PATH"
    echo ""
}

# Function to extract all detected data
run_extract() {
    echo "Extracting all detected data..."
    echo "========================================="
    zsteg -E "$IMAGE_PATH"
    echo ""
}

# Function to run all scans
run_all() {
    echo "Running complete zsteg analysis..."
    echo "========================================="
    run_basic
    run_verbose
    run_detailed
    run_extract
}

# Display menu and get user choice
echo "Zsteg Analysis for: $IMAGE_PATH"
echo ""
echo "Choose analysis type:"
echo "1) Basic scan (zsteg)"
echo "2) Verbose output (zsteg -v)"
echo "3) Detailed analysis (zsteg -a)"
echo "4) Extract all data (zsteg -E)"
echo "5) Run all scans"
echo "6) Custom selection"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        run_basic
        ;;
    2)
        run_verbose
        ;;
    3)
        run_detailed
        ;;
    4)
        run_extract
        ;;
    5)
        run_all
        ;;
    6)
        echo ""
        echo "Select which scans to run (y/n):"
        read -p "Basic scan? (y/n): " basic
        read -p "Verbose output? (y/n): " verbose
        read -p "Detailed analysis? (y/n): " detailed
        read -p "Extract all data? (y/n): " extract
        
        echo ""
        if [[ $basic =~ ^[Yy]$ ]]; then
            run_basic
        fi
        if [[ $verbose =~ ^[Yy]$ ]]; then
            run_verbose
        fi
        if [[ $detailed =~ ^[Yy]$ ]]; then
            run_detailed
        fi
        if [[ $extract =~ ^[Yy]$ ]]; then
            run_extract
        fi
        ;;
    *)
        echo "Invalid choice. Please run the script again and select 1-6."
        exit 1
        ;;
esac

echo "Analysis complete!"