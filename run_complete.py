#!/usr/bin/env python3
"""
Complete Leaked Data Parser & Analyzer
Unified application with GUI, CLI, and ClickHouse integration
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point with mode selection"""
    
    print("Leaked Data Parser & Analyzer v3.0.0")
    print("=" * 50)
    print("Choose your preferred interface:")
    print("1. GUI Application (Graphical Interface)")
    print("2. CLI Application (Command Line)")
    print("3. ClickHouse Setup & Status")
    print("4. Exit")
    print("=" * 50)
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                # Launch GUI
                try:
                    from main_app import main as gui_main
                    gui_main()
                except ImportError as e:
                    print(f"❌ GUI Error: {e}")
                    print("Please install GUI dependencies: pip install tkinter")
                break
                
            elif choice == '2':
                # Launch CLI
                try:
                    from cli_parser import cli
                    cli()
                except ImportError as e:
                    print(f"❌ CLI Error: {e}")
                    print("Please install CLI dependencies: pip install click rich")
                break
                
            elif choice == '3':
                # ClickHouse setup
                try:
                    from clickhouse_client import ClickHouseClient
                    client = ClickHouseClient()
                    status = client.get_status()
                    
                    print("\n📊 ClickHouse Status:")
                    for component, info in status.items():
                        print(f"  {component}: {info['status']} - {info['details']}")
                    
                    # Show statistics
                    stats = client.get_statistics()
                    print("\n📈 Database Statistics:")
                    for table, count in stats.items():
                        print(f"  {table}: {count} records")
                    
                except Exception as e:
                    print(f"❌ ClickHouse Error: {e}")
                    print("Please ensure ClickHouse is installed and running")
                break
                
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
