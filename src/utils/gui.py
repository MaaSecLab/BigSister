
#!/usr/bin/env python3
import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import shutil

# Metadata & stego tools
from metadata.parser import MetadataParser
from metadata.exiftool_scraper import MetadataScraper
from steganography.steghide_scraper import SteghideScraper
from steganography.binwalk_scraper import BinwalkScraper

class BigSisterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕵️‍♀️ Big Sister – OSINT Image Toolkit")
        self.geometry("1000x650")
        self.minsize(900, 550)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f4f7')
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), background='#f0f4f7', foreground='#333')
        style.configure('SubHeader.TLabel', font=('Helvetica', 12), background='#f0f4f7')
        style.configure('TButton', font=('Helvetica', 11), padding=6)

        self.current_file = None
        self._build_layout()

    def _build_layout(self):
        header = ttk.Frame(self)
        header.pack(fill='x', padx=20, pady=(20,10))
        ttk.Label(header, text="Big Sister", style='Header.TLabel').pack(side='left')
        ttk.Label(header, text="Image Metadata & Stego Analysis", style='SubHeader.TLabel').pack(side='left', padx=10)

        paned = ttk.PanedWindow(self, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=20, pady=10)

        ctrl_frame = ttk.Frame(paned, width=250)
        ctrl_frame.pack_propagate(False)
        paned.add(ctrl_frame, weight=1)

        ttk.Label(ctrl_frame, text="Select Image", style='SubHeader.TLabel').pack(anchor='w', pady=(10,5))
        btn_browse = ttk.Button(ctrl_frame, text="📁 Browse…", command=self._browse_file)
        btn_browse.pack(fill='x')

        self.lbl_file = ttk.Label(ctrl_frame, text="No file selected", wraplength=230)
        self.lbl_file.pack(fill='x', pady=(5,15))

        ttk.Separator(ctrl_frame).pack(fill='x', pady=10)
        self.btn_view = ttk.Button(ctrl_frame, text="🖼 View Image", command=self._view_image, state='disabled')
        self.btn_view.pack(fill='x', pady=5)
        self.btn_meta = ttk.Button(ctrl_frame, text="🔍 Analyze Metadata", command=self._show_metadata, state='disabled')
        self.btn_meta.pack(fill='x', pady=5)
        self.btn_steg = ttk.Button(ctrl_frame, text="🔐 Steghide Scan", command=self._show_steghide, state='disabled')
        self.btn_steg.pack(fill='x', pady=5)
        self.btn_binwalk = ttk.Button(ctrl_frame, text="🧩 Binwalk Scan", command=self._show_binwalk, state='disabled')
        self.btn_binwalk.pack(fill='x', pady=5)
        self.btn_zsteg = ttk.Button(ctrl_frame, text="🧬 Zsteg Scan", command=self._show_zsteg, state='disabled')
        self.btn_zsteg.pack(fill='x', pady=5)

        self.notebook = ttk.Notebook(paned)
        paned.add(self.notebook, weight=4)

        self.meta_tab = ttk.Frame(self.notebook)
        self.txt_meta = tk.Text(self.meta_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_meta.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.meta_tab, text="Metadata")

        self.img_tab = ttk.Frame(self.notebook)
        self.canvas = tk.Canvas(self.img_tab, background='#ddd')
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.img_tab, text="Image View")

        self.steg_tab = ttk.Frame(self.notebook)
        self.txt_steg = tk.Text(self.steg_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_steg.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.steg_tab, text="Steghide")

        self.binwalk_tab = ttk.Frame(self.notebook)
        self.txt_binwalk = tk.Text(self.binwalk_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_binwalk.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.binwalk_tab, text="Binwalk")

        self.zsteg_tab = ttk.Frame(self.notebook)
        self.txt_zsteg = tk.Text(self.zsteg_tab, wrap='word', state='disabled', bg='#ffffff', relief='flat')
        self.txt_zsteg.pack(fill='both', expand=True, padx=10, pady=10)
        self.notebook.add(self.zsteg_tab, text="Zsteg")

    def _browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff")])
        if not path:
            return
        self.current_file = path
        self.lbl_file.config(text=os.path.basename(path))
        for btn in (self.btn_view, self.btn_meta, self.btn_steg, self.btn_binwalk, self.btn_zsteg):
            btn.state(['!disabled'])

    def _view_image(self):
        if not self.current_file:
            return
        img = Image.open(self.current_file)
        img.thumbnail((600, 400), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, image=self.photo, anchor='center')
        self.notebook.select(self.img_tab)

    def _show_metadata(self):
        scraper = MetadataScraper()
        data = scraper.scrape(self.current_file)
        parsed = MetadataParser().parse_exif(data)
        self.txt_meta.config(state='normal')
        self.txt_meta.delete('1.0', 'end')
        for k, v in parsed.items():
            self.txt_meta.insert('end', f"{k:25}: {v}")
        self.txt_meta.config(state='disabled')
        self.notebook.select(self.meta_tab)

    def _show_steghide(self):
        scraper = SteghideScraper()
        data = scraper.scrape(self.current_file)
        self.txt_steg.config(state='normal')
        self.txt_steg.delete('1.0', 'end')
        if "RawOutput" in data:
            if "DerivedPassphrase" in data:
                self.txt_steg.insert('end', f"Used passphrase: {list(data['DerivedPassphrase'].values())[0]}")
            self.txt_steg.insert('end', data["RawOutput"])
        else:
            for k, v in data.items():
                self.txt_steg.insert('end', f"{k}: {v}")
        self.txt_steg.config(state='disabled')
        self.notebook.select(self.steg_tab)

    def _show_binwalk(self):
        scraper = BinwalkScraper()
        data = scraper.scrape(self.current_file)
        self.txt_binwalk.config(state='normal')
        self.txt_binwalk.delete('1.0', 'end')
        if "RawOutput" in data:
            self.txt_binwalk.insert('end', data["RawOutput"])
        else:
            self.txt_binwalk.insert('end', "No binwalk data found.")
        self.txt_binwalk.config(state='disabled')
        self.notebook.select(self.binwalk_tab)

    def _show_zsteg(self):
        self.txt_zsteg.config(state='normal')
        self.txt_zsteg.delete('1.0', 'end')
        if not shutil.which("zsteg"):
            self.txt_zsteg.insert('end', "zsteg is not installed. Please run: gem install zsteg")
        else:
            try:
                result = subprocess.run(["zsteg", self.current_file],
                                        capture_output=True, text=True, timeout=60)
                self.txt_zsteg.insert('end', result.stdout or result.stderr or "No zsteg output.")
            except Exception as e:
                self.txt_zsteg.insert('end', f"Error: {str(e)}")
        self.txt_zsteg.config(state='disabled')
        self.notebook.select(self.zsteg_tab)

def startGUI():
    app = BigSisterGUI()
    app.mainloop()

if __name__ == "__main__":
    startGUI()
