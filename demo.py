#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example script demonstrating the Conflict-Free Scheduling System
This script shows how to use the system programmatically.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scheduler import ConflictFreeScheduler, Activity
from utils.file_parser import FileParser
from utils.pdf_generator import PDFGenerator, AcademicPDFGenerator


def create_sample_activities():
    """Create sample activities for demonstration"""
    activities = [
        Activity(1, 0, 90, 3.0, "Programming Fundamentals", "CSE-101"),
        Activity(2, 100, 190, 3.0, "Data Structures", "CSE-102"),
        Activity(3, 50, 140, 1.0, "Programming Lab", "LAB-1"),  # Conflicts with Activity 1
        Activity(4, 200, 290, 3.0, "Algorithms", "CSE-101"),
        Activity(5, 150, 210, 1.5, "Database Lab", "LAB-2"),
        Activity(6, 300, 390, 3.0, "Software Engineering", "CSE-201"),
        Activity(7, 400, 490, 3.0, "Computer Networks", "CSE-202"),
        Activity(8, 350, 410, 1.0, "Network Lab", "LAB-1"),  # Conflicts with Activity 6
        Activity(9, 500, 590, 3.0, "Operating Systems", "CSE-101"),
        Activity(10, 600, 690, 1.5, "OS Lab", "LAB-2"),
    ]
    return activities


def demonstrate_basic_usage():
    """Demonstrate basic usage of the scheduler"""
    print("🔄 Creating sample activities...")
    activities = create_sample_activities()
    
    print(f"📊 Created {len(activities)} activities")
    print("\nSample activities:")
    for i, activity in enumerate(activities[:3]):  # Show first 3
        print(f"  {i+1}. {activity}")
    print("  ...")
    
    # Initialize scheduler
    scheduler = ConflictFreeScheduler()
    
    # Test conflict detection
    print(f"\n🔍 Conflict check: Activity 1 vs Activity 3")
    has_conflict = scheduler.has_conflict(activities[0], activities[2])
    print(f"   Result: {'Conflict detected' if has_conflict else 'No conflict'}")
    
    # Calculate total weight
    total_weight = scheduler.calculate_total_weight(activities)
    print(f"\n📈 Total weight of all activities: {total_weight}")
    
    return activities


def demonstrate_algorithms(activities):
    """Demonstrate all four algorithms"""
    scheduler = ConflictFreeScheduler()
    algorithms = {
        "Graph Coloring": "graph_coloring_schedule",
        "Dynamic Programming": "dp_schedule", 
        "Backtracking": "backtracking_schedule",
        "Genetic Algorithm": "genetic_algorithm_schedule"
    }
    
    results = {}
    
    print("\n🚀 Running all algorithms:")
    print("=" * 50)
    
    for name, method in algorithms.items():
        print(f"\n🔄 Running {name}...")
        try:
            # Get the method from scheduler
            algorithm_method = getattr(scheduler, method)
            result = algorithm_method(activities)
            results[name] = result
            
            # Print results
            scheduled_count = len(result)
            total_weight = scheduler.calculate_total_weight(result)
            efficiency = (scheduled_count / len(activities)) * 100
            
            print(f"   ✅ Scheduled: {scheduled_count}/{len(activities)} activities")
            print(f"   📊 Total weight: {total_weight:.2f}")
            print(f"   📈 Efficiency: {efficiency:.1f}%")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[name] = []
    
    return results


def demonstrate_file_operations():
    """Demonstrate file I/O operations"""
    print("\n📁 File Operations:")
    print("=" * 30)
    
    # Generate sample data
    print("📝 Generating sample data file...")
    sample_file = "data/demo_activities.csv"
    success = FileParser.generate_sample_data(sample_file, 8)
    
    if success:
        print(f"   ✅ Generated: {sample_file}")
        
        # Read the file back
        print("📖 Reading sample data...")
        activities = FileParser.parse_csv(sample_file)
        print(f"   ✅ Loaded {len(activities)} activities")
        
        # Save as JSON
        json_file = "data/demo_activities.json"
        print(f"💾 Saving as JSON: {json_file}")
        FileParser.write_json(activities, json_file)
        
        return activities
    else:
        print("   ❌ Failed to generate sample data")
        return []


def demonstrate_pdf_generation(activities, results):
    """Demonstrate PDF generation"""
    if not activities or not results:
        print("⚠️  Skipping PDF generation (no data)")
        return
    
    print("\n📄 PDF Generation:")
    print("=" * 25)
    
    # Get best result
    scheduler = ConflictFreeScheduler()
    best_algorithm = max(results.keys(), 
                        key=lambda k: scheduler.calculate_total_weight(results[k])
                        if results[k] else 0)
    best_result = results[best_algorithm]
    
    if not best_result:
        print("⚠️  No valid results for PDF generation")
        return
    
    print(f"🏆 Best result: {best_algorithm}")
    
    # Generate basic PDF
    print("📄 Generating basic HTML schedule...")
    pdf_gen = PDFGenerator()
    html_file = pdf_gen.generate_schedule_html(
        best_result, 
        f"Demo Schedule - {best_algorithm}"
    )
    print(f"   ✅ Generated: {html_file}")
    
    # Generate academic PDF
    print("🎓 Generating academic schedule...")
    academic_gen = AcademicPDFGenerator()
    academic_file = academic_gen.generate_academic_schedule(
        best_result,
        batch_code="BCSE24",
        section="A",
        semester="Spring 2025"
    )
    print(f"   ✅ Generated: {academic_file}")


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("=== Conflict-Free Scheduling System Demo ===")
    print("=" * 60)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Demonstrate basic usage
    activities = demonstrate_basic_usage()
    
    # Demonstrate algorithms
    results = demonstrate_algorithms(activities)
    
    # Demonstrate file operations
    file_activities = demonstrate_file_operations()
    
    # Use file activities if available, otherwise use sample activities
    demo_activities = file_activities if file_activities else activities
    
    # Demonstrate PDF generation
    demonstrate_pdf_generation(demo_activities, results)
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("Check the 'output' directory for generated files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
