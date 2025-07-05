"""
parser.py

Unified metadata parser for EXIF, Zsteg, Steghide, and Binwalk outputs.
"""

import re


class MetadataParser:
    """
    Parses raw and structured outputs from various metadata scrapers into
a consistent Python dictionary schema.
    """
    def __init__(self):
        """
        Initialize a MetadataParser. No state is stored between parse calls.
        """
        pass



    @staticmethod
    def _parse_key_value(line: str):
        """
        Extract a key and value from a "Key: Value" formatted string.
        Returns a tuple (key, value) or (None, None) if no match.
        """
        match = re.match(r'^\s*([^:]+?)\s*:\s*(.+)$', line)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None, None
    


    def parse_exif(self, exif_output):
        """
        Parse EXIF metadata.

        Accepts either:
        - A dict from an EXIF scraper (e.g., exiftool JSON or Pillow fallback)
        - A raw multiline string in "Key: Value" format

        Returns:
            dict: Parsed EXIF fields and values
        """
        parsed = {}
        if isinstance(exif_output, dict):
            # Copy to avoid mutating original
            return exif_output.copy()

        # Raw string input
        for line in exif_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed
    


    def parse_zsteg(self, zsteg_output):
        """
        Parse Zsteg output (raw text or dict).

        Returns:
            dict: Parsed key/value pairs
        """
        parsed = {}
        if isinstance(zsteg_output, dict):
            return zsteg_output.copy()
        for line in zsteg_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed
    


    def parse_steghide(self, steghide_output):
        """
        Parse Steghide "info" output (raw text or dict).

        Returns:
            dict: Parsed steghide metadata fields
        """
        parsed = {}
        if isinstance(steghide_output, dict):
            return steghide_output.copy()
        for line in steghide_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed



    def parse_binwalk(self, binwalk_output):
        """
        Parse Binwalk scan or extract output.

        Accepts either:
        - A dict with key 'Signatures' (as from a BinwalkScraper)
        - A raw multiline string

        Returns:
            dict: {'Signatures': [ {'Offset': ..., 'Description': ...}, ... ]}
        """
        # If already structured
        if isinstance(binwalk_output, dict) and 'Signatures' in binwalk_output:
            # Copy list of dicts
            return {'Signatures': list(binwalk_output['Signatures'])}

        # Raw text input
        signatures = []
        for line in binwalk_output.splitlines():
            m = re.match(r'^\s*([0-9A-Fa-fx]+)\s*:\s*(.+)$', line)
            if m:
                signatures.append({
                    'Offset': m.group(1),
                    'Description': m.group(2).strip()
                })
        return {'Signatures': signatures}
    
    

    def get_metadata(self):
        """
        For compatibility: returns an empty dict (no persistent state).
        """
        return {}
