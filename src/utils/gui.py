import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os, subprocess, shutil

from metadata.parser import MetadataParser
from metadata.iris_parser import IrisParser
from metadata.exiftool_scraper import MetadataScraper
from steganography.steghide_scraper import SteghideScraper
from steganography.binwalk_scraper import BinwalkScraper
from iris.image_search import ImageSearchIRIS
from steganography.zsteg_scraper import run_zsteg, parse_and_group_zsteg
from video_stego_scanner import VideoStegoScanner
from ocr.ocr_engine import OCREngine


class BigSisterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕵️‍♀️ Big Sister – OSINT Image Toolkit")
        self.geometry("1100x700")
        self.minsize(950, 600)
        self.current_file = None
        self.is_dark_mode = False  # Track dark mode state
        self.iris = None  # Initialize IRIS attribute
        self._set_theme()  # Apply the initial theme
        self._build_layout()
        
        # Ensure Contributors button is enabled by default
        if hasattr(self, 'action_buttons') and len(self.action_buttons) > 7:
            self.action_buttons[7].state(["!disabled"])  # Contributors button

    def _set_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Define colors based on the theme
        if self.is_dark_mode:
            bg = "#2c3e50"
            fg = "#ecf0f1"
            accent = "#3498db"
            font_main = ("Segoe UI", 11)
            font_header = ("Segoe UI Semibold", 18)
            font_subheader = ("Segoe UI", 12)
            text_bg = "#34495e"
            text_fg = "#ecf0f1"
            button_bg = "#34495e"
            button_fg = "#ecf0f1"
        else:
            bg = "#e6ebf2"
            fg = "#2c3e50"
            accent = "#3498db"
            font_main = ("Segoe UI", 11)
            font_header = ("Segoe UI Semibold", 18)
            font_subheader = ("Segoe UI", 12)
            text_bg = "#ffffff"
            text_fg = "#2c3e50"
            button_bg = "#ecf0f1"
            button_fg = "#2c3e50"

        # Apply styles
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, font=font_main, foreground=fg)
        style.configure("Header.TLabel", font=font_header, foreground=fg)
        style.configure("SubHeader.TLabel", font=font_subheader, foreground="#7f8c8d")
        style.configure("TButton", font=font_main, padding=8, relief="flat", background=button_bg, foreground=button_fg)
        style.map("TButton",
                  background=[('active', accent)],
                  foreground=[('active', '#ffffff')])

        # Customizing text box styles for dark mode
        self.textbox_bg = text_bg
        self.textbox_fg = text_fg

    def _build_layout(self):
        # Set up the header and title
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 5))
        ttk.Label(header, text="🕵️ Big Sister", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Image Metadata & Stego Analyzer", style="SubHeader.TLabel").pack(side="left", padx=15)

        # Dark Mode Toggle Button
        btn_dark_mode = ttk.Button(header, text="🌙 Dark Mode" if not self.is_dark_mode else "🌞 Light Mode", command=self.toggle_dark_mode)
        btn_dark_mode.pack(side="right", padx=20)

        # Create the main control panel with a paned window layout
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=20, pady=10)

        ctrl_frame = ttk.Frame(paned, width=270)
        ctrl_frame.pack_propagate(False)
        paned.add(ctrl_frame, weight=1)

        # File selection and action buttons
        ttk.Label(ctrl_frame, text="📁 Select Image", style="SubHeader.TLabel").pack(anchor="w", pady=(10, 5))
        ttk.Button(ctrl_frame, text="Browse...", command=self._browse_file).pack(fill="x")
        self.lbl_file = ttk.Label(ctrl_frame, text="No file selected", wraplength=230)
        self.lbl_file.pack(fill="x", pady=(5, 15))

        ttk.Separator(ctrl_frame).pack(fill="x", pady=10)

        buttons = [
            ("🖼 View Image", self._view_image),
            ("🔍 Analyze Metadata", self._show_metadata),
            ("🎯 IRIS Analysis", self._show_iris_analysis),
            ("🔐 Steghide Scan", self._show_steghide),
            ("🧩 Binwalk Scan", self._show_binwalk),
            ("🧬 Zsteg Scan", self._show_zsteg),
            ("🔎 Reverse Image Search", self._show_image_search),
            ("🧠 OCR Text Scan", self._show_ocr),
            ("🎥 Video Stego Scan", self._show_video_stego),
            ("👥 Contributors", self._show_contributors),  # Add this new button
        ]
        self.action_buttons = []
        self.action_buttons = []
        for i, (label, command) in enumerate(buttons):
            if label == "👥 Contributors":
                btn = ttk.Button(ctrl_frame, text=label, command=command, state="normal")  # Always enabled
            else:
                btn = ttk.Button(ctrl_frame, text=label, command=command, state="disabled")
            btn.pack(fill="x", pady=4)
            self.action_buttons.append(btn)

        # Notebook for tabs
        self.notebook = ttk.Notebook(paned)
        paned.add(self.notebook, weight=4)

        # Create all tabs for the notebook
        self._add_text_tab("Metadata", "txt_meta")
        self._add_image_tab()
        self._add_text_tab("Steghide", "txt_steg")
        self._add_text_tab("Binwalk", "txt_binwalk")
        self._add_text_tab("Zsteg", "txt_zsteg")
        self._add_image_search_tab()
        self._add_text_tab("OCR Output", "txt_ocr")
        self._add_text_tab("Contributors", "txt_contributors")

    def _add_text_tab(self, label, attr_name):
        frame = ttk.Frame(self.notebook)
        textbox = tk.Text(frame, wrap="word", bg=self.textbox_bg, relief="flat", font=("Consolas", 10), fg=self.textbox_fg)
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        setattr(self, attr_name, textbox)
        self.notebook.add(frame, text=label)

    def _add_image_tab(self):
        frame = ttk.Frame(self.notebook)
        self.canvas = tk.Canvas(frame, background=self.textbox_bg, relief="flat")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.notebook.add(frame, text="Image View")

    def _browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff")])
        if not path:
            return
        self.current_file = path
        self.lbl_file.config(text=os.path.basename(path))
        
        # Enable all buttons except keep Contributors always enabled
        for i, btn in enumerate(self.action_buttons):
            if i == 7:  # Contributors button index (0-based, counting from 0)
                btn.state(["!disabled"])  # Keep enabled
            else:
                btn.state(["!disabled"])  # Enable when file is selected

        # Display image immediately after selecting
        self._view_image()

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

        anomalies = scraper.check_timestamp_anomaly(self.current_file, data)

        self.txt_meta.config(state="normal")
        self.txt_meta.delete("1.0", "end")

        for k, v in parsed.items():
            self.txt_meta.insert("end", f"{k:25}: {v}\n")

        #print anomalies if there are any
        if anomalies:
            self.txt_meta.insert("end", "\n⚠️  ANOMALIES DETECTED\n")
            self.txt_meta.insert("end", "=" * 50 + "\n")
            for k, v in anomalies.items():
                self.txt_meta.insert("end", f"🚨 {k}: {v}\n")
        else:
            self.txt_meta.insert("end", "\n✅ No timestamp anomalies detected.\n")

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
        def zsteg_worker():
            self.txt_zsteg.config(state="normal")
            self.txt_zsteg.delete("1.0", "end")
            self.txt_zsteg.insert("end", "🧬 Running Zsteg scan...\nPlease wait...\n\n")
            self.txt_zsteg.config(state="disabled")
            self.notebook.select(self.txt_zsteg.master)

            output = run_zsteg(self.current_file)

            self.txt_zsteg.config(state="normal")
            self.txt_zsteg.delete("1.0", "end")
            parsed_output = parse_and_group_zsteg(output)
            self.txt_zsteg.insert("end", parsed_output)
            self.txt_zsteg.config(state="disabled")

    # Run the Zsteg scan in a background thread
        threading.Thread(target=zsteg_worker, daemon=True).start()

    def _add_image_search_tab(self):
        """Add a tab for reverse image search functionality"""
        frame = ttk.Frame(self.notebook)
        
        # Create a frame for the search controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Status label
        self.search_status = ttk.Label(control_frame, text="Ready to search", foreground="#7f8c8d")
        self.search_status.pack(anchor="w", pady=(0, 5))
        
        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=5)
        
        # Start search button
        self.btn_start_search = ttk.Button(button_frame, text="🚀 Start Reverse Image Search", 
                                          command=self._start_image_search, state="disabled")
        self.btn_start_search.pack(side="left", padx=(0, 10))
        
        # Stop search button
        self.btn_stop_search = ttk.Button(button_frame, text="🛑 Stop Search", 
                                         command=self._stop_image_search, state="disabled")
        self.btn_stop_search.pack(side="left")
        
        # Progress bar
        self.search_progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.search_progress.pack(fill="x", pady=5)
        
        # Results text area
        textbox = tk.Text(frame, wrap="word", bg=self.textbox_bg, relief="flat", 
                         font=("Consolas", 10), fg=self.textbox_fg)
        textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.txt_search = textbox
        
        self.notebook.add(frame, text="Image Search")

    def _show_image_search(self):
        """Switch to the image search tab and enable the search button"""
        if self.current_file:
            self.btn_start_search.state(["!disabled"])
            self.search_status.config(text=f"Ready to search: {os.path.basename(self.current_file)}")
        self.notebook.select(self.txt_search.master)

    def _start_image_search(self):
        """Start the reverse image search in a separate thread"""
        if not self.current_file:
            messagebox.showerror("Error", "No image selected!")
            return
        
        # Update UI state
        self.btn_start_search.state(["disabled"])
        self.btn_stop_search.state(["!disabled"])
        self.search_progress.start()
        self.search_status.config(text="Initializing search...")
        
        # Clear previous results
        self.txt_search.config(state="normal")
        self.txt_search.delete("1.0", "end")
        self.txt_search.insert("end", "🔍 Starting reverse image search...\n")
        self.txt_search.insert("end", f"📁 Image: {os.path.basename(self.current_file)}\n")
        self.txt_search.insert("end", "⏳ Opening browser and performing search...\n\n")
        self.txt_search.config(state="disabled")
        
        # Start search in a separate thread
        self.search_thread = threading.Thread(target=self._perform_image_search, daemon=True)
        self.search_thread.start()

    def _perform_image_search(self):
        """Perform the actual image search (runs in separate thread)"""
        try:
            # Initialize IRIS
            self.iris = ImageSearchIRIS()
            
            # Update status in main thread
            self.after(0, lambda: self.search_status.config(text="Setting up browser..."))
            
            # Perform the search
            success = self.iris.reverse_image_search(self.current_file)
            
            if success:
                # Update UI in main thread
                self.after(0, self._search_completed_successfully)
            else:
                # Update UI in main thread
                self.after(0, self._search_failed)
                
        except Exception as e:
            # Update UI in main thread
            self.after(0, lambda: self._search_error(str(e)))

    def _search_completed_successfully(self):
        """Handle successful search completion (runs in main thread)"""
        self.search_progress.stop()
        self.search_status.config(text="✅ Search completed! Browser opened with results.")
        
        self.txt_search.config(state="normal")
        self.txt_search.insert("end", "✅ REVERSE IMAGE SEARCH COMPLETED!\n")
        self.txt_search.insert("end", "=" * 50 + "\n")
        self.txt_search.insert("end", "🌐 The search results are now displayed in your browser.\n\n")
        self.txt_search.insert("end", "🔍 You can:\n")
        self.txt_search.insert("end", "   • Browse through visually similar images\n")
        self.txt_search.insert("end", "   • Check pages that contain matching images\n")
        self.txt_search.insert("end", "   • Click on any result to explore further\n")
        self.txt_search.insert("end", "   • Use browser tools to save or analyze results\n\n")
        self.txt_search.insert("end", "💡 The browser window will remain open for your analysis.\n")
        self.txt_search.insert("end", "   Use the 'Stop Search' button to close it when done.\n")
        self.txt_search.config(state="disabled")
        
        # Reset button states
        self.btn_start_search.state(["!disabled"])

    def _search_failed(self):
        """Handle search failure (runs in main thread)"""
        self.search_progress.stop()
        self.search_status.config(text="❌ Search failed. Check the results for details.")
        
        self.txt_search.config(state="normal")
        self.txt_search.insert("end", "❌ Search failed!\n")
        self.txt_search.insert("end", "Please check your internet connection and try again.\n")
        self.txt_search.config(state="disabled")
        
        # Reset button states
        self.btn_start_search.state(["!disabled"])
        self.btn_stop_search.state(["disabled"])

    def _search_error(self, error_msg):
        """Handle search error (runs in main thread)"""
        self.search_progress.stop()
        self.search_status.config(text="❌ Error occurred during search.")
        
        self.txt_search.config(state="normal")
        self.txt_search.insert("end", f"❌ Error: {error_msg}\n")
        self.txt_search.config(state="disabled")
        
        # Reset button states
        self.btn_start_search.state(["!disabled"])
        self.btn_stop_search.state(["disabled"])

    def _stop_image_search(self):
        """Stop the image search and close the browser"""
        if self.iris:
            try:
                self.iris.close()
                self.iris = None
            except Exception as e:
                print(f"Error closing IRIS: {e}")
        
        self.search_progress.stop()
        self.search_status.config(text="🛑 Search stopped. Browser closed.")
        
        self.txt_search.config(state="normal")
        self.txt_search.insert("end", "\n🛑 Search stopped by user. Browser closed.\n")
        self.txt_search.config(state="disabled")
        
        # Reset button states
        self.btn_start_search.state(["!disabled"])
        self.btn_stop_search.state(["disabled"])

    def _clear_and_rebuild_layout(self):
        # Save the current selected file, tab, and other state before rebuilding the layout
        file = self.current_file
        selected_tab = self.notebook.index(self.notebook.select())  # Save the current tab index

        # Close any open IRIS instance before rebuilding
        if hasattr(self, 'iris') and self.iris:
            try:
                self.iris.close()
                self.iris = None
            except:
                pass

        # Rebuild the layout (clearing and re-adding widgets)
        for widget in self.winfo_children():
            widget.destroy()

        # Rebuild the layout
        self._build_layout()

        # Restore the file selection and tab
        self.current_file = file

        # If the current_file is not None, update the label and enable buttons
        if self.current_file:
            self.lbl_file.config(text=os.path.basename(file))
            for i, btn in enumerate(self.action_buttons):
                btn.state(["!disabled"])  # Enable all buttons when file is selected
        else:
            self.lbl_file.config(text="No file selected")
            # Keep only Contributors button enabled when no file is selected
            for i, btn in enumerate(self.action_buttons):
                if i == 7:  # Contributors button index
                    btn.state(["!disabled"])  # Keep enabled
                else:
                    btn.state(["disabled"])  # Disable others

        self.notebook.select(selected_tab)  # Restore the selected tab

    def destroy(self):
        """Override destroy to clean up resources"""
        if self.iris:
            try:
                self.iris.close()
            except:
                pass
        super().destroy()

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode  # Toggle the mode
        self._set_theme()  # Apply the selected theme
        self._clear_and_rebuild_layout()  # Rebuild layout only when switching mode

    def _clear_and_rebuild_layout(self):
        # Save the current selected file, tab, and other state before rebuilding the layout
        file = self.current_file
        selected_tab = self.notebook.index(self.notebook.select())  # Save the current tab index

        # Rebuild the layout (clearing and re-adding widgets)
        for widget in self.winfo_children():
            widget.destroy()

        # Rebuild the layout
        self._build_layout()

        # Restore the file selection and tab
        self.current_file = file

        # If the current_file is not None, update the label
        if self.current_file:
            self.lbl_file.config(text=os.path.basename(file))
        else:
            self.lbl_file.config(text="No file selected")  # Set default text if no file is selected

        self.notebook.select(selected_tab)  # Restore the selected tab

    def _show_iris_analysis(self):
        """Show IRIS categorization analysis"""
        print("=" * 50)
        print("CALLING IRIS ANALYSIS FROM DEDICATED BUTTON")
        print("=" * 50)
        
        scraper = MetadataScraper()
        data = scraper.scrape(self.current_file)
        
        # Use MetadataParser to parse the EXIF data first
        metadata_parser = MetadataParser()
        parsed = metadata_parser.parse_exif(data)
        
        # Then use IrisParser for categorization and search terms
        iris_parser = IrisParser()
        categorized = iris_parser.categorize_exif_for_iris(parsed)
        search_terms = iris_parser.get_iris_search_terms(categorized)
        
        # Display in a new tab or reuse existing metadata tab
        self.txt_meta.config(state="normal")
        self.txt_meta.delete("1.0", "end")
        
        self.txt_meta.insert("end", "🎯 IRIS METADATA ANALYSIS\n")
        self.txt_meta.insert("end", "=" * 50 + "\n\n")
        
        self.txt_meta.insert("end", f"📊 Overall Confidence Score: {categorized['confidence_score']:.2f}\n\n")
        
        # Show each category
        categories = [
            ("📷 Device Information", categorized['device_info']),
            ("📍 Location Data", categorized['location_data']),
            ("🕒 Temporal Data", categorized['temporal_data']),
            ("⚙️ Technical Specifications", categorized['technical_specs'])
        ]
        
        for title, data_dict in categories:
            if data_dict:
                self.txt_meta.insert("end", f"{title}:\n")
                for k, v in data_dict.items():
                    self.txt_meta.insert("end", f"  • {k}: {v}\n")
                self.txt_meta.insert("end", "\n")
        
        if categorized['search_keywords']:
            self.txt_meta.insert("end", "🔍 All Generated Keywords:\n")
            for keyword in categorized['search_keywords']:
                self.txt_meta.insert("end", f"  • {keyword}\n")
            self.txt_meta.insert("end", "\n")
        
        if search_terms:
            self.txt_meta.insert("end", "🎯 Priority Search Terms for IRIS:\n")
            for i, term in enumerate(search_terms, 1):
                self.txt_meta.insert("end", f"  {i}. {term}\n")
        
        self.txt_meta.config(state="disabled")
        self.notebook.select(self.txt_meta.master)

    def _show_ocr(self):
        if not self.current_file:
            messagebox.showwarning("No File", "Please select an image file first.")
            return

        # Instantiate the OCR engine (optional: set tesseract_cmd)
        ocr_engine = OCREngine(tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe")  # Update if needed

        # Run OCR
        result = ocr_engine.extract_text_from_image(self.current_file, return_data=False)

        # Display result
        self.txt_ocr.config(state="normal")
        self.txt_ocr.delete("1.0", "end")
        if result["success"]:
            self.txt_ocr.insert("end", f"🧠 OCR Result (in {result['time']}s):\n\n{result['text']}")
        else:
            self.txt_ocr.insert("end", f"❌ OCR Failed:\n{result['error']}")
        self.txt_ocr.config(state="disabled")

        self.notebook.select(self.txt_ocr.master)

    def _show_video_stego(self):
        path = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mov *.avi *.mkv")])
        if not path:
            return

        self.txt_meta.config(state="normal")
        self.txt_meta.delete("1.0", "end")
        self.txt_meta.insert("end", f"🎥 Running Video Stego Scan on:\n{os.path.basename(path)}\nPlease wait...\n")
        self.txt_meta.config(state="disabled")
        self.notebook.select(self.txt_meta.master)
        threading.Thread(target=lambda: self.worker(path), daemon=True).start()

    def worker(self, path):
        scanner = VideoStegoScanner()
        report = scanner.scan_video(path)
        self.after(0, lambda: self._display_video_report(report))
        #self.after(0, lambda: self._display_video_report(report))
        #threading.Thread(target=lambda: self.worker(path), daemon=True).start()
        #threading.Thread(target=worker, daemon=True).start()


    def _display_video_report(self, report):
        txt = self.txt_meta
        txt.config(state="normal")
        txt.delete("1.0", "end")
        txt.insert("end", "🎯 Video Steganography Scan Report\n")
        txt.insert("end", "="*50 + "\n")
        txt.insert("end", f"Suspicious: {report['suspicious']}\n")
        txt.insert("end", f"Flagged Frames: {len(report['flagged_frames'])} / {report['total_frames']}\n\n")
        if report['flagged_frames']:
            txt.insert("end", "🚨 Frames flagged:\n")
            for fr in report['flagged_frames']:
                txt.insert("end", f"  • {fr}\n")
        txt.config(state="disabled")



    def _show_contributors(self):
        """Show project contributors and credits"""
        contributors_text = """🎯 BIG SISTER - MaaSec's Image Metadata & Stego Analyzer
═══════════════════════════════════════════════════════════════

👨‍💻 PROJECT CONTRIBUTORS
══════════════════════════

🏆 Project Leader
   • [Your Name] - Project Creator & Maintainer
   • GitHub: @yourusername
   • Role: Core architecture, GUI development, IRIS integration

🔧 Main Developers
   • [Vlad-Luca Manolescu] - MaaSec CTF Team member
    • GitHub: https://github.com/IlikeEndermen
    • Tasks: IRIS implementation, integration and data parsing, ExifTool implementation, Core architecture designer, Zsteg implementation
   • [Alexia-Madalina Cirstea] - MaaSec CTF Team member
    • GitHub: https://github.com/AlexiaMadalinaCirstea
    • Tasks: Please fill in your tasks here


🛠️ TECHNOLOGY STACK
═══════════════════

🖥️ Frontend:
   • Python Tkinter - Cross-platform GUI framework
   • PIL/Pillow - Image processing and display
   • TTK Themes - Modern UI styling

🔍 Analysis Tools:
   • ExifTool - Comprehensive metadata extraction
   • Steghide - Steganography detection and extraction
   • Binwalk - Embedded file signature analysis
   • Zsteg - LSB steganography detection

🌐 IRIS (Image Search):
   • Selenium WebDriver - Browser automation
   • Google Images API - Reverse image search
   • Bing Visual Search - Alternative search engine
   • Yandex Images - Extended search capabilities

📊 Data Processing:
   • Metadata Parser - Unified data structure
   • IRIS Parser - Search-optimized categorization
   • JSON Configuration - Flexible tool management

🏆 PROJECT STATS
════════════════

🎯 Use Cases:
   • CTF Competitions - Image forensics challenges
   • OSINT Investigations - Social media image analysis
   • Digital Forensics - Metadata examination
   • Security Research - Steganography detection

🌍 OPEN SOURCE
══════════════

📜 License: MIT License
🔗 Repository: https://github.com/yourusername/BigSister
🐛 Issues: Report bugs and request features
🤝 Contributions: Pull requests welcome!

📚 Documentation:
   • Setup Guide - Installation and configuration
   • User Manual - Feature descriptions and usage
   • API Reference - Developer documentation
   • Contributing Guide - How to contribute


═══════════════════════════════════════════════════════════════
        Built with ❤️ by the MaaSec CTF Team
═══════════════════════════════════════════════════════════════"""

        self.txt_contributors.config(state="normal")
        self.txt_contributors.delete("1.0", "end")
        self.txt_contributors.insert("end", contributors_text)
        self.txt_contributors.config(state="disabled")
        self.notebook.select(self.txt_contributors.master)


def startGUI():
    app = BigSisterGUI()
    app.mainloop()


if __name__ == "__main__":
    startGUI()
