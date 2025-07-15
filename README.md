# Big Sister (OSINT challenge automation tool)

## Description

Big Sister is a collection of script and tools that simplify the process of solving OSINT challenges during CTF competitions. 

## Problem

Open-Source Intelligence (OSINT) challenges are a central part of CTF competitions. They involve giving the participants some data (e.g. Image, Video, Audio etc.) and them finding out more information about the data using context clues and possible file metadata. 

We can automate many of the processes that are common across the majority of OSINT challenges, meaning that we can reduce the amount of time we spend on such challenges, increasing productivity and efficiency.

## Scope

For the first version of our "Big Sister" tool we will implement a metadata scraper and parser, alongside an Image Retrieval and Identification Script (I.R.I.S), which will use pre-existing reverse image search services to find close matches. In later stages we can implement Artificial Intelligence integration, that will provide LLM models such as ChatGPT o3 with the previously gathered data to result in even more comprehensive results.

## Implementation

Our main goal for this project is to create a program that is easy to use and modify. That means that we will use high-level programming languages and scripting languages, such as python, bash and lua. The target Operating System will be Debian-based Linux systems.

The metadata scraper part of the program will make a series of calls to third-party tools, such as exiftool, zsteg, steghide and binwalk. Another part of the program will then parse the output of those tools and store the lines that contain usable information. Lines containing information regarding the name of the user, the location of the file and other custom values are prime targets. Python based operating system calls can make calls to these tools with the file as an argument. Additionally, python is able to handle the parsing by using text matching.

IRIS can also be handled implemented using python. We can fork and use [Google-Reverse-Image-Search unofficial API](https://github.com/RMNCLDYO/Google-Reverse-Image-Search) as the basis for this module.

## Testing

This project will ideally reach a point where it is able to solve challenges without human intervention. We can perform testing by using OSINT challenges from past competitions, we have access to the [ctf-archives repository](https://github.com/sajjadium/ctf-archives) to collect OSINT challenges from a wide variety of competitions.


## Contribuitors
- [Alexia-Madalina Cirstea] (https://github.com/AlexiaMadalinaCirstea) (University emaiL: m.cirstea@student.maastrichtuniversity.nl) (Personal email: mmadalinacirstea@gmail.com)

- [Vlad-Luca Manolescu] (https://github.com/IlikeEndermen) (University emaiL: v.manolescu@student.maastrichtuniversity.nl) (Personal email: vvladmlg@gmail.com)

- [Irina Iarlykanova] (https://github.com/Irench1k) (University email: i.iarlykanova@student.maastrichtuniversity.nl) (Personal email: irina.iarlykanova@gmail.com)


# Complete Installation & Setup Guide

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


# Metadata and Steganography Toolset

This README documents the **Big Sister** project—a modular toolkit for analyzing and extracting metadata and embedded content from images and other media files.

---

## Overview

This documentation summarizes work completed on the Big Sister project, including:

- Steghide modules (shell script and Python scraper)
- Binwalk modules (shell script and Python scraper)
- ExifTool scraper updates
- Unified parser updates
- Main orchestration logic
- Steghide cover format compatibility and usage

---

## Modules

### Steghide Module

**scripts/runsteghide.sh**

A Bash wrapper for the `steghide` CLI that supports:

- `--info` mode to display embedded data metadata
- `--passphrase` (`-p`) to supply a passphrase when required
- `--output-dir` (`-o`) to specify where extracted files land

```bash
runsteghide.sh [--info] [-p PASS] [-o OUTPUT_DIR] <file>
```

**src/steganography/steghide_scraper.py**

A Python class `SteghideScraper` that:

- Invokes `steghide info -v` or `steghide extract` via `subprocess`
- Accepts an optional `passphrase` argument
- Parses `Key: Value` lines using a regex helper
- Returns a `dict` of metadata fields or raw output
- Provides `display_metadata()` to print results in human‑readable form

---

### Binwalk Module

**scripts/runbinwalk.sh**

A Bash wrapper for the `binwalk` CLI that supports:

- Signature scanning (default mode)
- Extraction (`-e` / `--extract`) to pull out embedded files
- Custom extraction directory (`-d` / `--output-dir`)

```bash
runbinwalk.sh [-e] [-d OUTPUT_DIR] <file>
```

**src/steganography/binwalk_scraper.py**

A Python class `BinwalkScraper` that:

- Invokes `binwalk` or `binwalk -e -C` via `subprocess`
- Returns a `dict` with a `Signatures` list of `{Offset, Description}`
- Includes raw output in the returned dict
- Provides `display_metadata()` to print signature tables and extraction info

---

### ExifTool Scraper

**src/metadata/exiftool_scraper.py**

A Python class `MetadataScraper` that:

- Attempts to call `exiftool -j -n` via `subprocess` to get full JSON metadata
- Falls back to `PIL.Image._getexif()` for basic tags if ExifTool is unavailable
- Merges parsed JSON or Pillow EXIF into a single `dict`
- Provides `display_metadata()` to format and print tag names and values

---

### Unified Parser

**src/metadata/parser.py**

A Python class `MetadataParser` that:

- Defines a helper `_parse_key_value(line)` using a single regex for `Key: Value` extraction
- Implements `parse_exif()`, `parse_zsteg()`, `parse_steghide()`, and `parse_binwalk()` methods
- Each accepts either raw multiline text or a prebuilt `dict`
- Returns a normalized `dict` schema for each module
- Supports parsing Binwalk signatures into a `{'Signatures': [...]}` structure

---

### Main Orchestration

**src/main.py**

- Introduced `run_metadata_chain(file_path)` to:
  1. Run EXIF scraper + parse output
  2. Run Steghide scraper + parse output
  3. Run Binwalk scraper + parse output
  4. Print a combined summary of all parsed metadata

- Updated `terminal_mode()` to use `argparse`:
  - `file` positional argument
  - `--extract-binwalk` flag to enable extraction step
  - `--search-image` flag to trigger the reverse-image search stub

- Retained a menu in `main()` to choose between CLI and GUI (`startGUI()` placeholder)

---

## Steghide Usage and Format Notes

### Supported Cover Formats

Steghide can embed data into:

- **JPEG** (`.jpg`, `.jpeg`)
- **BMP3** (Windows 3.x BITMAPINFOHEADER–based `.bmp`)
- **WAV** and **AU** audio files

> **Note:** Newer “BMP V5” files (with a 124-byte header) are **not** supported:
> ```
> the bmp file "<file>.bmp" has a format that is not supported (biSize: 124).
> ```

---

### Converting an Unsupported BMP to BMP3

If your `.bmp` has a 124-byte header, convert it to the classic 40-byte BITMAPINFOHEADER format using ImageMagick:

```bash
# Install ImageMagick if needed
sudo apt update
sudo apt install imagemagick-6.q16

# Convert V5 BMP → classic BMP3
convert /path/to/input.bmp bmp3:/path/to/output_v3.bmp
```

Note: The `bmp3:` prefix forces a V3 header. `output_v3.bmp` is now compatible with Steghide.

---

### Core Steghide Commands

#### 1. Embed Data

```bash
steghide embed   -cf <coverfile>   -ef <payload>   -p <passphrase>   [-z <level>]    # compression level 1–9 (default: 1)
  [-e none]       # disable encryption
  [-K]            # omit CRC32 checksum
  [-f]            # overwrite existing files
```

**Example:**
```bash
echo "SECRET" > secret.txt
steghide embed -cf hoothoot_v3.bmp -ef secret.txt -p testpass -z 9 -f
```

#### 2. Inspect (Info)

```bash
steghide info -p <passphrase> <stegofile>
```

**Example:**
```bash
steghide info -p testpass hoothoot_v3.bmp
```

#### 3. Extract Data

```bash
steghide extract   -sf <stegofile>   [-p <passphrase>]   [-xf <outfile>]   [-f]            # overwrite existing output file
```

**Examples:**
```bash
# Default extraction
steghide extract -sf hoothoot_v3.bmp -p testpass

# Custom filename
steghide extract -sf hoothoot_v3.bmp -p testpass -xf recovered.txt

# Force overwrite
steghide extract -sf hoothoot_v3.bmp -p testpass -f
```

---

### Quick Round-Trip Example

```bash
# 1) (If needed) Convert PNG → BMP3
convert input.png bmp3:input_v3.bmp

# 2) Embed
echo "HELLO_CTF" > payload.txt
steghide embed -cf input_v3.bmp -ef payload.txt -p mypass -f

# 3) Inspect
steghide info -p mypass input_v3.bmp

# 4) Extract
steghide extract -sf input_v3.bmp -p mypass -f
```

> Tip: Always verify your cover file’s format before embedding. Use `file input.bmp` or open with a hex viewer to check the DIB header size. Steghide requires the classic 40-byte header for BMPs.

---

## Project Status

All core scrapers (EXIF via ExifTool/Pillow, Zsteg, Binwalk) and their Python wrappers are fully implemented and parsed by the unified regex-based parser. The main entrypoint chains EXIF → Steghide → Binwalk with CLI/GUI options.

**Note:** The Steghide wrapper needs minor syntax fixes under WSL to align its flag handling.


# Docker

## 1. Prerequisites

Make sure you have Docker installed on your system.

- For Windows or macOS, get **Docker Desktop**.
- For Linux, follow the official **Docker Engine** installation guide.

> **Note on `sudo`**: The commands below assume you have completed the [official Docker post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) for Linux, which allow you to run Docker without `sudo`. If you get a `permission denied` error, you can either prefix the commands with `sudo` or follow that guide to add your user to the `docker` group.

## 2. First-Time Setup (Build the Image)

Before you can run the application, you need to build the Docker image. This command downloads all the dependencies and sets up the environment defined in the `Dockerfile`.

From the project's root directory (`~/BigSister`), run:

```bash
docker compose build
```

## 3. Running the Tool

To run the tool, you need to use this command:

```bash
docker compose run --rm bigsister
```

There are 2 different versions of the app (terminal and GUI), read instructions below.

### Terminal App

When starting the application, you will be given two choices:

```bash
=== Big Sister - Metadata and Image Analysis Tool ===
Choose your interface:
1. GUI (Graphical User Interface)
2. Terminal (Command Line Interface)
Enter 1 or 2:
```

If you want to use **terminal option (2)**, you need to specify the file, like this:

```bash
docker compose run --rm bigsister /downloads/example_image.jpeg
```

### GUI App

- **Linux**

  Before running the app, make sure to run:

  ```bash
  xhost +local:
  ```

  With this commad you are adding non-network local connections to your access control list. Without this command you will see `Authorization required, but no authorization protocol specified`.

  Then, you can run as usual:

  ```bash
  docker compose run --rm bigsister
  ```

- **Windows**

  Use [x11docker](https://github.com/mviereck/x11docker)

- **MacOS**

  Use [distrobox](https://github.com/89luca89/distrobox)

## 4. Get access to the files

By default Docker containers do not get access to the file system of the host.

In order to pass files to be analyzed, you need to map Docker volumes in the `docker-compose.yml`. We map current directory and `~/Downloads` by default:

```bash
volumes:
      # Map X11 file for GUI
      - /tmp/.X11-unix:/tmp/.X11-unix
      # Make current host directory available within container as /app
      - .:/app
      # Example for making other directories available
      - ~/Downloads:/Downloads
```

With this setup you can reference files, like this:

```bash
# A file in current directory
$ docker compose run --rm bigsister image.png
# Another file in host's ~/Downloads
$ docker compose run --rm bigsister /Downloads/another.png
```

You can add more directories by modifying `docker-compose.yml`
