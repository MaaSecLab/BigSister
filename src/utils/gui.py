import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os, subprocess, shutil

from metadata.parser import MetadataParser
from metadata.exiftool_scraper import MetadataScraper
from steganography.steghide_scraper import SteghideScraper
from steganography.binwalk_scraper import BinwalkScraper


class BigSisterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕵️‍♀️ Big Sister – OSINT Image Toolkit")
        self.geometry("1100x700")
        self.configure(bg="#e6ebf2")
        self.minsize(950, 600)
        self.current_file = None
        self._set_theme()
        self._build_layout()

    def _set_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        bg = "#e6ebf2"
        fg = "#2c3e50"
        accent = "#3498db"
        font_main = ("Segoe UI", 11)
        font_header = ("Segoe UI Semibold", 18)
        font_subheader = ("Segoe UI", 12)

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, font=font_main, foreground=fg)
        style.configure("Header.TLabel", font=font_header, foreground=fg)
        style.configure("SubHeader.TLabel", font=font_subheader, foreground="#7f8c8d")
        style.configure("TButton", font=font_main, padding=8, relief="flat", background="#ecf0f1")
        style.map("TButton",
                  background=[('active', accent)],
                  foreground=[('active', '#ffffff')])

    def _build_layout(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 5))
        ttk.Label(header, text="🕵️ Big Sister", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Image Metadata & Stego Analyzer", style="SubHeader.TLabel").pack(side="left", padx=15)

        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=20, pady=10)

        ctrl_frame = ttk.Frame(paned, width=270)
        ctrl_frame.pack_propagate(False)
        paned.add(ctrl_frame, weight=1)

        ttk.Label(ctrl_frame, text="📁 Select Image", style="SubHeader.TLabel").pack(anchor="w", pady=(10, 5))
        ttk.Button(ctrl_frame, text="Browse...", command=self._browse_file).pack(fill="x")

        self.lbl_file = ttk.Label(ctrl_frame, text="No file selected", wraplength=230)
        self.lbl_file.pack(fill="x", pady=(5, 15))

        ttk.Separator(ctrl_frame).pack(fill="x", pady=10)

        buttons = [
            ("🖼 View Image", self._view_image),
            ("🔍 Analyze Metadata", self._show_metadata),
            ("🔐 Steghide Scan", self._show_steghide),
            ("🧩 Binwalk Scan", self._show_binwalk),
            ("🧬 Zsteg Scan", self._show_zsteg),
        ]
        self.action_buttons = []
        for label, command in buttons:
            btn = ttk.Button(ctrl_frame, text=label, command=command, state="disabled")
            btn.pack(fill="x", pady=4)
            self.action_buttons.append(btn)

        self.notebook = ttk.Notebook(paned)
        paned.add(self.notebook, weight=4)

        self._add_text_tab("Metadata", "txt_meta")
        self._add_image_tab()
        self._add_text_tab("Steghide", "txt_steg")
        self._add_text_tab("Binwalk", "txt_binwalk")
        self._add_text_tab("Zsteg", "txt_zsteg")

    def _add_text_tab(self, label, attr_name):
        frame = ttk.Frame(self.notebook)
        textbox = tk.Text(frame, wrap="word", bg="#ffffff", relief="flat", font=("Consolas", 10))
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        setattr(self, attr_name, textbox)
        self.notebook.add(frame, text=label)

    def _add_image_tab(self):
        frame = ttk.Frame(self.notebook)
        self.canvas = tk.Canvas(frame, background="#bdc3c7", relief="flat")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.notebook.add(frame, text="Image View")

    def _browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff")])
        if not path:
            return
        self.current_file = path
        self.lbl_file.config(text=os.path.basename(path))
        for btn in self.action_buttons:
            btn.state(["!disabled"])

    def _view_image(self):
        if not self.current_file:
            return
        img = Image.open(self.current_file)
        img.thumbnail((800, 500), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.photo,
            anchor="center"
        )
        self.notebook.select(self.canvas.master)

    def _show_metadata(self):
        scraper = MetadataScraper()
        data = scraper.scrape(self.current_file)
        parsed = MetadataParser().parse_exif(data)
        self.txt_meta.config(state="normal")
        self.txt_meta.delete("1.0", "end")
        for k, v in parsed.items():
            self.txt_meta.insert("end", f"{k:25}: {v}\n")
        self.txt_meta.config(state="disabled")
        self.notebook.select(self.txt_meta.master)

    def _show_steghide(self):
        scraper = SteghideScraper()
        data = scraper.scrape(self.current_file)
        self.txt_steg.config(state="normal")
        self.txt_steg.delete("1.0", "end")
        if "RawOutput" in data:
            if "DerivedPassphrase" in data:
                self.txt_steg.insert("end", f"Used passphrase: {list(data['DerivedPassphrase'].values())[0]}\n")
            self.txt_steg.insert("end", data["RawOutput"])
        else:
            for k, v in data.items():
                self.txt_steg.insert("end", f"{k}: {v}\n")
        self.txt_steg.config(state="disabled")
        self.notebook.select(self.txt_steg.master)

    def _show_binwalk(self):
        scraper = BinwalkScraper()
        data = scraper.scrape(self.current_file)
        self.txt_binwalk.config(state="normal")
        self.txt_binwalk.delete("1.0", "end")
        if "RawOutput" in data:
            self.txt_binwalk.insert("end", data["RawOutput"])
        else:
            self.txt_binwalk.insert("end", "No binwalk data found.")
        self.txt_binwalk.config(state="disabled")
        self.notebook.select(self.txt_binwalk.master)

    def _show_zsteg(self):
        self.txt_zsteg.config(state="normal")
        self.txt_zsteg.delete("1.0", "end")
        if not shutil.which("zsteg"):
            self.txt_zsteg.insert("end", "zsteg is not installed. Please run: gem install zsteg")
        else:
            try:
                result = subprocess.run(["zsteg", self.current_file],
                                        capture_output=True, text=True, timeout=60)
                self.txt_zsteg.insert("end", result.stdout or result.stderr or "No zsteg output.")
            except Exception as e:
                self.txt_zsteg.insert("end", f"Error: {str(e)}")
        self.txt_zsteg.config(state="disabled")
        self.notebook.select(self.txt_zsteg.master)


def startGUI():
    app = BigSisterGUI()
    app.mainloop()


if __name__ == "__main__":
    startGUI()
