#!/usr/bin/env python3
"""
PDF Location Demonstration Script
Shows exactly where generated PDFs are located
"""

import os
import glob

def show_pdf_locations():
    print("🎯 PDF Location Demonstration")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, 'output')
    
    print(f"📂 Project Directory: {current_dir}")
    print(f"📁 Output Directory: {output_dir}")
    print()
    
    # Find all PDF files
    pdf_pattern = os.path.join(output_dir, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    
    if pdf_files:
        print(f"📄 Found {len(pdf_files)} PDF files:")
        print("-" * 50)
        
        for i, pdf_file in enumerate(sorted(pdf_files), 1):
            filename = os.path.basename(pdf_file)
            file_size = os.path.getsize(pdf_file)
            print(f"{i}. {filename}")
            print(f"   📍 Full path: {pdf_file}")
            print(f"   📏 Size: {file_size} bytes")
            print()
    else:
        print("❌ No PDF files found in output directory")
        print("🔧 Run the following command to generate PDFs:")
        print("   python main.py --academic-pdf --batch BCSE24 --section A")
    
    # Show HTML files too
    html_pattern = os.path.join(output_dir, "*.html")
    html_files = glob.glob(html_pattern)
    
    if html_files:
        print(f"🌐 Found {len(html_files)} HTML files:")
        print("-" * 50)
        
        for i, html_file in enumerate(sorted(html_files), 1):
            filename = os.path.basename(html_file)
            print(f"{i}. {filename}")
            print(f"   📍 Full path: {html_file}")
        print()
    
    print("🚀 To generate new PDFs, use:")
    print("   python main.py --academic-pdf --batch BCSE24 --section A")
    print("   python main.py --enhanced --batch BCSE24 --section A")
    print("   python main.py --comprehensive --enhanced")

if __name__ == "__main__":
    show_pdf_locations()
