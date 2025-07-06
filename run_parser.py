#!/usr/bin/env python3
"""
Leaked Data Parser - Main Execution Script
Run this file to start the parser application
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stealer_parser import InfoStealerParser, DataExporter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
from datetime import datetime

class ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaked Data Parser & Analyzer v2.0.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Set dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        self.style.configure('TButton', background='#4CAF50', foreground='#ffffff')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="Leaked Data Parser & Analyzer", 
                              font=('Arial', 20, 'bold'), fg='#4CAF50', bg='#2b2b2b')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input directory selection
        ttk.Label(main_frame, text="Input Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=50)
        input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_input)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        output_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output)
        output_browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Export format selection
        ttk.Label(main_frame, text="Export Format:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="json")
        format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, 
                                   values=["json", "csv", "excel", "html", "pdf"], state="readonly")
        format_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        # Parse button
        self.parse_btn = ttk.Button(main_frame, text="Start Parsing", command=self.start_parsing)
        self.parse_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status text
        self.status_text = tk.Text(main_frame, height=15, width=80, bg='#3c3c3c', fg='#ffffff')
        self.status_text.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def browse_input(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_var.set(directory)
            
    def browse_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def start_parsing(self):
        input_dir = self.input_var.get()
        output_dir = self.output_var.get()
        export_format = self.format_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories")
            return
            
        if not os.path.exists(input_dir):
            messagebox.showerror("Error", "Input directory does not exist")
            return
            
        # Disable parse button and start progress
        self.parse_btn.config(state='disabled')
        self.progress.start()
        
        # Start parsing in separate thread
        thread = threading.Thread(target=self.parse_data, args=(input_dir, output_dir, export_format))
        thread.daemon = True
        thread.start()
        
    def parse_data(self, input_dir, output_dir, export_format):
        try:
            self.log_message("Starting data parsing...")
            
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
            self.log_message("Parsing data from all sources...")
            data = parser.parse_all()
            
            if not data['sessions']:
                self.log_message("⚠️ No data found to parse")
                messagebox.showwarning("Warning", "No data found to parse. Please check your input directory.")
                return
            
            self.log_message(f"Found {data['metadata']['total_sessions']} sessions")
            self.log_message(f"Stealer types: {', '.join(data['metadata']['stealer_types'])}")
            
            # Export data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"parsed_data_{timestamp}.{export_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            self.log_message(f"Exporting data to {export_format.upper()} format...")
            
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
                self.log_message(f"✅ Export successful: {output_path}")
                messagebox.showinfo("Success", f"Data exported successfully!\nFile: {output_path}")
            else:
                self.log_message(f"❌ Export failed: {message}")
                messagebox.showerror("Export Error", message)
                
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
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
