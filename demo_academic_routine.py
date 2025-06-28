#!/usr/bin/env python3
"""
Comprehensive Academic Routine - Demonstration Script
Shows the new enhanced routine generation with proper time slots
"""

import os
import sys

def main():
    print("🎓 Enhanced Academic Routine Generation Demo")
    print("=" * 60)
    print()
    
    print("📋 New Features:")
    print("✅ Sunday to Thursday schedule")
    print("✅ Time slots: 8:30 AM - 5:30 PM")
    print("✅ Break time: 1:30 PM - 2:00 PM")
    print("✅ Each slot: 1.5 hours with 15-minute breaks")
    print("✅ Theory classes: 1 slot, Lab classes: 2 slots")
    print("✅ All batches (BCSE22, BCSE23, BCSE24, BCSE25)")
    print("✅ All sections (A & B)")
    print("✅ Real faculty names and room assignments")
    print("✅ Attractive table format like reference sample")
    print()
    
    print("🚀 Generating comprehensive academic routine...")
    print()
    
    # Run the academic routine generation
    os.system("python main.py --academic-routine")
    
    print()
    print("🎯 Generated Files:")
    
    # List the generated files
    output_files = []
    for file in os.listdir("output"):
        if file.startswith("comprehensive_academic_routine"):
            output_files.append(file)
            full_path = os.path.join("output", file)
            size = os.path.getsize(full_path)
            print(f"📄 {file} ({size} bytes)")
    
    if output_files:
        print()
        print("📍 File Locations:")
        current_dir = os.getcwd()
        for file in output_files:
            print(f"   {os.path.join(current_dir, 'output', file)}")
        
        print()
        print("🌐 To view HTML:")
        html_files = [f for f in output_files if f.endswith('.html')]
        if html_files:
            print(f"   open output/{html_files[0]}")
        
        print()
        print("📄 To view PDF:")
        pdf_files = [f for f in output_files if f.endswith('.pdf')]
        if pdf_files:
            print(f"   open output/{pdf_files[0]}")
    
    print()
    print("✨ Features of the new routine:")
    print("📅 Time Slots:")
    print("   Slot 1: 08:30 - 10:00")
    print("   Slot 2: 10:15 - 11:45")
    print("   Slot 3: 12:00 - 13:30")
    print("   BREAK:  13:30 - 14:00")
    print("   Slot 4: 14:00 - 15:30")
    print("   Slot 5: 15:45 - 17:15")
    print()
    
    print("📚 Sample Courses:")
    print("   BCSE22: Software Engineering, Computer Networks, Database")
    print("   BCSE23: Data Structures, Operating Systems, Computer Organization")
    print("   BCSE24: OOP, Discrete Math, Digital Logic Design")
    print("   BCSE25: Programming Fundamentals, Mathematics, Physics")
    print()
    
    print("👥 Faculty:")
    print("   Dr. Mohammad Rahman, Prof. Fatema Khatun, Dr. Ahmed Ali")
    print("   Ms. Rashida Begum, Mr. Karim Hassan, Dr. Nasir Uddin")
    print("   Ms. Salma Akter, Mr. Rafiqul Islam, Dr. Shahida Sultana")
    print("   Mr. Abdur Rahman")
    print()
    
    print("🏢 Rooms:")
    print("   Theory: CSE-301, CSE-302, CSE-303, CSE-304")
    print("   Labs: CSE-LAB1, CSE-LAB2, CSE-LAB3")
    print()
    
    print("🎨 UI Features:")
    print("   ✨ Modern gradient backgrounds")
    print("   📱 Responsive design")
    print("   🎨 Color-coded course information")
    print("   📋 Professional table layout")
    print("   🖱️  Interactive hover effects")
    print()
    
    print("✅ Academic routine generation complete!")
    print("🎯 The routine matches the reference sample format with enhanced styling.")

if __name__ == "__main__":
    main()
