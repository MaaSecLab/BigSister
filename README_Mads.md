# Big Sister

This README summarizes the work completed so far on the Big Sister project, including:

* Steghide modules (shell script and Python scraper)
* Binwalk modules (shell script and Python scraper)
* ExifTool scraper updates
* Unified parser updates
* Main orchestration updates

## Steghide Module

**scripts/runsteghide.sh**

A Bash wrapper for the `steghide` CLI that supports:

* `--info` mode to display embedded data metadata
* `--passphrase` (`-p`) to supply a passphrase when required
* `--output-dir` (`-o`) to specify where extracted files land

```bash
runsteghide.sh [--info] [-p PASS] [-o OUTPUT_DIR] <file>
```

**src/steganography/steghide\_scraper.py**

A Python class `SteghideScraper` that:

* Invokes `steghide info -v` or `steghide extract` via `subprocess`
* Accepts an optional `passphrase` argument
* Parses `Key: Value` lines using a regex helper
* Returns a `dict` of metadata fields or raw output
* Provides `display_metadata()` to print results in human‑readable form

## Binwalk Module

**scripts/runbinwalk.sh**

A Bash wrapper for the `binwalk` CLI that supports:

* Signature scanning (default mode)
* Extraction (`-e` / `--extract`) to pull out embedded files
* Custom extraction directory (`-d` / `--output-dir`)

```bash
runbinwalk.sh [-e] [-d OUTPUT_DIR] <file>
```

**src/steganography/binwalk\_scraper.py**

A Python class `BinwalkScraper` that:

* Invokes `binwalk` or `binwalk -e -C` via `subprocess`
* Returns a `dict` with a `Signatures` list of `{Offset, Description}`
* Includes raw output in the returned dict
* Provides `display_metadata()` to print signature tables and extraction info

## ExifTool Scraper Updates

**src/metadata/exiftool\_scraper.py**

A Python class `MetadataScraper` that:

* Attempts to call `exiftool -j -n` via `subprocess` to get full JSON metadata
* Falls back to `PIL.Image._getexif()` for basic tags if ExifTool is unavailable
* Merges parsed JSON or Pillow EXIF into a single `dict`
* Provides `display_metadata()` to format and print tag names and values

## Unified Parser Updates

**src/metadata/parser.py**

A Python class `MetadataParser` that:

* Defines a helper `_parse_key_value(line)` using a single regex for `Key: Value` extraction
* Implements `parse_exif()`, `parse_zsteg()`, `parse_steghide()`, and `parse_binwalk()` methods

  * Each accepts either raw multiline text or a prebuilt `dict`
  * Returns a normalized `dict` schema for each module
* Supports parsing Binwalk signatures into a `{'Signatures': [...]}` structure

## Main Orchestration Updates

**src/main.py**

* Introduced `run_metadata_chain(file_path)` to:

  1. Run EXIF scraper + parse output
  2. Run Steghide scraper + parse output
  3. Run Binwalk scraper + parse output
  4. Print a combined summary of all parsed metadata
* Updated `terminal_mode()` to use `argparse`:

  * `file` positional argument
  * `--extract-binwalk` flag to enable extraction step
  * `--search-image` flag to trigger the reverse-image search stub
* Retained a menu in `main()` to choose between CLI and GUI (`startGUI()` placeholder)

---

All modules are now wired together through `main.py`, providing a clear metadata “scraper → parser → output” flow for images and files.


After testing:

All core scrapers (EXIF via ExifTool/Pillow, Zsteg, Binwalk) and their Python wrappers are fully implemented and parsed by the unified regex-based parser, and the main entrypoint chains EXIF → Steghide → Binwalk with CLI/GUI options. Only the Steghide wrapper still needs its flag syntax aligned under WSL before it behaves correctly.


Finished steghide - check Steghide_Use.md

