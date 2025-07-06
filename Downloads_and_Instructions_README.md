# Big Sister - Complete Installation & Setup Guide

## Overview

Big Sister is an OSINT (Open Source Intelligence) automation tool designed for CTF competitions. It combines metadata extraction, steganography analysis, and reverse image search capabilities into a unified GUI and CLI interface.

## System Requirements

### Operating System
- **Primary Target**: Debian-based Linux systems (Ubuntu, Kali Linux, etc.)
- **Secondary**: Other Linux distributions with package manager support
- **Minimum**: Python 3.8+

### Hardware Requirements
- **RAM**: Minimum 4GB (8GB recommended for large file analysis)
- **Storage**: 2GB free space for tools and dependencies
- **Network**: Internet connection required for reverse image search

## Core Dependencies

### 1. System Package Dependencies

Install these packages using your system's package manager:

```bash
# Update package lists
sudo apt update

# Install core system tools
sudo apt install -y \
    exiftool \
    steghide \
    binwalk \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    imagemagick-6.q16 \
    ruby \
    ruby-dev \
    build-essential \
    chromium-browser \
    chromium-chromedriver
```

### 2. Ruby Dependencies

```bash
# Install zsteg (Ruby gem for steganography analysis)
sudo gem install zsteg
```

### 3. Python Dependencies

Create a virtual environment and install Python packages:

```bash
# Create virtual environment
python3 -m venv bigsister-env
source bigsister-env/bin/activate

# Install Python packages
pip install --upgrade pip
pip install \
    pillow \
    selenium \
    webdriver-manager \
    tkinter-tooltip \
    requests \
    beautifulsoup4 \
    lxml
```

## Tool-Specific Features

### 1. Metadata Extraction Tools

#### ExifTool
- **Purpose**: Extract comprehensive metadata from images and files
- **Installation**: `sudo apt install exiftool`
- **Features**:
  - EXIF data extraction
  - JSON output support
  - Supports 100+ file formats
  - Custom tag support

#### Pillow (PIL Fork)
- **Purpose**: Fallback image processing library
- **Installation**: `pip install pillow`
- **Features**:
  - Basic EXIF extraction when ExifTool unavailable
  - Image format detection
  - Image resizing and processing

### 2. Steganography Analysis Tools

#### Steghide
- **Purpose**: Detect and extract hidden data in images
- **Installation**: `sudo apt install steghide`
- **Supported Formats**: JPEG, BMP3, WAV, AU
- **Features**:
  - Password-protected extraction
  - Capacity analysis
  - Info mode for metadata inspection
- **Script**: [`runsteghide.sh`](src/steganography/runsteghide.sh)

#### Zsteg
- **Purpose**: Ruby-based steganography detection
- **Installation**: `sudo gem install zsteg`
- **Features**:
  - LSB steganography detection
  - Multiple analysis modes
  - Comprehensive scanning options
- **Script**: [`runzsteg.sh`](src/steganography/runzsteg.sh)

#### Binwalk
- **Purpose**: Firmware and file signature analysis
- **Installation**: `sudo apt install binwalk`
- **Features**:
  - Embedded file detection
  - Automatic extraction
  - Entropy analysis
  - Custom signature support
- **Script**: [`runbinwalk.sh`](src/steganography/runbinwalk.sh)

### 3. Image Search Capabilities

#### Selenium WebDriver
- **Purpose**: Automated reverse image searching
- **Installation**: `pip install selenium webdriver-manager`
- **Features**:
  - Google Images reverse search
  - Automated browser interaction
  - Result extraction and parsing
- **Requirements**: Chrome/Chromium browser

#### Chrome/Chromium Browser
- **Installation**: `sudo apt install chromium-browser chromium-chromedriver`
- **Purpose**: Browser automation for image search
- **Alternative**: Google Chrome can be used instead

## Project Structure & Features

### Core Modules

#### 1. Metadata Processing
- **Location**: [`src/metadata/`](src/metadata/)
- **Components**:
  - [`exiftool_scraper.py`](src/metadata/exiftool_scraper.py) - EXIF data extraction
  - [`parser.py`](src/metadata/parser.py) - Unified metadata parsing

#### 2. Steganography Analysis
- **Location**: [`src/steganography/`](src/steganography/)
- **Components**:
  - [`steghide_scraper.py`](src/steganography/steghide_scraper.py) - Steghide automation
  - [`binwalk_scraper.py`](src/steganography/binwalk_scraper.py) - Binwalk automation
  - [`zsteg_scraper.py`](src/steganography/zsteg_scraper.py) - Zsteg automation
  - Shell scripts for each tool

#### 3. Image Search (IRIS)
- **Location**: [`src/iris/`](src/iris/)
- **Components**:
  - [`image_search.py`](src/iris/image_search.py) - Reverse image search automation

#### 4. User Interfaces
- **Location**: [`src/utils/`](src/utils/)
- **Components**:
  - [`gui.py`](src/utils/gui.py) - Tkinter-based GUI with dark/light mode
  - [`terminal.py`](src/utils/terminal.py) - Command-line interface
  - [`file_handler.py`](src/utils/file_handler.py) - File operation utilities

### 5. Main Orchestration
- **Location**: [`src/main.py`](src/main.py)
- **Features**:
  - Unified metadata processing chain
  - CLI argument parsing
  - GUI/Terminal mode selection

## Configuration

### Tool Paths Configuration
Edit [`config.json`](config.json) to specify custom tool paths:

```json
{
  "tool_paths": {
    "exiftool": "/usr/bin/exiftool",
    "zsteg": "/usr/local/bin/zsteg",
    "steghide": "/usr/bin/steghide",
    "binwalk": "/usr/bin/binwalk"
  }
}
```

## Supported File Formats

### Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp) - Note: BMP V5 requires conversion to BMP3 for Steghide
- GIF (.gif)
- TIFF (.tiff, .tif)
- WebP (.webp)

### Audio Formats (Steghide)
- WAV (.wav)
- AU (.au)

### General Files (Binwalk)
- Firmware images
- Archive files
- Any binary file with embedded data

## Troubleshooting

### Common Issues

#### 1. BMP Format Compatibility
If you encounter BMP format errors with Steghide:
```bash
# Convert BMP V5 to BMP3
convert input.bmp bmp3:output_v3.bmp
```

#### 2. Chrome/Chromium WebDriver Issues
```bash
# Update webdriver
pip install --upgrade webdriver-manager

# Alternative Chrome installation
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

#### 3. Permission Issues
```bash
# Make shell scripts executable
chmod +x src/steganography/*.sh
chmod +x scripts/*.sh
```

---

**Note**: This tool is designed for educational and legitimate OSINT research. Users are responsible for compliance with applicable laws and terms of service when using reverse image search features.