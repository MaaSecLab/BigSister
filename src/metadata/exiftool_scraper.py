"""
exiftool_scraper.py

Scrapes image metadata using the external ExifTool binary (preferred)
and falls back to Pillow for basic info if ExifTool is unavailable.
"""

import subprocess
import json
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS


class MetadataScraper:
    def __init__(self, exiftool_path: str = "exiftool"):
        """
        Initialize the MetadataScraper.

        Args:
            exiftool_path (str): Path to the ExifTool executable.
        """
        self.exiftool_path = exiftool_path

    def scrape(self, file_path: str) -> dict:
        """
        Scrape metadata from the given file path.

        This will first try ExifTool (with JSON output). If that fails,
        it will fall back to PIL’s internal EXIF parser for core tags.

        Args:
            file_path (str): Path to the image file to analyze.

        Returns:
            dict: Dictionary containing all scraped metadata.
        """
        file = Path(file_path)
        if not file.exists():
            return {"Error": f"File not found: {file_path}"}

        metadata = {}
        # --- 1) Try ExifTool JSON ---
        try:
            # "-j" => JSON output, "-n" => numeric values where appropriate
            result = subprocess.run(
                [self.exiftool_path, "-j", "-n", str(file)],
                capture_output=True,
                check=True,
                text=True,
            )
            # ExifTool returns a JSON array; we take the first element
            data = json.loads(result.stdout)
            if isinstance(data, list) and data:
                metadata.update(data[0])
            else:
                metadata["Warning"] = "ExifTool returned no data"
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            # Fallback to PIL if ExifTool not found or errors out
            metadata["ExifTool Error"] = str(e)
            metadata.update(self._pillow_fallback(file_path))

        return metadata

    def _pillow_fallback(self, file_path: str) -> dict:
        """
        Fallback metadata extraction via Pillow.

        Args:
            file_path (str): Path to the image file.

        Returns:
            dict: Basic metadata from Pillow.
        """
        info = {}
        try:
            img = Image.open(file_path)
            info = {
                "Filename": img.filename,
                "Image Size": f"{img.width}x{img.height}",
                "Image Format": img.format,
                "Image Mode": img.mode,
            }
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    # decode bytes if necessary
                    if isinstance(value, bytes):
                        try:
                            value = value.decode(errors="ignore")
                        except Exception:
                            pass
                    info[tag] = value
        except Exception as e:
            info = {"Pillow Error": f"Failed to read image: {e}"}
        return info

    def display_metadata(self, metadata: dict):
        """
        Print metadata in a human-readable table format.

        Args:
            metadata (dict): Dictionary containing metadata to display.
        """
        if not metadata:
            print("No metadata found.")
            return

        # Compute padding based on longest key
        key_width = max(len(str(k)) for k in metadata.keys()) + 2
        separator = "=" * (key_width + 50)

        print("\n" + separator)
        print(" METADATA ".center(key_width + 50, "-"))
        print(separator)
        for k, v in sorted(metadata.items()):
            print(f"{k:{key_width}}: {v}")
        print(separator)
