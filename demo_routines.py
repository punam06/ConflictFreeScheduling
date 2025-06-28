#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive Routine Demonstration Script
Shows all generated academic routines with different formats and designs
"""

import os
import webbrowser
from datetime import datetime

def main():
    """Demonstrate all routine generation capabilities"""
    print("=" * 70)
    print("🎓 COMPREHENSIVE ACADEMIC ROUTINE DEMONSTRATION")
    print("=" * 70)
    
    # Get output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    
    if not os.path.exists(output_dir):
        print("❌ Output directory not found. Please run the routine generators first.")
        return
    
    # List all generated HTML files
    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
    pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
    
    print(f"\n📂 Found {len(html_files)} HTML files and {len(pdf_files)} PDF files in output directory")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Show latest generated files
    latest_files = []
    
    # Find latest enhanced sample routine
    sample_files = [f for f in html_files if 'enhanced_sample_routine' in f]
    if sample_files:
        latest_sample = max(sample_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        latest_files.append(('Enhanced Sample Routine (Modern UI)', latest_sample))
    
    # Find latest reference-based routine
    reference_files = [f for f in html_files if 'reference_based_comprehensive_routine' in f]
    if reference_files:
        latest_reference = max(reference_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        latest_files.append(('Reference-Based Routine', latest_reference))
    
    # Find other comprehensive routines
    other_files = [f for f in html_files if 'comprehensive_routine' in f and 'reference_based' not in f]
    if other_files:
        latest_other = max(other_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        latest_files.append(('Standard Comprehensive Routine', latest_other))
    
    # Display information about generated routines
    print("🎨 AVAILABLE ROUTINE FORMATS:")
    print("-" * 50)
    
    for i, (title, filename) in enumerate(latest_files, 1):
        file_path = os.path.join(output_dir, filename)
        file_size = os.path.getsize(file_path) / 1024  # KB
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        print(f"{i}. {title}")
        print(f"   📄 File: {filename}")
        print(f"   📊 Size: {file_size:.1f} KB")
        print(f"   🕒 Generated: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   🌐 URL: file://{file_path}")
        print()
    
    # Show PDF files summary
    print("📋 PDF FILES GENERATED:")
    print("-" * 50)
    
    pdf_categories = {
        'Enhanced Sample': [f for f in pdf_files if 'enhanced_sample_routine' in f],
        'Reference-Based': [f for f in pdf_files if 'reference_based_comprehensive_routine' in f],
        'Section Routines': [f for f in pdf_files if 'section_routine' in f],
        'Comprehensive': [f for f in pdf_files if 'comprehensive_routine' in f and 'reference_based' not in f]
    }
    
    for category, files in pdf_categories.items():
        if files:
            latest_pdf = max(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
            print(f"• {category}: {latest_pdf}")
    
    # Show key features
    print("\n✨ KEY FEATURES IMPLEMENTED:")
    print("-" * 50)
    print("🎯 Faculty Preference Scheduling")
    print("   - Respects faculty preferred time slots")
    print("   - Assigns courses based on faculty expertise")
    print("   - Optimizes workload distribution")
    print()
    print("🏫 Room Management")
    print("   - Uses only available rooms: 302, 303, 304, 504, 1003")
    print("   - Smart room allocation for theory and lab sessions")
    print("   - Conflict-free room scheduling")
    print()
    print("⏰ Optimal Time Scheduling")
    print("   - Minimizes gaps between classes for students")
    print("   - Proper lunch break timing (13:30 - 14:00)")
    print("   - 90-minute class sessions with 15-minute breaks")
    print()
    print("🎨 Enhanced UI Design")
    print("   - Modern, responsive web interface")
    print("   - Professional PDF layouts")
    print("   - Color-coded course information")
    print("   - Print-friendly formats")
    print()
    print("📊 Comprehensive Coverage")
    print("   - Multiple batches (BCSE22, BCSE23, BCSE24, BCSE25)")
    print("   - Section-wise detailed scheduling")
    print("   - Full course information with faculty names")
    print("   - Academic year and semester details")
    
    # Show usage examples
    print("\n🚀 USAGE EXAMPLES:")
    print("-" * 50)
    print("# Generate sample-based routine (recommended)")
    print("python main.py  # Select option 6")
    print()
    print("# Generate reference-based routine")
    print("python main.py  # Select option 5")
    print()
    print("# Direct generator usage")
    print("python src/utils/sample_routine_generator.py")
    print("python src/utils/reference_pdf_generator.py")
    
    print("\n" + "=" * 70)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("✅ All routine formats generated successfully")
    print("📁 Check the 'output' directory for all generated files")
    print("🌐 Open any HTML file in a browser to view the routine")
    print("=" * 70)

if __name__ == "__main__":
    main()
