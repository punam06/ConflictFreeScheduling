#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integrated Demo Script for Conflict-Free Scheduling System

This script demonstrates how all components of the system work together
to create professional academic schedules.
"""

import sys
import os
import time
from datetime import datetime
from typing import List, Dict

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import core components
from src import ConflictFreeScheduler, Activity
from src.utils import FileParser, PDFGenerator, AcademicPDFGenerator
from src.algorithms import GraphColoringScheduler, DynamicProgrammingScheduler
from src.algorithms import BacktrackingScheduler, GeneticAlgorithmScheduler

def print_banner():
    """Print the application banner"""
    print("=" * 70)
    print("🎓 CONFLICT-FREE ACADEMIC SCHEDULING SYSTEM - INTEGRATION DEMO")
    print("=" * 70)
    print("Demonstrating all components working together")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 70)

def load_sample_data() -> List[Activity]:
    """Load or generate sample data"""
    print("\n📊 Loading sample data...")
    
    # Try to load from CSV first
    sample_file = "data/demo_activities.csv"
    if os.path.exists(sample_file):
        print(f"📂 Loading activities from {sample_file}")
        activities = FileParser.parse_csv(sample_file)
    else:
        # Generate and save sample data
        print("📝 Generating sample academic activities...")
        activities = [
            Activity(1, 0, 90, 3.0, "Programming Fundamentals", "Room 101"),
            Activity(2, 100, 190, 3.0, "Data Structures", "Room 102"),
            Activity(3, 50, 140, 1.0, "Programming Lab", "Lab 1"),  # Conflicts with Activity 1
            Activity(4, 200, 290, 3.0, "Algorithms", "Room 103"),
            Activity(5, 150, 240, 3.0, "Digital Logic Design", "Room 104"),
            Activity(6, 300, 390, 3.0, "Database Systems", "Room 101"),
            Activity(7, 270, 360, 3.0, "Operating Systems", "Room 102"),  # Conflicts with Activity 6
            Activity(8, 400, 490, 1.5, "Database Lab", "Lab 2"),
            Activity(9, 500, 590, 3.0, "Computer Networks", "Room 103"),
            Activity(10, 550, 640, 3.0, "Software Engineering", "Room 104"),  # Conflicts with Activity 9
        ]
        # Save generated data
        FileParser.write_csv(activities, "data/demo_activities.csv")
        # Also save as JSON
        FileParser.write_json(activities, "data/demo_activities.json")
        
    print(f"✅ Loaded {len(activities)} activities")
    return activities

def run_all_algorithms(activities: List[Activity]) -> Dict[str, List[Activity]]:
    """Run all scheduling algorithms and compare results"""
    print("\n🧠 Running all scheduling algorithms...")
    
    results = {}
    scheduler = ConflictFreeScheduler()
    
    # Graph Coloring Algorithm
    print("\n🔄 Running Graph Coloring algorithm...")
    start_time = time.time()
    results["graph-coloring"] = scheduler.graph_coloring_schedule(activities)
    graph_time = (time.time() - start_time) * 1000  # ms
    print(f"  ✅ Completed in {graph_time:.2f}ms")
    
    # Dynamic Programming Algorithm
    print("\n🔄 Running Dynamic Programming algorithm...")
    start_time = time.time()
    results["dynamic-prog"] = scheduler.dp_schedule(activities)
    dp_time = (time.time() - start_time) * 1000  # ms
    print(f"  ✅ Completed in {dp_time:.2f}ms")
    
    # Backtracking Algorithm
    print("\n🔄 Running Backtracking algorithm...")
    start_time = time.time()
    results["backtracking"] = scheduler.backtracking_schedule(activities)
    bt_time = (time.time() - start_time) * 1000  # ms
    print(f"  ✅ Completed in {bt_time:.2f}ms")
    
    # Genetic Algorithm
    print("\n🔄 Running Genetic Algorithm...")
    start_time = time.time()
    results["genetic"] = scheduler.genetic_algorithm_schedule(activities)
    ga_time = (time.time() - start_time) * 1000  # ms
    print(f"  ✅ Completed in {ga_time:.2f}ms")
    
    # Print comparison table
    print("\n📊 ALGORITHM COMPARISON")
    print("=" * 70)
    print(f"{'Algorithm':<18} {'Activities':<12} {'Total Weight':<15} {'Efficiency %':<12} {'Time (ms)':<12}")
    print("-" * 70)
    
    for name, result in results.items():
        weight = scheduler.calculate_total_weight(result)
        efficiency = len(result) / len(activities) * 100
        time_taken = {
            "graph-coloring": graph_time,
            "dynamic-prog": dp_time,
            "backtracking": bt_time,
            "genetic": ga_time
        }[name]
        
        print(f"{name:<18} {len(result):<12} {weight:<15.2f} {efficiency:<12.1f} {time_taken:<12.2f}")
    
    return results

def generate_output(results: Dict[str, List[Activity]]):
    """Generate output files for each algorithm"""
    print("\n📄 Generating output files...")
    
    # Find best result
    scheduler = ConflictFreeScheduler()
    best_algo = max(results.keys(), key=lambda k: scheduler.calculate_total_weight(results[k]))
    best_result = results[best_algo]
    
    print(f"🏆 Best algorithm: {best_algo.upper()} (selected for PDF generation)")
    
    # Generate basic schedule HTML
    pdf_gen = PDFGenerator()
    filepath = pdf_gen.generate_schedule_html(best_result, f"Schedule - {best_algo.upper()}")
    print(f"✅ Generated basic schedule HTML: {filepath}")
    
    # Generate academic PDF
    academic_pdf = AcademicPDFGenerator()
    filepath = academic_pdf.generate_academic_schedule(
        best_result, 
        batch_code="BCSE24",
        section="A", 
        semester="Summer 2025"
    )
    print(f"✅ Generated academic schedule HTML: {filepath}")
    
    print("\n🔗 View the generated files in the 'output' directory")

def main():
    """Main function"""
    print_banner()
    
    # Load sample data
    activities = load_sample_data()
    
    # Run all algorithms and compare
    results = run_all_algorithms(activities)
    
    # Generate output
    generate_output(results)
    
    print("\n✨ Demo completed successfully!")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
