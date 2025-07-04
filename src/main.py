import sys
from metadata.exiftool_scraper import MetadataScraper
from metadata.parser import MetadataParser
from iris.image_search import ImageSearch
from utils.terminal import terminal
from utils.gui import startGUI

def main():
    print("=== Big Sister - Metadata and Image Analysis Tool ===")
    print("Choose your interface:")
    print("1. GUI (Graphical User Interface)")
    print("2. Terminal (Command Line Interface)")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            startGUI()
            break
        elif choice == '2':
            terminal()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    

if __name__ == "__main__":
    main()