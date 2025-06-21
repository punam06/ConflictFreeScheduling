#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conflict-Free Class Scheduling System - Main Application

This is the main entry point for the conflict-free scheduling system.
Enhanced with academic PDF generation and professional BUP scheduling.
"""

import sys
import os
import argparse
from typing import List, Dict
import time

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scheduler import ConflictFreeScheduler, Activity
from utils.file_parser import FileParser
from utils.pdf_generator import PDFGenerator, AcademicPDFGenerator

# Import algorithms directly for the run-all feature
from algorithms.graph_coloring import GraphColoringScheduler
from algorithms.dynamic_programming import DynamicProgrammingScheduler
from algorithms.backtracking import BacktrackingScheduler
from algorithms.genetic_algorithm import GeneticAlgorithmScheduler, GAConfig


def print_banner():
    """Print application banner"""
    print("=" * 50)
    print("=== Conflict-Free Class Scheduling System ===")
    print("CSE Department Academic Scheduling Solution")
    print("=" * 50)


def print_algorithm_info():
    """Print information about the four core algorithms"""
    print("\n🎓 4 Core Algorithms:")
    print("  1. Graph Coloring    - Models conflicts as graph edges, assigns time slots as colors")
    print("  2. Dynamic Programming - Optimal weighted activity selection with memoization")
    print("  3. Backtracking      - Exhaustive search with pruning for optimal solutions")
    print("  4. Genetic Algorithm - Population-based evolutionary optimization")


def run_single_algorithm(algorithm: str, activities: List[Activity]) -> List[Activity]:
    """
    Run a single algorithm on the activities
    
    Args:
        algorithm: Algorithm name
        activities: List of activities to schedule
        
    Returns:
        Scheduled activities
    """
    scheduler = ConflictFreeScheduler()
    
    print(f"\n🔄 Running {algorithm.upper()} algorithm...")
    start_time = time.time()
    
    if algorithm == "graph-coloring":
        result = scheduler.graph_coloring_schedule(activities)
    elif algorithm == "dynamic-prog":
        result = scheduler.dp_schedule(activities)
    elif algorithm == "backtracking":
        result = scheduler.backtracking_schedule(activities)
    elif algorithm == "genetic":
        result = scheduler.genetic_algorithm_schedule(activities)
    else:
        print(f"❌ Unknown algorithm: {algorithm}")
        return []
    
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    print(f"✅ {algorithm.upper()} completed in {execution_time:.2f}ms")
    print(f"📊 Scheduled {len(result)} activities with total weight {scheduler.calculate_total_weight(result):.2f}")
    
    return result


def run_all_algorithms(activities: List[Activity]) -> Dict[str, List[Activity]]:
    """
    Run all four algorithms and compare results
    
    Args:
        activities: List of activities to schedule
        
    Returns:
        Dictionary with results from all algorithms
    """
    algorithms = ["graph-coloring", "dynamic-prog", "backtracking", "genetic"]
    results = {}
    
    print("\n🚀 Running all 4 algorithms for comparison...")
    print("-" * 60)
    
    for algorithm in algorithms:
        results[algorithm] = run_single_algorithm(algorithm, activities)
    
    # Print comparison
    print("\n📈 ALGORITHM COMPARISON")
    print("-" * 60)
    print(f"{'Algorithm':<20} {'Activities':<12} {'Total Weight':<15} {'Efficiency':<12}")
    print("-" * 60)
    
    for algorithm, result in results.items():
        scheduler = ConflictFreeScheduler()
        total_weight = scheduler.calculate_total_weight(result)
        efficiency = len(result) / len(activities) * 100 if activities else 0
        
        print(f"{algorithm:<20} {len(result):<12} {total_weight:<15.2f} {efficiency:<12.1f}%")
    
    return results


def get_user_input() -> Dict:
    """
    Get user input for scheduling parameters
    
    Returns:
        Dictionary with user input values
    """
    print("\n📝 Please provide scheduling parameters:")
    
    # Ask for algorithm preference
    print("\nSelect scheduling algorithm:")
    print("1. Graph Coloring (default)")
    print("2. Dynamic Programming")
    print("3. Backtracking")
    print("4. Genetic Algorithm")
    print("5. Run All Algorithms")
    
    algorithm_choice = input("\nEnter your choice (1-5) [1]: ").strip() or "1"
    
    algorithm_map = {
        "1": "graph-coloring",
        "2": "dynamic-prog",
        "3": "backtracking",
        "4": "genetic",
        "5": "run-all"
    }
    
    algorithm = algorithm_map.get(algorithm_choice, "graph-coloring")
    
    # Ask for input file
    use_custom_input = input("\nUse custom input file? (y/n) [n]: ").lower().strip() == "y"
    input_file = None
    
    if use_custom_input:
        input_file = input("Enter path to input file (CSV/JSON): ").strip()
        
        # Validate file exists
        if not os.path.exists(input_file):
            print(f"❌ File not found: {input_file}")
            print("Using default sample data instead.")
            input_file = None
    
    # Ask for batch information
    use_batch = input("\nSpecify academic batch information? (y/n) [n]: ").lower().strip() == "y"
    batch = None
    section = "A"
    
    if use_batch:
        batch = input("Enter batch code (e.g., BCSE24) [BCSE24]: ").strip() or "BCSE24"
        section = input("Enter section (A/B) [A]: ").strip().upper() or "A"
        section = "A" if section not in ["A", "B"] else section
    
    # PDF output type
    pdf_type = input("\nSelect PDF type (academic/basic) [academic]: ").lower().strip() or "academic"
    use_basic_pdf = pdf_type == "basic"
    
    # Use database
    use_database = input("\nUse database for input? (y/n) [n]: ").lower().strip() == "y"
    
    if use_database:
        init_db = input("Initialize database with sample data? (y/n) [y]: ").lower().strip() != "n"
    else:
        init_db = False
    
    # Return user selections as dictionary
    return {
        "algorithm": algorithm,
        "run_all": algorithm == "run-all",
        "input_file": input_file,
        "batch": batch,
        "section": section,
        "use_basic_pdf": use_basic_pdf,
        "use_database": use_database,
        "init_db": init_db
    }


def create_args_from_user_input(user_input: Dict) -> argparse.Namespace:
    """
    Create argparse.Namespace object from user input
    
    Args:
        user_input: Dictionary with user input values
        
    Returns:
        argparse.Namespace object
    """
    # Create a minimal Namespace object with default values
    args = argparse.Namespace(
        algorithm=user_input.get("algorithm", "graph-coloring"),
        run_all=user_input.get("run_all", False),
        input=user_input.get("input_file"),
        output=None,
        pdf=user_input.get("use_basic_pdf", False),
        academic_pdf=not user_input.get("use_basic_pdf", False),
        batch=user_input.get("batch"),
        section=user_input.get("section", "A"),
        semester="Spring 2025",
        use_database=user_input.get("use_database", False),
        init_db=user_input.get("init_db", False),
        no_database=not user_input.get("use_database", False),
        visualize=False,
        enhanced_generator=False,
        comprehensive_routine=False,
        university_schedule=False
    )
    
    return args


def load_activities(args) -> List[Activity]:
    """
    Load activities from various sources
    
    Args:
        args: Command line arguments
        
    Returns:
        List of activities
    """
    activities = []
    
    if args.use_database:
        try:
            # Import the DatabaseManager using the full path
            from src.database.database_manager import DatabaseManager
            
            db = DatabaseManager()
            
            if args.init_db:
                print("🔄 Initializing database with sample data...")
                if db.initialize_with_sample_data():
                    print("✅ Database initialized successfully")
                else:
                    print("❌ Database initialization failed")
                    return activities
            else:
                if not db.connect():
                    print("❌ Database connection failed")
                    return activities
            
            if args.batch:
                activities = db.get_courses_by_batch(args.batch)
            else:
                activities = db.get_all_courses()
            
            print(f"📊 Loaded {len(activities)} activities from database")
            
        except ImportError:
            print("❌ Database modules not available. Install SQLAlchemy and PyMySQL:")
            print("   pip install sqlalchemy pymysql")
            return activities
        except Exception as e:
            print(f"❌ Database error: {e}")
            return activities
    
    elif args.input:
        # Load from file
        if args.input.endswith('.csv'):
            activities = FileParser.parse_csv(args.input)
        elif args.input.endswith('.json'):
            activities = FileParser.parse_json(args.input)
        else:
            activities = FileParser.parse_text(args.input)
    
    else:
        # Generate sample data
        print("📝 Generating sample activities...")
        sample_file = "data/sample_activities.csv"
        if FileParser.generate_sample_data(sample_file, 10):
            activities = FileParser.parse_csv(sample_file)
        else:
            # Fallback: create minimal sample data
            activities = [
                Activity(1, 0, 90, 3.0, "Programming Fundamentals", "CSE-101"),
                Activity(2, 100, 190, 3.0, "Data Structures", "CSE-102"),
                Activity(3, 50, 140, 1.0, "Programming Lab", "LAB-1"),
                Activity(4, 200, 290, 3.0, "Algorithms", "CSE-101"),
                Activity(5, 150, 210, 1.5, "Database Lab", "LAB-2"),
            ]
            print("📊 Using fallback sample data")
    
    return activities


def main():
    """Main application function"""
    print_banner()
    
    # Check if any command line arguments were provided
    if len(sys.argv) > 1:
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description="Conflict-Free Class Scheduling System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py                          (Interactively asks for input)
  python main.py --algorithm graph-coloring
  python main.py --run-all --visualize
  python main.py --init-db
  python main.py --input data/courses.csv --pdf    (Generate basic PDF instead of academic)
            """
        )
        
        # Algorithm selection
        parser.add_argument('--algorithm', choices=['graph-coloring', 'dynamic-prog', 'backtracking', 'genetic'],
                        default='graph-coloring', help='Algorithm to use')
        parser.add_argument('--run-all', action='store_true', help='Run all 4 algorithms and compare results')
        
        # Input/Output options
        parser.add_argument('--input', help='Input file with activities data')
        parser.add_argument('--output', help='Output file for results')
        
        # PDF Generation
        parser.add_argument('--pdf', action='store_true', help='Generate basic PDF output instead of academic PDF')
        parser.add_argument('--academic-pdf', action='store_true', help='Generate professional academic schedule PDF (default behavior)')
        
        # Academic options
        parser.add_argument('--batch', help='Specify batch code (e.g., BCSE23)')
        parser.add_argument('--section', default='A', help='Specify section name (A or B)')
        parser.add_argument('--semester', default='Spring 2025', help='Semester information')
        
        # Database options
        parser.add_argument('--use-database', action='store_true', help='Use database for input')
        parser.add_argument('--init-db', action='store_true', help='Initialize/reset database with sample data')
        parser.add_argument('--no-database', action='store_true', help='Disable database integration')
        
        # Other options
        parser.add_argument('--visualize', action='store_true', help='Enable visualization output')
        parser.add_argument('--enhanced-generator', action='store_true', help='Use enhanced routine generator')
        parser.add_argument('--comprehensive-routine', action='store_true', help='Generate comprehensive routine')
        parser.add_argument('--university-schedule', action='store_true', help='Generate complete university schedule')
        
        args = parser.parse_args()
    else:
        # No command line arguments provided, use interactive mode
        print("\n🖥️ Interactive Mode: No command line arguments provided.")
        user_input = get_user_input()
        args = create_args_from_user_input(user_input)
        print("\n✅ Using user-provided parameters for scheduling.")
    
    # Handle special flags
    if args.enhanced_generator or args.comprehensive_routine or args.university_schedule:
        args.use_database = True
    
    if args.no_database:
        args.use_database = False
    
    if args.init_db:
        args.use_database = True
    
    # Show algorithm information
    print_algorithm_info()
    
    # Load activities
    print("\n📂 Loading activities...")
    activities = load_activities(args)
    
    if not activities:
        print("❌ No activities loaded. Exiting.")
        return 1
    
    print(f"✅ Loaded {len(activities)} activities")
    
    # Process activities
    if args.run_all:
        results = run_all_algorithms(activities)
        
        # Generate output for the best result (highest weight)
        scheduler = ConflictFreeScheduler()
        best_algorithm = max(results.keys(), 
                           key=lambda k: scheduler.calculate_total_weight(results[k]))
        best_result = results[best_algorithm]
        
        print(f"\n🏆 Best result: {best_algorithm.upper()}")
        
        # Always generate PDF output by default (academic PDF is the preferred format)
        if args.pdf:  # Basic PDF was explicitly requested
            pdf_gen = PDFGenerator()
            output_path = pdf_gen.generate_schedule_html(best_result, f"Schedule - {best_algorithm.upper()}")
            print(f"\n✅ Basic PDF schedule generated: {output_path}")
        else:  # Academic PDF is the default in all cases
            pdf_gen = AcademicPDFGenerator()
            batch_code = args.batch if args.batch else "BCSE24"
            output_path = pdf_gen.generate_academic_schedule(best_result, batch_code, args.section, args.semester)
            print(f"\n✅ Academic PDF schedule generated: {output_path}")
    
    else:
        # Run single algorithm
        result = run_single_algorithm(args.algorithm, activities)
        
        if result:
            # Print schedule
            scheduler = ConflictFreeScheduler()
            scheduler.print_schedule(result)
            
            # Always generate PDF output by default (academic PDF is the preferred format)
            if args.pdf:  # Basic PDF was explicitly requested
                pdf_gen = PDFGenerator()
                output_path = pdf_gen.generate_schedule_html(result, f"Schedule - {args.algorithm.upper()}")
                print(f"\n✅ Basic PDF schedule generated: {output_path}")
            else:  # Academic PDF is the default in all cases
                pdf_gen = AcademicPDFGenerator()
                batch_code = args.batch if args.batch else "BCSE24"
                output_path = pdf_gen.generate_academic_schedule(result, batch_code, args.section, args.semester)
                print(f"\n✅ Academic PDF schedule generated: {output_path}")
            
            # Save to file if requested
            if args.output:
                if args.output.endswith('.csv'):
                    FileParser.write_csv(result, args.output)
                elif args.output.endswith('.json'):
                    FileParser.write_json(result, args.output)
    
    print("\n✅ Scheduling complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
