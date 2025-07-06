#!/usr/bin/env python3
"""
Command Line Interface for Leaked Data Parser & Analyzer
Advanced CLI with ClickHouse integration and rich output
"""

import click
import sys
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from stealer_parser import InfoStealerParser, DataExporter
    from data_analyzer import DataAnalyzer
    from clickhouse_client import ClickHouseClient
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rprint
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

@click.group()
@click.version_option(version="3.0.0", prog_name="Leaked Data Parser")
def cli():
    """
    �� Leaked Data Parser & Analyzer CLI
    
    Advanced command-line tool for parsing, analyzing, and storing leaked data
    with ClickHouse integration for real-time analytics.
    """
    pass

@cli.command()
@click.option('--input', '-i', 'input_dir', required=True, 
              help='Input directory containing data files')
@click.option('--output', '-o', 'output_dir', required=True,
              help='Output directory for parsed results')
@click.option('--formats', '-f', multiple=True, 
              default=['json'], 
              type=click.Choice(['json', 'csv', 'excel', 'html', 'pdf']),
              help='Export formats (multiple allowed)')
@click.option('--analyze', '-a', is_flag=True, 
              help='Run security analysis after parsing')
@click.option('--clickhouse', '-c', is_flag=True,
              help='Store results in ClickHouse database')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def parse(input_dir: str, output_dir: str, formats: List[str], 
          analyze: bool, clickhouse: bool, verbose: bool):
    """
    Parse leaked data from various sources and formats.
    
    Example:
        python cli_parser.py parse -i ./data -o ./results -f json csv -a -c
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Initialize parser
            task = progress.add_task("Initializing parser...", total=None)
            parser = InfoStealerParser()
            progress.update(task, description="Parser initialized")
            
            # Parse data
            progress.update(task, description="Parsing data files...")
            parsed_data = parser.parse_directory(input_dir)
            
            if not parsed_data:
                console.print("[red]❌ No data found to parse[/red]")
                return
            
            progress.update(task, description="Data parsing completed")
            
            # Export data
            if formats:
                progress.update(task, description="Exporting data...")
                exporter = DataExporter()
                
                for fmt in formats:
                    progress.update(task, description=f"Exporting to {fmt.upper()}...")
                    if fmt == 'json':
                        exporter.export_json(parsed_data, output_dir)
                    elif fmt == 'csv':
                        exporter.export_csv(parsed_data, output_dir)
                    elif fmt == 'excel':
                        exporter.export_excel(parsed_data, output_dir)
                    elif fmt == 'html':
                        exporter.export_html(parsed_data, output_dir)
                    elif fmt == 'pdf':
                        exporter.export_pdf(parsed_data, output_dir)
            
            # Run analysis if requested
            if analyze:
                progress.update(task, description="Running security analysis...")
                analyzer = DataAnalyzer(parsed_data)
                analysis_results = analyzer.analyze_all()
                
                # Export analysis
                analysis_file = os.path.join(output_dir, "security_analysis.json")
                with open(analysis_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis_results, f, indent=2, ensure_ascii=False)
            
            # Store in ClickHouse if requested
            if clickhouse:
                progress.update(task, description="Storing in ClickHouse...")
                ch_client = ClickHouseClient()
                ch_client.store_data(parsed_data)
            
            progress.update(task, description="✅ All operations completed successfully!")
            
        # Display summary
        display_summary(parsed_data, output_dir, formats, analyze, clickhouse)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        if verbose:
            console.print_exception()

@cli.command()
@click.option('--data-file', '-d', required=True,
              help='JSON file containing parsed data')
@click.option('--output', '-o', required=True,
              help='Output directory for analysis results')
def analyze(data_file: str, output: str):
    """
    Run security analysis on parsed data.
    
    Example:
        python cli_parser.py analyze -d ./results/unified_data.json -o ./analysis
    """
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analyzer = DataAnalyzer(data)
        results = analyzer.analyze_all()
        
        # Export analysis
        output_file = os.path.join(output, "security_analysis.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✅ Analysis completed and saved to {output_file}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")

@cli.command()
@click.option('--query', '-q', required=True,
              help='SQL query to execute on ClickHouse')
@click.option('--format', '-f', default='table',
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format')
def query(query: str, format: str):
    """
    Execute queries on ClickHouse database.
    
    Example:
        python cli_parser.py query -q "SELECT COUNT(*) FROM leaked_data"
    """
    try:
        ch_client = ClickHouseClient()
        results = ch_client.execute_query(query)
        
        if format == 'table':
            display_query_results(results)
        elif format == 'json':
            console.print_json(json.dumps(results, indent=2))
        elif format == 'csv':
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(results)
            console.print(output.getvalue())
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")

@cli.command()
def status():
    """
    Check ClickHouse connection and database status.
    """
    try:
        ch_client = ClickHouseClient()
        status_info = ch_client.get_status()
        
        table = Table(title="ClickHouse Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        for component, info in status_info.items():
            table.add_row(component, info['status'], info['details'])
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")

def display_summary(data: dict, output_dir: str, formats: List[str], 
                   analyze: bool, clickhouse: bool):
    """Display operation summary"""
    
    summary = Table(title="Operation Summary")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="green")
    
    # Count records
    total_records = sum(len(records) for records in data.values() if isinstance(records, list))
    summary.add_row("Total Records", str(total_records))
    
    # Data types
    data_types = list(data.keys())
    summary.add_row("Data Types", ", ".join(data_types))
    
    # Export formats
    summary.add_row("Export Formats", ", ".join(formats))
    
    # Analysis
    summary.add_row("Security Analysis", "✅ Yes" if analyze else "❌ No")
    
    # ClickHouse
    summary.add_row("ClickHouse Storage", "✅ Yes" if clickhouse else "❌ No")
    
    # Output directory
    summary.add_row("Output Directory", output_dir)
    
    console.print(summary)

def display_query_results(results: List[tuple]):
    """Display query results in a table"""
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return
    
    table = Table(title="Query Results")
    
    # Add columns based on first row
    for i, col in enumerate(results[0]):
        table.add_column(f"Column {i+1}", style="cyan")
    
    # Add rows
    for row in results:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)

if __name__ == '__main__':
    cli()
