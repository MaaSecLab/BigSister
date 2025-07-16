"""
main.py

Big Sister - Orchestrates metadata scrapers, parser, and reverse-image search
via either a GUI or terminal interface.
"""

import sys
from pathlib import Path

# Metadata scrapers
from metadata.exiftool_scraper import MetadataScraper
from steganography.steghide_scraper import SteghideScraper
from steganography.binwalk_scraper import BinwalkScraper

# Unified parser
from metadata.parser import MetadataParser

# Reverse-image search
from iris.image_search import ImageSearchIRIS

# Interfaces
from utils.gui import startGUI


def run_metadata_chain(file_path: str) -> dict:
    """
    Run the full metadata scraping → parsing chain on the given file.
    Returns a dict of combined parsed metadata.
    """
    parser = MetadataParser()
    combined = {}



    # 1) EXIFTool (with Pillow fallback)
    exif_scraper = MetadataScraper()
    raw_exif = exif_scraper.scrape(file_path)
    print("\n[ Raw EXIFTool Output ]")
    exif_scraper.display_metadata(raw_exif)

    exif_anomalies = exif_scraper.check_timestamp_anomaly(file_path, raw_exif)
    if exif_anomalies:
        print("\n[ EXIF Timestamp Anomalies ]")
        for k, v in exif_anomalies.items():
            print(f"{k:25}: {v}")

    parsed_exif = parser.parse_exif(raw_exif)
    print("\n[ Parsed EXIF Metadata ]")
    for k, v in parsed_exif.items():
        print(f"{k:25}: {v}")
    combined.update(parsed_exif)



    # 2) Steghide
    steg_scraper = SteghideScraper()
    raw_steg = steg_scraper.scrape(file_path)
    print("\n[ Raw Steghide Output ]")
    steg_scraper.display_metadata(raw_steg)
    parsed_steg = parser.parse_steghide(raw_steg)
    print("\n[ Parsed Steghide Metadata ]")
    for k, v in parsed_steg.items():
        print(f"{k:25}: {v}")
    combined.update(parsed_steg)



    # 3) Binwalk
    bw_scraper = BinwalkScraper()
    raw_bw = bw_scraper.scrape(file_path, extract=False)
    print("\n[ Raw Binwalk Output ]")
    bw_scraper.display_metadata(raw_bw)
    parsed_bw = parser.parse_binwalk(raw_bw)
    print("\n[ Parsed Binwalk Metadata ]")
    for k, v in parsed_bw.items():
        print(f"{k:25}: {v}")
    combined.update(parsed_bw)



    # 4) Summary
    print("\n" + "=" * 60)
    print("Combined Parsed Metadata".center(60))
    print("=" * 60)
    for k, v in combined.items():
        print(f"{k:25}: {v}")
    print("=" * 60)

    return combined




def run_image_search(file_path: str):
    """
    Perform a reverse-image search on the given file and display results.
    """
    searcher = ImageSearchIRIS()
    results = searcher.search_image(file_path)
    print("\n[ Reverse Image Search Results ]")
    searcher.display_results(results)


def terminal_mode():
    """
    Command-line interface for Big Sister.
    """
    import argparse

    ap = argparse.ArgumentParser(
        description="Big Sister – Metadata & Reverse-Image CTF Tool"
    )
    ap.add_argument(
        "file",
        help="Path to the file/image to analyze",
    )
    ap.add_argument(
        "--extract-binwalk",
        action="store_true",
        help="Also extract embedded files via binwalk",
    )
    ap.add_argument(
        "--search-image",
        action="store_true",
        help="Perform reverse-image search after metadata scraping",
    )
    args = ap.parse_args()

    fp = Path(args.file)
    if not fp.is_file():
        print(f"Error: '{args.file}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    # 1) Metadata scraping & parsing
    run_metadata_chain(str(fp))

    # 2) Optional binwalk extraction
    if args.extract_binwalk:
        print("\n[ Binwalk Extraction ]")
        bw_scraper = BinwalkScraper()
        bw_scraper.scrape(str(fp), extract=True, extract_dir=f"{fp.name}.extracted")

    # 3) Optional reverse-image search
    if args.search_image:
        run_image_search(str(fp))


def main():
    print("=== Big Sister - Metadata and Image Analysis Tool ===")
    print("Choose your interface:")
    print("1. GUI (Graphical User Interface)")
    print("2. Terminal (Command Line Interface)")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            startGUI()
            break
        elif choice == "2":
            terminal_mode()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
