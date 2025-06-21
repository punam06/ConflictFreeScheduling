#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Run Script for Conflict-Free Scheduling System

This script automatically generates a PDF schedule with default settings.
Just click the run button to execute it and get a PDF schedule.
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
from src.utils.pdf_generator import PDFGenerator, AcademicPDFGenerator


def print_banner():
    """Print a banner to the console"""
    print("=" * 70)
    print("🎓 CONFLICT-FREE SCHEDULING SYSTEM - QUICK RUN")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("Automatically generating conflict-free schedule...")
    print("=" * 70)


def load_or_create_data():
    """Load data from default location or create sample data"""
    # Try to load from CSV first
    csv_file = "data/demo_activities.csv"
    json_file = "data/demo_activities.json"
    
    if os.path.exists(csv_file):
        print(f"📂 Loading activities from {csv_file}")
        return FileParser.parse_csv(csv_file)
    elif os.path.exists(json_file):
        print(f"📂 Loading activities from {json_file}")
        return FileParser.parse_json(json_file)
    else:
        # Create sample data
        print("📝 Creating sample activities...")
        activities = [
            Activity(1, 0, 90, 3.0, "Programming Fundamentals", "Room 101"),
            Activity(2, 100, 190, 3.0, "Data Structures", "Room 102"),
            Activity(3, 50, 140, 1.0, "Programming Lab", "Lab 1"),
            Activity(4, 200, 290, 3.0, "Algorithms", "Room 103"),
            Activity(5, 150, 240, 3.0, "Digital Logic Design", "Room 104"),
            Activity(6, 300, 390, 3.0, "Database Systems", "Room 101"),
            Activity(7, 270, 360, 3.0, "Operating Systems", "Room 102"),
            Activity(8, 400, 490, 1.5, "Database Lab", "Lab 2"),
            Activity(9, 500, 590, 3.0, "Computer Networks", "Room 103"),
            Activity(10, 550, 640, 3.0, "Software Engineering", "Room 104"),
        ]
        
        # Save for future use
        os.makedirs("data", exist_ok=True)
        FileParser.write_csv(activities, csv_file)
        print(f"✅ Saved sample data to {csv_file}")
        
        return activities


def main():
    """Main function that runs everything in sequence"""
    print_banner()
    
    # Load data
    print("\n🔄 Step 1: Loading data...")
    activities = load_or_create_data()
    print(f"✅ Loaded {len(activities)} activities")
    
    # Initialize scheduler
    print("\n🔄 Step 2: Initializing scheduler...")
    scheduler = ConflictFreeScheduler()
    
    # Run the algorithm (Graph Coloring by default as it's typically fastest)
    print("\n🔄 Step 3: Generating conflict-free schedule...")
    start_time = time.time()
    result = scheduler.graph_coloring_schedule(activities)
    execution_time = (time.time() - start_time) * 1000  # ms
    
    print(f"✅ Schedule generated in {execution_time:.2f}ms")
    print(f"📊 Scheduled {len(result)}/{len(activities)} activities")
    print(f"📊 Total schedule weight: {scheduler.calculate_total_weight(result):.2f}")
    
    # Generate PDF output
    print("\n🔄 Step 4: Generating PDF output...")
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Generate academic PDF (looks more professional)
    pdf_gen = AcademicPDFGenerator()
    current_date = datetime.now().strftime("%Y%m%d")
    output_file = f"academic_schedule_{current_date}.html"
    
    pdf_path = pdf_gen.generate_academic_schedule(
        result,
        batch_code="BCSE24",
        section="A",
        semester="Summer 2025",
        filename=output_file
    )
    
    # Also generate basic HTML version
    basic_pdf = PDFGenerator()
    basic_path = basic_pdf.generate_schedule_html(
        result,
        title="Conflict-Free Schedule",
        filename=f"schedule_{current_date}.html"
    )
    
    print(f"\n✅ Academic schedule saved to: {pdf_path}")
    print(f"✅ Basic schedule saved to: {basic_path}")
    print("\n🎉 Done! Your conflict-free schedule is ready.")
    print("Open the HTML files in your browser to view and print the schedule.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
