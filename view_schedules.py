#!/usr/bin/env python3
# View generated schedules in browser

import os
import webbrowser
from pathlib import Path

def main():
    """Open generated schedule files in browser"""
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("❌ No output directory found. Run the scheduling system first.")
        return
    
    html_files = list(output_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found. Run the scheduling system first.")
        return
    
    print("📄 Found schedule files:")
    for i, file in enumerate(html_files, 1):
        print(f"  {i}. {file.name}")
    
    print("\nSelect a file to view (or press Enter to view the latest):")
    choice = input().strip()
    
    if choice:
        try:
            selected_file = html_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid choice")
            return
    else:
        # Get the latest file
        selected_file = max(html_files, key=lambda f: f.stat().st_mtime)
    
    # Open in default web browser
    file_url = f"file:///{selected_file.absolute().as_posix()}"
    webbrowser.open(file_url)
    print(f"🌐 Opening {selected_file.name} in browser...")

if __name__ == "__main__":
    main()
