import tkinter
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


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

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/home", title = "Select a File",
                                filetypes = (("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.ico *.svg"),
                                           ("JPEG files", "*.jpg *.jpeg"),
                                           ("PNG files", "*.png"),
                                           ("GIF files", "*.gif"),
                                           ("All files", "*.*")))
    
    if filename:
        label_file_explorer.configure(text="File Opened: " + filename)
        openImage(filename)


def startGUI():
    global label_file_explorer
    global m
    m = tkinter.Tk()

    m.title('Big Sister File Explorer')

    m.geometry("700x400")

    m.config(background="lightblue")

    label_file_explorer = Label(m, text="File Explorer using Tkinter", width=100, height=4,
                                fg="blue")

    button_explore = Button(m, text = "Browse Files", command = browseFiles)

    button_exit = Button(m, text = "Exit", command = exit)

    label_file_explorer.pack()
    button_explore.pack()
    button_exit.pack()

    m.mainloop()

if __name__ == "__main__":
    startGUI()