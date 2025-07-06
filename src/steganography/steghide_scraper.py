#!/usr/bin/env python3
"""
steghide_scraper.py

Scrapes steganography metadata from images using the Steghide CLI,
with a passphrase derived from common EXIF fields if none is provided.
"""

import subprocess
from pathlib import Path
import re

# for deriving a passphrase from EXIF, if none supplied
from metadata.exiftool_scraper import MetadataScraper


class SteghideScraper:
    # EXIF tags we’ll check for potential passphrases, in priority order
    _PASS_TAG_CANDIDATES = [
        "UserComment", "ImageDescription", "Comment", "Artist", "Software"
    ]

    def __init__(self, steghide_path: str = "steghide"):
        """
        Initialize the SteghideScraper.

        Args:
            steghide_path (str): Path to the Steghide executable.
        """
        self.steghide_path = steghide_path

    def scrape(self, file_path: str, passphrase: str = None) -> dict:
        """
        Scrape steghide metadata from the given file path.

        If no passphrase is provided, attempts to derive one
        from EXIF metadata before calling `steghide info`.

        Args:
            file_path (str): Path to the steg-embedded file to analyze.
            passphrase (str, optional): Explicit passphrase override.

        Returns:
            dict: Dictionary containing:
              - DerivedPassphrase (if any)
              - All steghide info fields
              - On extract mode, any extraction data
        """
        file = Path(file_path)
        if not file.exists():
            return {"Error": f"File not found: {file_path}"}

        derived = {}
        # If user didn't supply a passphrase, peek at EXIF for clues
        if passphrase is None:
            exif = MetadataScraper().scrape(file_path)
            for tag in self._PASS_TAG_CANDIDATES:
                if tag in exif:
                    candidate = exif[tag]
                    # only use non-empty strings
                    if isinstance(candidate, str) and candidate.strip():
                        passphrase = candidate.strip()
                        derived["DerivedPassphrase"] = {tag: passphrase}
                        break

        # build info command
        # new
        cmd = [self.steghide_path, "info"]
        if passphrase:
            cmd += ["-p", passphrase]
        cmd += [str(file)]

        try:
            # always send at least a newline so steghide won’t hang waiting for stdin
            result = subprocess.run(
                cmd,
                input=(passphrase or "") + "\n",
                capture_output=True,
                text=True,
                check=True,
            )
            raw = result.stdout
        except subprocess.CalledProcessError as e:
            raw = (e.stdout or "") + "\n" + (e.stderr or "")

        parsed = self._parse_output(raw)
        # merge derived passphrase if found
        if "DerivedPassphrase" in derived:
            parsed["DerivedPassphrase"] = derived["DerivedPassphrase"]
        return parsed

    def _parse_output(self, output: str) -> dict:
        """
        Parse the text output from `steghide info` into a structured dict.

        Args:
            output (str): Raw stdout/stderr from the steghide command.

        Returns:
            dict: Parsed key-value metadata.
        """
        metadata = {}
        kv_pattern = re.compile(r'^\s*([^:]+?):\s*(.+)$')
        for line in output.splitlines():
            m = kv_pattern.match(line)
            if m:
                metadata[m.group(1).strip()] = m.group(2).strip()

        if not metadata:
            metadata["RawOutput"] = output.strip()
        return metadata

    def display_metadata(self, metadata: dict):
        """
        Print steghide metadata in a human-readable format.

        Args:
            metadata (dict): Dictionary containing metadata to display.
        """
        if not metadata:
            print("No steghide data found.")
            return

        key_width = max(len(str(k)) for k in metadata.keys()) + 2
        separator = "-" * (key_width + 40)

        print("\n" + separator)
        print(" STEGHIDE METADATA ".center(key_width + 40, "-"))
        print(separator)
        for k, v in sorted(metadata.items()):
            print(f"{k:{key_width}}: {v}")
        print(separator)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape Steghide metadata from an image file, "
                    "deriving passphrase from EXIF if needed."
    )
    parser.add_argument("file", help="Path to the file to inspect")
    parser.add_argument(
        "-p", "--passphrase", help="Explicit passphrase for steghide data", default=None
    )
    args = parser.parse_args()

    scraper = SteghideScraper()
    meta = scraper.scrape(args.file, passphrase=args.passphrase)
    scraper.display_metadata(meta)
