"""
steghide_scraper.py

Scrapes steganography metadata from images using the Steghide CLI.
"""

import subprocess
from pathlib import Path
import re


class SteghideScraper:
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

        This calls `steghide info` on the file and parses its output.
        If the archive is passphrase-protected, you can provide it.

        Args:
            file_path (str): Path to the steg-embedded file to analyze.
            passphrase (str, optional): Passphrase for encrypted data.

        Returns:
            dict: Dictionary containing all scraped steghide metadata.
        """
        file = Path(file_path)
        if not file.exists():
            return {"Error": f"File not found: {file_path}"}

        cmd = [self.steghide_path, "info", "-v", str(file)]
        try:
            # If a passphrase is needed, pipe it to stdin
            result = subprocess.run(
                cmd,
                input=(passphrase + "\n") if passphrase else None,
                capture_output=True,
                text=True,
                check=True,
            )
            raw = result.stdout
        except subprocess.CalledProcessError as e:
            # steghide returns exit code 1 if no hidden data, or prompts for passphrase
            raw = e.stdout + "\n" + e.stderr

        return self._parse_output(raw)

    def _parse_output(self, output: str) -> dict:
        """
        Parse the text output from `steghide info` into a structured dict.

        Args:
            output (str): Raw stdout/stderr from the steghide command.

        Returns:
            dict: Parsed key-value metadata.
        """
        metadata = {}
        lines = output.splitlines()
        kv_pattern = re.compile(r'^\s*([^:]+?):\s*(.+)$')

        for line in lines:
            # Match lines like "embedding algorithm: aes-128"
            m = kv_pattern.match(line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                metadata[key] = val

        # Detect common messages
        if not metadata:
            # No key:value pairs found; capture entire output under a generic key
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

    parser = argparse.ArgumentParser(description="Scrape Steghide metadata from an image file.")
    parser.add_argument("file", help="Path to the file to inspect")
    parser.add_argument(
        "-p", "--passphrase", help="Passphrase for encrypted steghide data", default=None
    )
    args = parser.parse_args()

    scraper = SteghideScraper()
    meta = scraper.scrape(args.file, passphrase=args.passphrase)
    scraper.display_metadata(meta)
