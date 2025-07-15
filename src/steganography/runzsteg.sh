#!/bin/bash
# Zsteg analysis script
# Path: BigSister/src/steganography/runzsteg.sh

IMAGE_PATH="$1"

# === Safety checks ===
if [ -z "$IMAGE_PATH" ]; then
    echo "Error: No image path provided!"
    echo "Usage: $0 <image_path>"
    exit 1
fi

if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: File '$IMAGE_PATH' does not exist!"
    exit 1
fi

if ! command -v zsteg &> /dev/null; then
    echo "Error: zsteg is not installed."
    echo "Please install it using: gem install zsteg"
    exit 1
fi

# === Zsteg analysis ===
echo "🧬 Running Zsteg scan on: $IMAGE_PATH"
echo "Please wait..."
echo ""

# Run multiple modes
zsteg "$IMAGE_PATH"
echo ""
echo "────────────────────────────────────────────"
echo "📣 Verbose Scan:"
zsteg -v "$IMAGE_PATH"
echo ""
echo "────────────────────────────────────────────"
echo "🧠 Full Analysis (-a):"
zsteg -a "$IMAGE_PATH"
echo ""
echo "────────────────────────────────────────────"
echo "📦 Extract All Detected Payloads:"
zsteg -E "$IMAGE_PATH"
echo ""
echo "✅ Done!"
