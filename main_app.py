#!/usr/bin/env python3
"""
Leaked Data Parser & Analyzer - Complete Integrated Application (Fixed Version)
Main application that combines parsing, analysis, and multi-format export
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from stealer_parser import InfoStealerParser, DataExporter
    from data_analyzer import DataAnalyzer
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    import threading
    import json
    from datetime import datetime
    import webbrowser
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)

class IntegratedParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaked Data Parser & Analyzer - Complete Suite v3.0.0")
        self.root.geometry("1200x900")
        self.root.configure(bg='#1e1e1e')
        
        # Set dark theme with compatible styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles without problematic font options
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
        self.style.configure('TButton', background='#4CAF50', foreground='#ffffff')
        self.style.configure('TCheckbutton', background='#1e1e1e', foreground='#ffffff')
        self.style.configure('TNotebook', background='#1e1e1e')
        self.style.configure('TNotebook.Tab', background='#2b2b2b', foreground='#ffffff')
        
        # Data storage
        self.parsed_data = None
        self.analysis_results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with compatible font
        title_label = tk.Label(main_container, text="Leaked Data Parser & Analyzer", 
                              fg='#4CAF50', bg='#1e1e1e')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(main_container, text="Complete Suite v3.0.0 - Integrated Parsing, Analysis & Export", 
                                 fg='#888888', bg='#1e1e1e')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Tab 1: Data Parsing
        self.setup_parsing_tab()
        
        # Tab 2: Data Analysis
        self.setup_analysis_tab()
        
        # Tab 3: Export Options
        self.setup_export_tab()
        
        # Tab 4: Results & Reports
        self.setup_results_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to start data parsing and analysis")
        status_bar = tk.Label(main_container, textvariable=self.status_var, 
                             fg='#888888', bg='#2b2b2b', relief='sunken')
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def setup_parsing_tab(self):
        """Setup the data parsing tab"""
        parsing_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(parsing_frame, text="Data Parsing")
        
        # Input directory selection
        ttk.Label(parsing_frame, text="Input Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(parsing_frame, textvariable=self.input_var, width=80)
        input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(parsing_frame, text="Browse", command=self.browse_input)
        browse_btn.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Output directory selection
        ttk.Label(parsing_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(parsing_frame, textvariable=self.output_var, width=80)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        output_browse_btn = ttk.Button(parsing_frame, text="Browse", command=self.browse_output)
        output_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Parse button
        self.parse_btn = ttk.Button(parsing_frame, text="Start Complete Analysis", 
                                   command=self.start_complete_analysis)
        self.parse_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(parsing_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Parsing log
        ttk.Label(parsing_frame, text="Parsing Log:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        self.parsing_log = scrolledtext.ScrolledText(parsing_frame, height=15, width=100, 
                                                   bg='#2b2b2b', fg='#ffffff')
        self.parsing_log.grid(row=5, column=0, columnspan=3, pady=5)
        
        parsing_frame.columnconfigure(1, weight=1)
        
    def setup_analysis_tab(self):
        """Setup the data analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(analysis_frame, text="Data Analysis")
        
        # Analysis controls
        controls_frame = ttk.Frame(analysis_frame)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.analyze_btn = ttk.Button(controls_frame, text="Run Security Analysis", 
                                     command=self.run_analysis)
        self.analyze_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.export_analysis_btn = ttk.Button(controls_frame, text="Export Analysis Report", 
                                             command=self.export_analysis)
        self.export_analysis_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.view_summary_btn = ttk.Button(controls_frame, text="View Summary", 
                                          command=self.view_summary)
        self.view_summary_btn.grid(row=0, column=2)
        
        # Analysis results
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, height=30, width=100, 
                                                     bg='#2b2b2b', fg='#ffffff')
        self.analysis_text.grid(row=1, column=0, columnspan=2, pady=10)
        
        analysis_frame.columnconfigure(0, weight=1)
        
    def setup_export_tab(self):
        """Setup the export options tab"""
        export_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(export_frame, text="Export Options")
        
        # Export formats selection
        ttk.Label(export_frame, text="Select Export Formats:").grid(row=0, column=0, sticky=tk.W, pady=(0, 20))
        
        # Create checkboxes for export formats
        self.export_formats = {
            'json': tk.BooleanVar(value=True),
            'csv': tk.BooleanVar(value=False),
            'excel': tk.BooleanVar(value=False),
            'html': tk.BooleanVar(value=False),
            'pdf': tk.BooleanVar(value=False)
        }
        
        formats_frame = ttk.Frame(export_frame)
        formats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        row = 0
        col = 0
        for format_name, var in self.export_formats.items():
            cb = ttk.Checkbutton(formats_frame, text=f"{format_name.upper()} Format", variable=var)
            cb.grid(row=row, column=col, padx=20, pady=10, sticky=tk.W)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Export buttons
        buttons_frame = ttk.Frame(export_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        select_all_btn = ttk.Button(buttons_frame, text="Select All", command=self.select_all_formats)
        select_all_btn.grid(row=0, column=0, padx=5)
        
        deselect_all_btn = ttk.Button(buttons_frame, text="Deselect All", command=self.deselect_all_formats)
        deselect_all_btn.grid(row=0, column=1, padx=5)
        
        self.export_btn = ttk.Button(buttons_frame, text="Export Selected Formats", 
                                    command=self.export_selected_formats)
        self.export_btn.grid(row=0, column=2, padx=20)
        
        # Export log
        ttk.Label(export_frame, text="Export Log:").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        self.export_log = scrolledtext.ScrolledText(export_frame, height=15, width=100, 
                                                  bg='#2b2b2b', fg='#ffffff')
        self.export_log.grid(row=4, column=0, columnspan=2, pady=5)
        
        export_frame.columnconfigure(0, weight=1)
        
    def setup_results_tab(self):
        """Setup the results and reports tab"""
        results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(results_frame, text="Results & Reports")
        
        # Quick stats
        stats_frame = ttk.LabelFrame(results_frame, text="Quick Statistics", padding="10")
        stats_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.stats_text = tk.Text(stats_frame, height=8, width=80, bg='#2b2b2b', fg='#ffffff')
        self.stats_text.grid(row=0, column=0, pady=5)
        
        # Action buttons
        actions_frame = ttk.Frame(results_frame)
        actions_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        open_output_btn = ttk.Button(actions_frame, text="Open Output Folder", 
                                    command=self.open_output_folder)
        open_output_btn.grid(row=0, column=0, padx=5)
        
        view_report_btn = ttk.Button(actions_frame, text="View HTML Report", 
                                    command=self.view_html_report)
        view_report_btn.grid(row=0, column=1, padx=5)
        
        clear_data_btn = ttk.Button(actions_frame, text="Clear All Data", 
                                   command=self.clear_all_data)
        clear_data_btn.grid(row=0, column=2, padx=5)
        
        # Results log
        ttk.Label(results_frame, text="Results Log:").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        self.results_log = scrolledtext.ScrolledText(results_frame, height=15, width=100, 
                                                   bg='#2b2b2b', fg='#ffffff')
        self.results_log.grid(row=3, column=0, columnspan=2, pady=5)
        
        results_frame.columnconfigure(0, weight=1)
        
    def browse_input(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_var.set(directory)
            self.log_message("Input directory selected: " + directory, "parsing")
            
    def browse_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
            self.log_message("Output directory selected: " + directory, "parsing")
            
    def log_message(self, message, tab="parsing"):
        """Log message to appropriate tab"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        if tab == "parsing":
            self.parsing_log.insert(tk.END, formatted_message)
            self.parsing_log.see(tk.END)
        elif tab == "export":
            self.export_log.insert(tk.END, formatted_message)
            self.export_log.see(tk.END)
        elif tab == "results":
            self.results_log.insert(tk.END, formatted_message)
            self.results_log.see(tk.END)
        
        self.root.update()
        
    def start_complete_analysis(self):
        """Start complete parsing and analysis process"""
        input_dir = self.input_var.get()
        output_dir = self.output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories")
            return
            
        # Disable buttons and start progress
        self.parse_btn.config(state='disabled')
        self.progress.start()
        
        # Start processing in separate thread
        thread = threading.Thread(target=self.complete_analysis_process, args=(input_dir, output_dir))
        thread.daemon = True
        thread.start()
        
    def complete_analysis_process(self, input_dir, output_dir):
        """Complete analysis process including parsing and analysis"""
        try:
            self.log_message("Starting complete data analysis process...", "parsing")
            
            # Step 1: Parse data
            self.log_message("Step 1: Parsing data from all sources...", "parsing")
            parser = InfoStealerParser(input_dir)
            self.parsed_data = parser.parse_all()
            
            if not self.parsed_data['sessions']:
                self.log_message("No data found to parse", "parsing")
                messagebox.showwarning("Warning", "No data found to parse. Please check your input directory.")
                return
            
            self.log_message(f"Found {self.parsed_data['metadata']['total_sessions']} sessions", "parsing")
            self.log_message(f"Stealer types: {', '.join(self.parsed_data['metadata']['stealer_types'])}", "parsing")
            
            # Step 2: Analyze data
            self.log_message("Step 2: Running security analysis...", "parsing")
            analyzer = DataAnalyzer(self.parsed_data)
            self.analysis_results = analyzer.analyze_all()
            
            self.log_message("Analysis completed successfully!", "parsing")
            
            # Step 3: Update UI
            self.root.after(0, self.update_analysis_display)
            self.root.after(0, self.update_stats_display)
            
            self.log_message("Complete analysis process finished!", "parsing")
            self.log_message("Data ready for export and reporting", "results")
            
            messagebox.showinfo("Success", "Complete analysis finished successfully!\nData is ready for export and reporting.")
            
        except Exception as e:
            self.log_message(f"Error during analysis: {str(e)}", "parsing")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        finally:
            # Re-enable buttons and stop progress
            self.root.after(0, lambda: self.parse_btn.config(state='normal'))
            self.root.after(0, self.progress.stop)
            
    def run_analysis(self):
        """Run analysis on existing parsed data"""
        if not self.parsed_data:
            messagebox.showwarning("Warning", "No parsed data available. Please run data parsing first.")
            return
            
        try:
            self.analyze_btn.config(state='disabled')
            
            analyzer = DataAnalyzer(self.parsed_data)
            self.analysis_results = analyzer.analyze_all()
            
            self.update_analysis_display()
            self.update_stats_display()
            
            self.log_message("Analysis completed successfully!", "results")
            
        except Exception as e:
            self.log_message(f"Error during analysis: {str(e)}", "results")
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            
        finally:
            self.analyze_btn.config(state='normal')
            
    def update_analysis_display(self):
        """Update the analysis display"""
        if not self.analysis_results:
            return
            
        # Clear previous content
        self.analysis_text.delete(1.0, tk.END)
        
        # Display analysis results
        analysis_text = "=== SECURITY ANALYSIS RESULTS ===\n\n"
        
        # Statistics
        stats = self.analysis_results.get('statistics', {})
        analysis_text += f"STATISTICS:\n"
        analysis_text += f"- Total Sessions: {stats.get('total_sessions', 0)}\n"
        analysis_text += f"- Total Passwords: {stats.get('total_passwords', 0)}\n"
        analysis_text += f"- Total Cookies: {stats.get('total_cookies', 0)}\n"
        analysis_text += f"- Most Active Stealer: {stats.get('most_active_stealer', ['Unknown', 0])[0]}\n\n"
        
        # Security Analysis
        threats = self.analysis_results.get('threat_analysis', {})
        analysis_text += f"SECURITY ANALYSIS:\n"
        analysis_text += f"- Risk Level: {threats.get('risk_level', 'Unknown')}\n"
        analysis_text += f"- Risk Score: {threats.get('risk_score', 0)}/100\n"
        analysis_text += f"- Total Threats: {threats.get('total_threats', 0)}\n\n"
        
        # Password Analysis
        password_analysis = self.analysis_results.get('password_analysis', {})
        analysis_text += f"PASSWORD ANALYSIS:\n"
        analysis_text += f"- Weak Password %: {password_analysis.get('weak_password_percentage', 0):.1f}%\n"
        analysis_text += f"- Unique Passwords: {password_analysis.get('unique_passwords', 0)}\n"
        analysis_text += f"- Password Reuse: {password_analysis.get('password_reuse_rate', 0)}\n\n"
        
        # Recommendations
        recommendations = self.analysis_results.get('recommendations', [])
        analysis_text += f"RECOMMENDATIONS ({len(recommendations)}):\n"
        for i, rec in enumerate(recommendations, 1):
            analysis_text += f"{i}. [{rec['priority']}] {rec['recommendation']}\n"
        
        self.analysis_text.insert(tk.END, analysis_text)
        
    def update_stats_display(self):
        """Update the statistics display"""
        if not self.analysis_results:
            return
            
        # Clear previous content
        self.stats_text.delete(1.0, tk.END)
        
        stats = self.analysis_results.get('statistics', {})
        threats = self.analysis_results.get('threat_analysis', {})
        
        stats_text = f"QUICK STATS:\n"
        stats_text += f"Sessions: {stats.get('total_sessions', 0)}\n"
        stats_text += f"Passwords: {stats.get('total_passwords', 0)}\n"
        stats_text += f"Cookies: {stats.get('total_cookies', 0)}\n"
        stats_text += f"Risk Level: {threats.get('risk_level', 'Unknown')}\n"
        stats_text += f"Risk Score: {threats.get('risk_score', 0)}/100\n"
        stats_text += f"Threats: {threats.get('total_threats', 0)}\n"
        
        self.stats_text.insert(tk.END, stats_text)
        
    def select_all_formats(self):
        """Select all export formats"""
        for var in self.export_formats.values():
            var.set(True)
        self.log_message("All export formats selected", "export")
        
    def deselect_all_formats(self):
        """Deselect all export formats"""
        for var in self.export_formats.values():
            var.set(False)
        self.log_message("All export formats deselected", "export")
        
    def export_selected_formats(self):
        """Export data in selected formats"""
        if not self.parsed_data:
            messagebox.showwarning("Warning", "No parsed data available. Please run data parsing first.")
            return
            
        output_dir = self.output_var.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select output directory")
            return
            
        # Get selected formats
        selected_formats = [fmt for fmt, var in self.export_formats.items() if var.get()]
        
        if not selected_formats:
            messagebox.showerror("Error", "Please select at least one export format")
            return
            
        # Start export process
        thread = threading.Thread(target=self.export_process, args=(output_dir, selected_formats))
        thread.daemon = True
        thread.start()
        
    def export_process(self, output_dir, selected_formats):
        """Export data in multiple formats"""
        try:
            self.export_btn.config(state='disabled')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            successful_exports = []
            failed_exports = []
            
            self.log_message(f"Starting multi-format export ({len(selected_formats)} formats)...", "export")
            
            for export_format in selected_formats:
                try:
                    output_filename = f"complete_analysis_{timestamp}.{export_format}"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    self.log_message(f"Exporting to {export_format.upper()}...", "export")
                    
                    if export_format == "json":
                        success, message = DataExporter.export_json(self.parsed_data, output_path)
                    elif export_format == "csv":
                        success, message = DataExporter.export_csv(self.parsed_data, output_path)
                    elif export_format == "excel":
                        success, message = DataExporter.export_excel(self.parsed_data, output_path)
                    elif export_format == "html":
                        success, message = DataExporter.export_html(self.parsed_data, output_path)
                    elif export_format == "pdf":
                        success, message = DataExporter.export_pdf(self.parsed_data, output_path)
                    else:
                        success, message = False, "Unsupported export format"
                    
                    if success:
                        self.log_message(f"{export_format.upper()} export successful: {output_filename}", "export")
                        successful_exports.append(export_format.upper())
                    else:
                        self.log_message(f"{export_format.upper()} export failed: {message}", "export")
                        failed_exports.append(export_format.upper())
                        
                except Exception as e:
                    self.log_message(f"Error exporting {export_format.upper()}: {str(e)}", "export")
                    failed_exports.append(export_format.upper())
            
            # Export analysis report
            if self.analysis_results:
                analysis_filename = f"security_analysis_{timestamp}.json"
                analysis_path = os.path.join(output_dir, analysis_filename)
                
                try:
                    with open(analysis_path, 'w', encoding='utf-8') as f:
                        json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
                    self.log_message(f"Security analysis exported: {analysis_filename}", "export")
                except Exception as e:
                    self.log_message(f"Error exporting analysis: {str(e)}", "export")
            
            # Summary
            self.log_message("Export Summary:", "export")
            self.log_message(f"Successful: {', '.join(successful_exports)}", "export")
            if failed_exports:
                self.log_message(f"Failed: {', '.join(failed_exports)}", "export")
            
            if successful_exports:
                messagebox.showinfo("Export Complete", 
                                  f"Successfully exported data in {len(successful_exports)} format(s):\n"
                                  f"{', '.join(successful_exports)}\n\n"
                                  f"Files saved to: {output_dir}")
            else:
                messagebox.showerror("Export Failed", "All export formats failed. Check the log for details.")
                
        except Exception as e:
            self.log_message(f"Export error: {str(e)}", "export")
            messagebox.showerror("Export Error", f"Export failed: {str(e)}")
            
        finally:
            self.export_btn.config(state='normal')
            
    def export_analysis(self):
        """Export analysis report"""
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results available. Please run analysis first.")
            return
            
        output_dir = self.output_var.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select output directory")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"security_analysis_{timestamp}.json")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
            
            self.log_message(f"Analysis report exported: {output_path}", "results")
            messagebox.showinfo("Success", f"Analysis report exported successfully!\nFile: {output_path}")
            
        except Exception as e:
            self.log_message(f"Error exporting analysis: {str(e)}", "results")
            messagebox.showerror("Error", f"Failed to export analysis: {str(e)}")
            
    def view_summary(self):
        """View analysis summary"""
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results available. Please run analysis first.")
            return
            
        analyzer = DataAnalyzer(self.parsed_data)
        summary = analyzer.generate_summary_report()
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Security Analysis Summary")
        summary_window.geometry("800x600")
        summary_window.configure(bg='#1e1e1e')
        
        summary_text = scrolledtext.ScrolledText(summary_window, bg='#2b2b2b', fg='#ffffff')
        summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        summary_text.insert(tk.END, summary)
        
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_dir = self.output_var.get()
        if output_dir and os.path.exists(output_dir):
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                os.system(f"open '{output_dir}'")
            else:
                os.system(f"xdg-open '{output_dir}'")
        else:
            messagebox.showwarning("Warning", "Output directory not set or does not exist")
            
    def view_html_report(self):
        """View HTML report in browser"""
        output_dir = self.output_var.get()
        if not output_dir:
            messagebox.showwarning("Warning", "Output directory not set")
            return
            
        # Look for HTML files
        html_files = list(Path(output_dir).glob("*.html"))
        if html_files:
            # Open the most recent HTML file
            latest_html = max(html_files, key=lambda x: x.stat().st_mtime)
            webbrowser.open(f"file://{latest_html.absolute()}")
        else:
            messagebox.showwarning("Warning", "No HTML reports found. Please export data in HTML format first.")
            
    def clear_all_data(self):
        """Clear all parsed and analyzed data"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.parsed_data = None
            self.analysis_results = None
            
            # Clear displays
            self.parsing_log.delete(1.0, tk.END)
            self.analysis_text.delete(1.0, tk.END)
            self.export_log.delete(1.0, tk.END)
            self.results_log.delete(1.0, tk.END)
            self.stats_text.delete(1.0, tk.END)
            
            self.log_message("All data cleared", "results")
            self.status_var.set("Ready to start data parsing and analysis")

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = IntegratedParserApp(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
