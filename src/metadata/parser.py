class MetadataParser:
    def __init__(self):
        self.metadata = {}

    def parse_exif(self, exif_output):
        for line in exif_output.splitlines():
            if "User" in line or "Location" in line:
                key, value = line.split(":", 1)
                self.metadata[key.strip()] = value.strip()

    def parse_zsteg(self, zsteg_output):
        for line in zsteg_output.splitlines():
            if "User" in line or "Location" in line:
                key, value = line.split(":", 1)
                self.metadata[key.strip()] = value.strip()

    def parse_steghide(self, steghide_output):
        for line in steghide_output.splitlines():
            if "User" in line or "Location" in line:
                key, value = line.split(":", 1)
                self.metadata[key.strip()] = value.strip()

    def parse_binwalk(self, binwalk_output):
        for line in binwalk_output.splitlines():
            if "User" in line or "Location" in line:
                key, value = line.split(":", 1)
                self.metadata[key.strip()] = value.strip()

    def get_metadata(self):
        return self.metadata