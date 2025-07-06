#!/usr/bin/env python3
import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from metadata.parser import MetadataParser

# Make sure src/ is on the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metadata.exiftool_scraper import MetadataScraper
from iris.image_search import ImageSearch

class BigSisterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕵️‍♀️ Big Sister – OSINT Image Toolkit")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Apply a modern theme
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f4f7')
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), background='#f0f4f7', foreground='#333')
        style.configure('SubHeader.TLabel', font=('Helvetica', 12), background='#f0f4f7')
        style.configure('TButton', font=('Helvetica', 11), padding=6)
        style.map('TButton',
                  foreground=[('active', '#0052cc')],
                  background=[('active', '#cce0ff')])

        self.current_file = None

        self._build_layout()

    def _build_layout(self):
        # Top header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=20, pady=(20,10))
        ttk.Label(header, text="Big Sister", style='Header.TLabel').pack(side='left')
        ttk.Label(header, text="Image Metadata & Stego Analysis", style='SubHeader.TLabel').pack(side='left', padx=10)

        # Main PanedWindow
        paned = ttk.PanedWindow(self, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=20, pady=10)

        # Left: Controls
        ctrl_frame = ttk.Frame(paned, width=250)
        ctrl_frame.pack_propagate(False)
        paned.add(ctrl_frame, weight=1)

        # File chooser
        ttk.Label(ctrl_frame, text="Select Image", style='SubHeader.TLabel').pack(anchor='w', pady=(10,5))
        btn_browse = ttk.Button(ctrl_frame, text="📁 Browse…", command=self._browse_file)
        btn_browse.pack(fill='x')

        self.lbl_file = ttk.Label(ctrl_frame, text="No file selected", wraplength=230)
        self.lbl_file.pack(fill='x', pady=(5,15))

        # Action buttons
        ttk.Separator(ctrl_frame).pack(fill='x', pady=10)
        self.btn_view = ttk.Button(ctrl_frame, text="🖼 View Image", command=self._view_image, state='disabled')
        self.btn_view.pack(fill='x', pady=5)
        self.btn_meta = ttk.Button(ctrl_frame, text="🔍 Analyze Metadata", command=self._show_metadata, state='disabled')
        self.btn_meta.pack(fill='x', pady=5)
        self.btn_stego = ttk.Button(ctrl_frame, text="🕵️‍♂️ Stego Detect", command=self._show_stego, state='disabled')
        self.btn_stego.pack(fill='x', pady=5)

        # Right: Output notebook
        self.notebook = ttk.Notebook(paned)
        paned.add(self.notebook, weight=4)

        # Tab: metadata
        self.meta_tab = ttk.Frame(self.notebook)
        self.txt_meta = tk.Text(self.meta_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_meta.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.meta_tab, text="Metadata")

        # Tab: image
        self.img_tab = ttk.Frame(self.notebook)
        self.canvas = tk.Canvas(self.img_tab, background='#ddd')
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.img_tab, text="Image View")

        # Tab: stego results
        self.stego_tab = ttk.Frame(self.notebook)
        self.txt_stego = tk.Text(self.stego_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_stego.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.stego_tab, text="Stego Analysis")

    def _browse_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"), ("All files", "*.*")]
        )
        if not path:
            return
        self.current_file = path
        self.lbl_file.config(text=os.path.basename(path))
        for btn in (self.btn_view, self.btn_meta, self.btn_stego):
            btn.state(['!disabled'])

    def _view_image(self):
        if not self.current_file:
            return
        img = Image.open(self.current_file)
        img.thumbnail((600, 400), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width()//2,
                                 self.canvas.winfo_height()//2,
                                 image=self.photo, anchor='center')
        self.notebook.select(self.img_tab)

    def _show_metadata(self):
        scraper = MetadataScraper()
        data = scraper.scrape(self.current_file)
        parser = MetadataParser()
        parsed = parser.parse_exif(data) if isinstance(data, dict) else parser.parse_exif(data)
        self.txt_meta.config(state='normal')
        self.txt_meta.delete('1.0', 'end')
        for k, v in parsed.items():
            self.txt_meta.insert('end', f"{k:25}: {v}\n")
        self.txt_meta.config(state='disabled')
        self.notebook.select(self.meta_tab)

    def _show_stego(self):
        scraper = MetadataScraper()  # replace with your SteghideScraper when ready
        data = scraper.scrape(self.current_file)
        self.txt_stego.config(state='normal')
        self.txt_stego.delete('1.0', 'end')
        self.txt_stego.insert('end', data.get("RawOutput", "No stego data found."))
        self.txt_stego.config(state='disabled')
        self.notebook.select(self.stego_tab)

def startGUI():
    app = BigSisterGUI()
    app.mainloop()

if __name__ == "__main__":
    startGUI()
