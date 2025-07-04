class MetadataScraper:
    def __init__(self):
        """Initialize the MetadataScraper."""
        pass
    
    def scrape(self, file_path):
        """
        Scrape metadata from the given file path.
        
        Args:
            file_path (str): Path to the image file to analyze
            
        Returns:
            dict: Dictionary containing all scraped metadata
        """
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        try:
            # Open the image file
            image = Image.open(file_path)
            
            # Basic image information
            info_dict = {
                "Filename": image.filename,
                "Image Size": image.size,
                "Image Height": image.height,
                "Image Width": image.width,
                "Image Format": image.format,
                "Image Mode": image.mode,
            }
            
            # Get EXIF data
            exifdata = image._getexif()
            
            # Parse EXIF data if available
            if exifdata:
                for tag_id in exifdata:
                    # Get the tag name, instead of human unreadable tag id
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    # Decode bytes if necessary
                    if isinstance(data, bytes):
                        data = data.decode()
                    info_dict[tag] = data
            
            return info_dict
            
        except Exception as e:
            return {"Error": f"Failed to scrape metadata: {str(e)}"}
    
    def display_metadata(self, metadata):
        """
        Display metadata in a formatted way.
        
        Args:
            metadata (dict): Dictionary containing metadata to display
        """
        print("\n=== Metadata Information ===")
        for label, value in metadata.items():
            print(f"{label:25}: {value}")
        print("=" * 50)