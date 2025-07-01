class MetadataScraper:
    def __init__(self):
        self.tools = {
            'exiftool': 'exiftool',
            'zsteg': 'zsteg',
            'steghide': 'steghide',
            'binwalk': 'binwalk'
        }

    def call_tool(self, tool, file_path):
        import subprocess
        try:
            result = subprocess.run([self.tools[tool], file_path], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Error calling {tool}: {e}")
            return None

    def scrape_metadata(self, file_path):
        metadata = {}
        for tool in self.tools.keys():
            output = self.call_tool(tool, file_path)
            if output:
                metadata[tool] = output
        return metadata