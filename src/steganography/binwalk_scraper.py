#!/usr/bin/env python3
"""
binwalk_scraper.py

Scrapes file signatures and extraction info using the Binwalk CLI.
"""

import subprocess
import platform
import shlex
import re
from pathlib import Path


class BinwalkScraper:
    def __init__(self, binwalk_path: str = None):
        """
        Initialize the BinwalkScraper.

        Args:
            binwalk_path (str): Custom path or command for Binwalk. If None, auto-select based on platform.
        """
        if binwalk_path:
            self.binwalk_path = binwalk_path
        elif platform.system() == "Windows":
            self.binwalk_path = "wsl binwalk"
        else:
            self.binwalk_path = "binwalk"

    def _convert_to_wsl_path(self, path: Path) -> str:
        """
        Convert a Windows-style path to WSL (/mnt/c/...) format, if needed.

        Args:
            path (Path): The original file path.

        Returns:
            str: Converted path string suitable for WSL binwalk.
        """
        if platform.system() == "Windows" and self.binwalk_path.startswith("wsl"):
            resolved = path.resolve()
            drive = resolved.drive[0].lower()  # 'C:...' → 'c'
            wsl_path = f"/mnt/{drive}{resolved.as_posix()[2:]}"  # strip 'C:'
            return wsl_path
        return str(path)

    def scrape(self, file_path: str, extract: bool = False, extract_dir: str = None) -> dict:
        """
        Run binwalk on the file. If extract=True, will extract embedded data.

        Args:
            file_path (str): Path to the file to analyze.
            extract (bool): Whether to run with -e (extract) flag.
            extract_dir (str, optional): Directory to extract into.

        Returns:
            dict: Parsed scan results, plus raw output and extraction dir if used.
        """
        file = Path(file_path)
        if not file.exists():
            return {"Error": f"File not found: {file_path}"}

        cmd = shlex.split(self.binwalk_path)
        if extract:
            cmd.append("-e")
            if extract_dir:
                cmd.extend(["-C", str(extract_dir)])

        # Convert path for WSL if needed
        cmd.append(self._convert_to_wsl_path(file))

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            raw = result.stdout
        except subprocess.CalledProcessError as e:
            raw = (e.stdout or "") + "\n" + (e.stderr or "")

        data = self._parse_output(raw)
        data["RawOutput"] = raw
        if extract:
            outdir = extract_dir or f"{file.name}.extracted"
            data["Extraction Directory"] = str(Path(outdir))

        return data

    def _parse_output(self, output: str) -> dict:
        """
        Parse binwalk scan output into structured signatures.

        Args:
            output (str): Raw stdout/stderr from binwalk.

        Returns:
            dict: {'Signatures': [ {'Offset':..., 'Description':...}, ... ] }
        """
        signatures = []
        # Match lines with decimal offset, hex offset, then description
        line_pattern = re.compile(r'^\s*(\d+)\s+0x[0-9A-Fa-f]+\s+(.+)$')

        for line in output.splitlines():
            m = line_pattern.match(line)
            if m:
                signatures.append({
                    "Offset": m.group(1),
                    "Description": m.group(2).strip()
                })

        return {"Signatures": signatures}

    def display_metadata(self, data: dict):
        """
        Pretty-print the binwalk results.

        Args:
            data (dict): Output from scrape(), including 'Signatures' etc.
        """
        sigs = data.get("Signatures", [])
        separator = "=" * 60

        print("\n" + separator)
        print(" BINWALK SIGNATURES ".center(60, "-"))
        print(separator)
        if sigs:
            for sig in sigs:
                print(f"{sig['Offset']:>10} | {sig['Description']}")
        else:
            print("No signatures found.")
        if "Extraction Directory" in data:
            print("\nExtraction Directory:", data["Extraction Directory"])
        print(separator)
