#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Routine Generator for Conflict-Free Scheduling System

This script generates a PDF routine from an input file (CSV or JSON).
Usage: python generate_routine.py input_file [batch_code] [section]
"""

import os
import sys
import time
from datetime import datetime

# Make sure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import necessary components
from src.scheduler import ConflictFreeScheduler, Activity
from src.utils.file_parser import FileParser
from src.utils.pdf_generator import AcademicPDFGenerator


def print_usage():
    """Print usage information"""
    print("\nUsage:")
    print("  python generate_routine.py input_file [batch_code] [section]")
    print("\nExample:")
    print("  python generate_routine.py data/my_courses.csv BCSE24 A")
    print("  python generate_routine.py data/activities.json")


def main():
    """Main function"""
    # Check arguments
    if len(sys.argv) < 2:
        print("❌ Error: Input file required")
        print_usage()
        return 1
    
    # Parse arguments
    input_file = sys.argv[1]
    batch_code = sys.argv[2] if len(sys.argv) > 2 else "BCSE24"
    section = sys.argv[3] if len(sys.argv) > 3 else "A"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' does not exist")
        print_usage()
        return 1
    
    print("=" * 70)
    print("🎓 CONFLICT-FREE SCHEDULING SYSTEM - PDF ROUTINE GENERATOR")
    print("=" * 70)
    print(f"Input file: {input_file}")
    print(f"Batch: {batch_code}, Section: {section}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 70)
    
    # Load data from input file
    print("\n🔄 Loading data from input file...")
    
    try:
        if input_file.lower().endswith('.csv'):
            activities = FileParser.parse_csv(input_file)
        elif input_file.lower().endswith('.json'):
            activities = FileParser.parse_json(input_file)
        else:
            print(f"❌ Error: Unsupported file format. Use CSV or JSON")
            return 1
        
        print(f"✅ Loaded {len(activities)} activities")
        
        # Initialize scheduler
        print("\n🔄 Generating conflict-free schedule...")
        scheduler = ConflictFreeScheduler()
        
        # Run the graph coloring algorithm (fastest for most cases)
        start_time = time.time()
        result = scheduler.graph_coloring_schedule(activities)
        execution_time = (time.time() - start_time) * 1000  # ms
        
        print(f"✅ Schedule generated in {execution_time:.2f}ms")
        print(f"📊 Scheduled {len(result)}/{len(activities)} activities")
        
        # Check if we got all activities scheduled
        if len(result) < len(activities):
            print(f"⚠️  Warning: Could not schedule all activities due to conflicts")
            print(f"⚠️  {len(activities) - len(result)} activities could not be scheduled")
        
        # Generate academic PDF output
        print("\n🔄 Generating PDF routine...")
        os.makedirs("output", exist_ok=True)
        
        # Generate filename based on batch and section
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"academic_schedule_{batch_code}_{section}_{timestamp}.html"
        
        pdf_gen = AcademicPDFGenerator()
        output_path = pdf_gen.generate_academic_schedule(
            result,
            batch_code=batch_code,
            section=section,
            semester=f"Summer 2025",  # You can change this or add as parameter
            filename=filename
        )
        
        print(f"\n✅ Academic routine saved to: {output_path}")
        print("Open the HTML file in your browser to view and print the routine.")
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
