# Using Steghide with BMP and JPEG Covers

## Supported Cover Formats

Steghide can embed data into:
- **JPEG** (`.jpg`, `.jpeg`)
- **BMP3** (Windows 3.x BITMAPINFOHEADER–based `.bmp`)
- **WAV** and **AU** audio files

> **Note:** Newer “BMP V5” files (with a 124-byte header) are **not** supported:
> ```
> the bmp file "<file>.bmp" has a format that is not supported (biSize: 124).
> ```

---

## Converting an Unsupported BMP to BMP3

If your `.bmp` has a 124-byte header, convert it to the classic 40-byte BITMAPINFOHEADER format using ImageMagick:

```bash
# Install ImageMagick if needed
sudo apt update
sudo apt install imagemagick-6.q16

# Convert V5 BMP → classic BMP3
convert /path/to/input.bmp \
        bmp3:/path/to/output_v3.bmp


Note: The bmp3: prefix forces a V3 header.
output_v3.bmp is now compatible with Steghide.


Core Steghide Commands
1. Embed Data

steghide embed \
  -cf <coverfile> \
  -ef <payload> \
  -p <passphrase> \
  [-z <level>]    # compression level 1–9 (default: 1)
  [-e none]       # disable encryption
  [-K]            # omit CRC32 checksum
  [-f]            # overwrite existing files


Example
echo "SECRET" > secret.txt
steghide embed \
  -cf hoothoot_v3.bmp \
  -ef secret.txt \
  -p testpass \
  -z 9 \
  -f

2. Inspect (Info)
steghide info \
  [-p <passphrase>] \
  <stegofile>

If data was encrypted, include -p.
Outputs capacity, embedded filename, size, encryption/compression info.

Example
steghide info -p testpass hoothoot_v3.bmp


3. Extract Data
steghide extract \
  -sf <stegofile> \
  [-p <passphrase>] \
  [-xf <outfile>] \
  [-f]            # overwrite existing output file
-sf specifies the stego file.

-xf names the extracted file (defaults to original name).

-f overwrites any existing output.

Examples
# Default extraction
steghide extract -sf hoothoot_v3.bmp -p testpass

# Custom filename
steghide extract -sf hoothoot_v3.bmp -p testpass -xf recovered.txt

# Force overwrite
steghide extract -sf hoothoot_v3.bmp -p testpass -f


Quick Round-Trip Example
# 1) (If needed) Convert PNG → BMP3
convert input.png bmp3:input_v3.bmp

# 2) Embed
echo "HELLO_CTF" > payload.txt
steghide embed \
  -cf input_v3.bmp \
  -ef payload.txt \
  -p mypass \
  -f

# 3) Inspect
steghide info -p mypass input_v3.bmp

# 4) Extract
steghide extract -sf input_v3.bmp -p mypass -f


Tip: Always verify your cover file’s format before embedding. Use file input.bmp or open with a hex viewer to check the DIB header size. Steghide requires the classic 40-byte header for BMPs.


