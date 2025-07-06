#!/usr/bin/env python3
"""
Multi-Export Leaked Data Parser - Main Execution Script
Run this file to start the parser application with multi-format export support
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from stealer_parser import InfoStealerParser, DataExporter
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import threading
    import json
    from datetime import datetime
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)

class MultiExportParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Export Leaked Data Parser & Analyzer v2.2.0")
        self.root.geometry("1000x800")
        self.root.configure(bg='#2b2b2b')
        
        # Set dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        self.style.configure('TButton', background='#4CAF50', foreground='#ffffff')
        self.style.configure('TCheckbutton', background='#2b2b2b', foreground='#ffffff')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="Multi-Export Leaked Data Parser & Analyzer", 
                              font=('Arial', 24, 'bold'), fg='#4CAF50', bg='#2b2b2b')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Version info
        version_label = tk.Label(main_frame, text="Version 2.2.0 - Multi-Format Export Support", 
                                font=('Arial', 12), fg='#888888', bg='#2b2b2b')
        version_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Input directory selection
        ttk.Label(main_frame, text="Input Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=70)
        input_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_input)
        browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=70)
        output_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        output_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output)
        output_browse_btn.grid(row=3, column=2, padx=(5, 0), pady=5)
        
        # Export formats selection
        ttk.Label(main_frame, text="Export Formats:").grid(row=4, column=0, sticky=tk.W, pady=10)
        
        # Create a frame for checkboxes
        formats_frame = ttk.Frame(main_frame)
        formats_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=10)
        
        # Export format checkboxes
        self.export_formats = {
            'json': tk.BooleanVar(value=True),
            'csv': tk.BooleanVar(value=False),
            'excel': tk.BooleanVar(value=False),
            'html': tk.BooleanVar(value=False),
            'pdf': tk.BooleanVar(value=False)
        }
        
        row = 0
        col = 0
        for format_name, var in self.export_formats.items():
            cb = ttk.Checkbutton(formats_frame, text=format_name.upper(), variable=var)
            cb.grid(row=row, column=col, padx=10, pady=5, sticky=tk.W)
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        # Select All / Deselect All buttons
        select_frame = ttk.Frame(main_frame)
        select_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        select_all_btn = ttk.Button(select_frame, text="Select All", command=self.select_all_formats)
        select_all_btn.grid(row=0, column=0, padx=5)
        
        deselect_all_btn = ttk.Button(select_frame, text="Deselect All", command=self.deselect_all_formats)
        deselect_all_btn.grid(row=0, column=1, padx=5)
        
        # Parse button
        self.parse_btn = ttk.Button(main_frame, text="Start Multi-Format Export", command=self.start_parsing)
        self.parse_btn.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status text
        self.status_text = tk.Text(main_frame, height=25, width=100, bg='#3c3c3c', fg='#ffffff')
        self.status_text.grid(row=8, column=0, columnspan=3, pady=10)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=8, column=3, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Initial message
        self.log_message("🚀 Multi-Export Leaked Data Parser v2.2.0 loaded successfully!")
        self.log_message("✅ All systems ready for multi-format data parsing")
        self.log_message("📋 Select multiple export formats to export data in all selected formats")
        
    def select_all_formats(self):
        """Select all export formats"""
        for var in self.export_formats.values():
            var.set(True)
        self.log_message("✅ All export formats selected")
        
    def deselect_all_formats(self):
        """Deselect all export formats"""
        for var in self.export_formats.values():
            var.set(False)
        self.log_message("❌ All export formats deselected")
        
    def browse_input(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_var.set(directory)
            self.log_message(f"📁 Input directory selected: {directory}")
            
    def browse_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
            self.log_message(f"📁 Output directory selected: {directory}")
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def start_parsing(self):
        input_dir = self.input_var.get()
        output_dir = self.output_var.get()
        
        # Get selected formats
        selected_formats = [fmt for fmt, var in self.export_formats.items() if var.get()]
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories")
            return
            
        if not selected_formats:
            messagebox.showerror("Error", "Please select at least one export format")
            return
            
        # Disable parse button and start progress
        self.parse_btn.config(state='disabled')
        self.progress.start()
        
        # Start parsing in separate thread
        thread = threading.Thread(target=self.parse_data, args=(input_dir, output_dir, selected_formats))
        thread.daemon = True
        thread.start()
        
    def parse_data(self, input_dir, output_dir, selected_formats):
        try:
            self.log_message("🔍 Starting multi-format data parsing...")
            
            # التحقق من وجود مجلد المدخل
            if not os.path.exists(input_dir):
                raise FileNotFoundError(f"Input directory not found: {input_dir}")
                
            # التحقق من صلاحيات الكتابة
            if not os.access(output_dir, os.W_OK):
                raise PermissionError(f"No write permission for output directory: {output_dir}")
            
            # التحقق من أن مجلد المدخل يحتوي على بيانات
            input_path = Path(input_dir)
            if not any(input_path.iterdir()):
                raise ValueError(f"Input directory is empty: {input_dir}")
            
            # Initialize parser
            parser = InfoStealerParser(input_dir)
            
            # Parse all data
            self.log_message("📊 Parsing data from all sources...")
            data = parser.parse_all()
            
            if not data['sessions']:
                self.log_message("⚠️ No data found to parse")
                messagebox.showwarning("Warning", "No data found to parse. Please check your input directory.")
                return
            
            self.log_message(f"✅ Found {data['metadata']['total_sessions']} sessions")
            self.log_message(f" Stealer types: {', '.join(data['metadata']['stealer_types'])}")
            
            # Export data in multiple formats
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            successful_exports = []
            failed_exports = []
            
            self.log_message(f"💾 Starting multi-format export ({len(selected_formats)} formats)...")
            
            for export_format in selected_formats:
                try:
                    output_filename = f"multi_export_{timestamp}.{export_format}"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    self.log_message(f"📄 Exporting to {export_format.upper()}...")
                    
                    if export_format == "json":
                        success, message = DataExporter.export_json(data, output_path)
                    elif export_format == "csv":
                        success, message = DataExporter.export_csv(data, output_path)
                    elif export_format == "excel":
                        success, message = DataExporter.export_excel(data, output_path)
                    elif export_format == "html":
                        success, message = DataExporter.export_html(data, output_path)
                    elif export_format == "pdf":
                        success, message = DataExporter.export_pdf(data, output_path)
                    else:
                        success, message = False, "Unsupported export format"
                    
                    if success:
                        self.log_message(f"✅ {export_format.upper()} export successful: {output_filename}")
                        successful_exports.append(export_format.upper())
                    else:
                        self.log_message(f"❌ {export_format.upper()} export failed: {message}")
                        failed_exports.append(export_format.upper())
                        
                except Exception as e:
                    self.log_message(f"❌ Error exporting {export_format.upper()}: {str(e)}")
                    failed_exports.append(export_format.upper())
            
            # Summary
            self.log_message("📊 Export Summary:")
            self.log_message(f"✅ Successful: {', '.join(successful_exports)}")
            if failed_exports:
                self.log_message(f"❌ Failed: {', '.join(failed_exports)}")
            
            # Show final message
            if successful_exports:
                messagebox.showinfo("Multi-Export Complete", 
                                  f"Successfully exported data in {len(successful_exports)} format(s):\n"
                                  f"{', '.join(successful_exports)}\n\n"
                                  f"Files saved to: {output_dir}")
            else:
                messagebox.showerror("Export Failed", "All export formats failed. Check the log for details.")
                
        except FileNotFoundError as e:
            self.log_message(f"❌ File error: {str(e)}")
            messagebox.showerror("File Error", str(e))
        except PermissionError as e:
            self.log_message(f"❌ Permission error: {str(e)}")
            messagebox.showerror("Permission Error", str(e))
        except ValueError as e:
            self.log_message(f"❌ Validation error: {str(e)}")
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            self.log_message(f"❌ Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            
        finally:
            # Re-enable parse button and stop progress
            self.root.after(0, lambda: self.parse_btn.config(state='normal'))
            self.root.after(0, self.progress.stop)

def main():
    try:
        root = tk.Tk()
        app = MultiExportParserGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
