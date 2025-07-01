import sys
from metadata.scraper import MetadataScraper
from metadata.parser import MetadataParser
from iris.image_search import ImageSearch

def main():
    # Initialize the metadata scraper and parser
    scraper = MetadataScraper()
    parser = MetadataParser()

    # Get user input for the file to analyze
    file_path = input("Enter the path of the file to analyze: ")

    # Scrape metadata from the file
    metadata_output = scraper.scrape(file_path)

    # Parse the scraped metadata
    parsed_data = parser.parse(metadata_output)

    # Display the parsed information
    print("Parsed Metadata:")
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

    # Initialize the image search module
    image_search = ImageSearch()

    # Get user input for the image to search
    image_path = input("Enter the path of the image to search: ")

    # Perform reverse image search
    search_results = image_search.search(image_path)

    # Display the search results
    print("Image Search Results:")
    for result in search_results:
        print(result)

if __name__ == "__main__":
    main()