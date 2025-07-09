#!/usr/bin/env python3
"""
steghide_scraper.py

Scrapes steganography metadata from images using the Steghide CLI,
with a passphrase derived from common EXIF fields if none is provided.
"""

import subprocess
from pathlib import Path
import re

from metadata.exiftool_scraper import MetadataScraper


class SteghideScraper:
    _PASS_TAG_CANDIDATES = [
        "UserComment", "ImageDescription", "Comment", "Artist", "Software"
    ]

    def __init__(self, steghide_path: str = "steghide"):
        self.steghide_path = steghide_path

    def scrape(self, file_path: str, passphrase: str = None) -> dict:
        file = Path(file_path)
        if not file.exists():
            return {"Error": f"File not found: {file_path}"}

        derived = {}
        if passphrase is None:
            exif = MetadataScraper().scrape(file_path)
            for tag in self._PASS_TAG_CANDIDATES:
                if tag in exif:
                    candidate = exif[tag]
                    if isinstance(candidate, str) and candidate.strip():
                        passphrase = candidate.strip()
                        derived["DerivedPassphrase"] = {tag: passphrase}
                        break

        # Always provide a passphrase (even if empty) to prevent interactive prompt
        cmd = [self.steghide_path, "info", "-p", passphrase if passphrase else "", str(file)]

        try:
            # Avoid terminal errors by feeding a newline to stdin
            result = subprocess.run(
                cmd,
                input="\n",
                capture_output=True,
                text=True,
                check=True,
            )
            raw = result.stdout
        except subprocess.CalledProcessError as e:
            raw_output = (e.stdout or "") + "\n" + (e.stderr or "")
            if "could not extract any data with that passphrase" in raw_output:
                raw_output += (
                "\n Steghide could not extract any data using this passphrase.\n"
                "👉 CTF Tip: Check EXIF fields like Artist, Comment, or challenge hints for possible passwords. You can also try running this script with -p <passphrase> to test known values.\n"
                )
        raw = raw_output


        parsed = self._parse_output(raw)
        if "DerivedPassphrase" in derived:
            parsed["DerivedPassphrase"] = derived["DerivedPassphrase"]
        return parsed

    def _parse_output(self, output: str) -> dict:
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
        description="Scrape Steghide metadata from an image file, deriving passphrase from EXIF if needed."
    )
    parser.add_argument("file", help="Path to the file to inspect")
    parser.add_argument("-p", "--passphrase", help="Explicit passphrase for steghide data", default=None)
    args = parser.parse_args()

    scraper = SteghideScraper()
    meta = scraper.scrape(args.file, passphrase=args.passphrase)
    scraper.display_metadata(meta)
