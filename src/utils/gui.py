import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import sys
import os

# Add the parent directory to the Python path to enable relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metadata.exiftool_scraper import MetadataScraper
from metadata.parser import MetadataParser
from iris.image_search import ImageSearch

def openImage(filename):
    if filename:
        try:
            # Create a new window for the image
            image_window = Toplevel(m)
            image_window.title(f"Image Viewer - {filename.split('/')[-1]}")
            
            # Open and resize image if needed
            img = Image.open(filename)
            
            # Resize image if it's too large
            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Create label to display image
            img_label = Label(image_window, image=photo)
            img_label.image = photo  # Keep reference
            img_label.pack()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")

def analyzeMetadata(filename):
    """Analyze metadata for the selected file and display it in a new window."""
    if filename:
        try:
            # Initialize the metadata scraper
            scraper = MetadataScraper()
            
            # Scrape metadata from the file
            metadata_output = scraper.scrape(filename)
            
            # Create a new window for metadata display
            metadata_window = Toplevel(m)
            metadata_window.title(f"Metadata Analysis - {filename.split('/')[-1]}")
            metadata_window.geometry("800x600")
            
            # Create a scrolled text widget for metadata display
            text_widget = scrolledtext.ScrolledText(metadata_window, wrap=tkinter.WORD, width=80, height=30)
            text_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            # Format and display metadata
            text_widget.insert(tkinter.END, "=== Metadata Information ===\n\n")
            
            if "Error" in metadata_output:
                text_widget.insert(tkinter.END, f"Error: {metadata_output['Error']}\n")
            else:
                for label, value in metadata_output.items():
                    text_widget.insert(tkinter.END, f"{label:25}: {value}\n")
            
            text_widget.insert(tkinter.END, "\n" + "=" * 50)
            
            # Make text widget read-only
            text_widget.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not analyze metadata: {str(e)}")

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/home", title = "Select a File",
                                filetypes = (("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.ico *.svg"),
                                           ("JPEG files", "*.jpg *.jpeg"),
                                           ("PNG files", "*.png"),
                                           ("GIF files", "*.gif"),
                                           ("All files", "*.*")))
    
    if filename:
        label_file_explorer.configure(text="File Opened: " + filename)
        global current_file
        current_file = filename
        
        # Enable analysis buttons
        button_view_image.configure(state='normal')
        button_analyze_metadata.configure(state='normal')

def viewCurrentImage():
    """View the currently selected image."""
    if current_file:
        openImage(current_file)

def analyzeCurrentMetadata():
    """Analyze metadata for the currently selected image."""
    if current_file:
        analyzeMetadata(current_file)

def startGUI():
    global label_file_explorer
    global m
    global current_file
    global button_view_image
    global button_analyze_metadata
    
    current_file = None
    m = tkinter.Tk()

    m.title('Big Sister - OSINT challenge automation tool')
    m.geometry("700x500")
    m.config(background="lightblue")

    # Title label
    title_label = Label(m, text="Big Sister - Image Metadata Analysis Tool", 
                       font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
    title_label.pack(pady=10)

    # File explorer label
    label_file_explorer = Label(m, text="Select an image file to analyze", 
                               width=80, height=4, fg="blue", bg="lightblue")
    label_file_explorer.pack(pady=10)

    # Browse button
    button_explore = Button(m, text="Browse Files", command=browseFiles, 
                           font=("Arial", 12), bg="white", fg="blue", 
                           width=20, height=2)
    button_explore.pack(pady=10)

    # Frame for action buttons
    button_frame = Frame(m, bg="lightblue")
    button_frame.pack(pady=20)

    # View image button
    button_view_image = Button(button_frame, text="View Image", command=viewCurrentImage,
                              font=("Arial", 12), bg="lightgreen", fg="black",
                              width=20, height=2, state='disabled')
    button_view_image.pack(side=LEFT, padx=10)

    # Analyze metadata button
    button_analyze_metadata = Button(button_frame, text="Analyze Metadata", command=analyzeCurrentMetadata,
                                    font=("Arial", 12), bg="lightcoral", fg="black",
                                    width=20, height=2, state='disabled')
    button_analyze_metadata.pack(side=LEFT, padx=10)

    # Exit button
    button_exit = Button(m, text="Exit", command=m.quit, 
                        font=("Arial", 12), bg="lightgray", fg="red",
                        width=20, height=2)
    button_exit.pack(pady=20)

    m.mainloop()

if __name__ == "__main__":
    startGUI()