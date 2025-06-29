#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Conflict-Free Class Scheduling System
==============================================

A comprehensive academic scheduling system that automatically generates 
conflict-free course schedules using multiple optimization algorithms.

Features:
- Multiple scheduling algorithms (Graph Coloring, Dynamic Programming, Backtracking, Genetic)
- Database integration with MySQL
- Enhanced PDF generation with eye-catching designs
- Faculty input system with automatic room allocation
- Comprehensive, batch-wise, and section-wise routine generation
- Interactive command-line interface

Author: Punam
Version: 2.0 (Enhanced)
"""

import sys
import os
import argparse
import time
import json
from datetime import datetime
from typing import List, Dict, Optional

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scheduler import ConflictFreeScheduler, Activity
from utils.file_parser import FileParser
from utils.pdf_generator import PDFGenerator, AcademicPDFGenerator
from utils.enhanced_pdf_generator import EnhancedPDFGenerator
from utils.comprehensive_routine_generator import ComprehensiveRoutineGenerator
from utils.reference_pdf_generator import ReferencePDFRoutineGenerator
from utils.faculty_input import FacultyInputSystem
from utils.sample_routine_generator import SampleRoutineGenerator
# Database import is conditional - only when needed

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


def ensure_activity_attributes(activity: Activity) -> Activity:
    """
    Ensure activity has all required attributes for enhanced PDF generation
    
    Args:
        activity: Activity object to check
        
    Returns:
        Activity with all required attributes
    """
    if not hasattr(activity, 'faculty'):
        activity.faculty = "TBA"
    if not hasattr(activity, 'course_code'):
        activity.course_code = f"CSE{activity.id:03d}"
    
    # Ensure attributes are not None
    if activity.faculty is None:
        activity.faculty = "TBA"
    if activity.course_code is None:
        activity.course_code = f"CSE{activity.id:03d}"
        
    return activity


def ensure_activities_attributes(activities: List[Activity]) -> List[Activity]:
    """
    Ensure all activities have required attributes
    
    Args:
        activities: List of activities
        
    Returns:
        List of activities with all required attributes
    """
    return [ensure_activity_attributes(activity) for activity in activities]


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
    
    # Ask for routine type
    print("\nSelect routine generation type:")
    print("1. Section-wise routine (specific batch and section)")
    print("2. Batch-wise routine (all sections of a batch)")
    print("3. Comprehensive routine (all batches and sections)")
    print("4. Faculty input routine (custom faculty scheduling)")
    print("5. Reference-based routine (matches reference PDF format)")
    print("6. Sample-based routine (enhanced UI with faculty preferences)")
    
    routine_choice = input("\nEnter your choice (1-6) [1]: ").strip() or "1"
    
    routine_types = {
        "1": "section",
        "2": "batch", 
        "3": "comprehensive",
        "4": "faculty",
        "5": "reference",
        "6": "sample"
    }
    
    routine_type = routine_types.get(routine_choice, "section")
    
    # Ask for algorithm preference
    print("\nSelect scheduling algorithm:")
    print("1. Graph Coloring (default)")
    print("2. Dynamic Programming")
    print("3. Backtracking")
    print("4. Genetic Algorithm")
    print("5. Run All Algorithms")
    print("6. Preserve Realistic Schedule (No Optimization)")
    
    algorithm_choice = input("\nEnter your choice (1-6) [1]: ").strip() or "1"
    
    algorithm_map = {
        "1": "graph-coloring",
        "2": "dynamic-prog",
        "3": "backtracking",
        "4": "genetic",
        "5": "run-all",
        "6": "preserve"
    }
    
    algorithm = algorithm_map.get(algorithm_choice, "graph-coloring")
    
    # Ask for input file (unless faculty mode)
    use_custom_input = False
    input_file = None
    
    if routine_type != "faculty":
        use_custom_input = input("\nUse custom input file? (y/n) [n]: ").lower().strip() == "y"
        
        if use_custom_input:
            input_file = input("Enter path to input file (CSV/JSON): ").strip()
            
            # Validate file exists
            if not os.path.exists(input_file):
                print(f"❌ File not found: {input_file}")
                print("Using default sample data instead.")
                input_file = None
    
    # Ask for batch information (except for comprehensive mode)
    batch = None
    section = "A"
    
    if routine_type in ["section", "batch"]:
        batch = input("\nEnter batch code (e.g., BCSE24) [BCSE24]: ").strip() or "BCSE24"
        
        if routine_type == "section":
            section = input("Enter section (A/B) [A]: ").strip().upper() or "A"
            section = "A" if section not in ["A", "B"] else section
    
    # PDF output type
    pdf_type = input("\nSelect PDF type (academic/basic) [academic]: ").lower().strip() or "academic"
    use_basic_pdf = pdf_type == "basic"
    
    # Use database (auto-enable for comprehensive and faculty modes, skip for reference and sample)
    if routine_type in ["reference", "sample"]:
        use_database = False
        print(f"\n📋 {routine_type.title()} mode uses predefined data - database skipped")
    elif routine_type in ["comprehensive", "faculty"]:
        use_database = True
        print(f"\n🔄 Database mode automatically enabled for {routine_type} routine")
    else:
        use_database = input("\nUse database for input? (y/n) [n]: ").lower().strip() == "y"
    
    if use_database:
        init_db = input("Initialize database with realistic CSE department data? (y/n) [y]: ").lower().strip() != "n"
    else:
        init_db = False
    
    # Return user selections as dictionary
    return {
        "routine_type": routine_type,
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
        basic_pdf=user_input.get("use_basic_pdf", False),
        enhanced=not user_input.get("use_basic_pdf", False),
        routine_type=user_input.get("routine_type", "section"),
        comprehensive=user_input.get("routine_type") == "comprehensive",
        batch_wise=user_input.get("routine_type") == "batch",
        faculty_input=user_input.get("routine_type") == "faculty",
        batch=user_input.get("batch"),
        section=user_input.get("section", "A"),
        semester="Spring 2025",
        use_database=user_input.get("use_database", False),
        init_db=user_input.get("init_db", False),
        no_database=not user_input.get("use_database", False),
        visualize=False
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
                print("🔄 Initializing database with realistic CSE department data...")
                if db.initialize_with_realistic_data():
                    print("✅ Realistic database initialized successfully")
                else:
                    print("❌ Database initialization failed")
                    return activities
            else:
                if not db.connect():
                    print("❌ Database connection failed")
                    return activities
            
            if args.batch:
                activities = db.get_realistic_activities_by_batch(args.batch)
            elif hasattr(args, 'routine_type') and args.routine_type == "comprehensive":
                activities = db.get_all_realistic_activities()
            elif hasattr(args, 'algorithm') and args.algorithm == "preserve":
                # For preserve mode, always use realistic activities
                activities = db.get_all_realistic_activities()
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


def preserve_realistic_schedule(activities: List[Activity]) -> List[Activity]:
    """
    Preserve the realistic schedule without running optimization algorithms
    
    Args:
        activities: List of activities with realistic timing
        
    Returns:
        Activities with preserved realistic schedule
    """
    print("🔄 Using realistic schedule (no algorithm optimization)")
    print("📊 Preserving original realistic timing and assignments")
    
    # The activities already have realistic timing, faculty, and room assignments
    # No need to run scheduling algorithms
    return activities


def handle_faculty_input_routine() -> List[Activity]:
    """
    Handle faculty input routine generation with both interactive and non-interactive modes
    
    Returns:
        List of activities generated from faculty input
    """
    print("\n" + "="*60)
    print("🎓 FACULTY INPUT SYSTEM")
    print("="*60)
    
    faculty_system = FacultyInputSystem()
    
    # Check if existing faculty data exists
    faculty_data_path = "data/faculty_data.json"
    faculty_test_path = "data/faculty_input_test.json"
    
    # Try to load existing faculty data
    data_loaded = False
    
    if os.path.exists(faculty_data_path):
        try:
            with open(faculty_data_path, 'r') as f:
                content = f.read().strip()
                if content and content != "{}":  # Check if file has meaningful content
                    if faculty_system.load_faculty_data():
                        print("✅ Existing faculty data loaded from faculty_data.json")
                        data_loaded = True
                    else:
                        print("⚠️ Failed to load faculty_data.json")
        except Exception as e:
            print(f"⚠️ Error reading faculty_data.json: {e}")
    
    # If no valid data found, try test data
    if not data_loaded and os.path.exists(faculty_test_path):
        try:
            if faculty_system.load_faculty_data(faculty_test_path):
                print("✅ Loaded test faculty data from faculty_input_test.json")
                data_loaded = True
        except Exception as e:
            print(f"⚠️ Error reading faculty_input_test.json: {e}")
    
    # If still no data, check if we should run interactively
    if not data_loaded:
        print("\n� No existing faculty data found.")
        
        # Check if we're in a truly interactive environment
        try:
            import sys
            if sys.stdin.isatty():
                # Interactive mode - ask user
                use_interactive = input("Would you like to input faculty data interactively? (y/n) [n]: ").lower().strip() == 'y'
                if use_interactive:
                    return handle_interactive_faculty_input(faculty_system)
            
            # Non-interactive or user chose not to use interactive mode
            print("🔄 Using default faculty schedule generation...")
            return create_default_faculty_schedule()
            
        except (EOFError, KeyboardInterrupt):
            print("\n🔄 Non-interactive mode detected. Using default faculty schedule...")
            return create_default_faculty_schedule()
    
    # Data was loaded successfully
    print(f"📊 Loaded {len(faculty_system.faculties)} faculty members and {len(faculty_system.courses)} courses")
    
    # Check if we should run interactive mode for modifications
    try:
        import sys
        if sys.stdin.isatty() and len(faculty_system.courses) == 0:
            # Interactive mode and no courses assigned
            modify_data = input("\nNo courses assigned. Would you like to add courses interactively? (y/n) [n]: ").lower().strip() == 'y'
            if modify_data:
                return handle_interactive_faculty_input(faculty_system)
    except (EOFError, KeyboardInterrupt):
        pass
    
    # Convert faculty courses to Activity objects
    activities = []
    for course in faculty_system.courses:
        activity = Activity(
            id=len(activities) + 1,
            start=course['start_time'],
            end=course['end_time'],
            weight=course['credits'],
            name=course['course_name'],
            room=course['room']
        )
        # Add faculty and course code information
        activity.faculty = course['faculty_name']
        activity.course_code = course['course_code']
        activities.append(activity)
    
    print(f"✅ Generated {len(activities)} activities from faculty input system")
    return activities


def handle_interactive_faculty_input(faculty_system: 'FacultyInputSystem') -> List[Activity]:
    """
    Handle interactive faculty input
    
    Args:
        faculty_system: FacultyInputSystem instance
        
    Returns:
        List of activities from interactive input
    """
    # Main faculty input loop
    while True:
        print("\n" + "-"*40)
        print("Faculty Input Options:")
        print("1. Add Faculty Member")
        print("2. Assign Courses to Faculty")
        print("3. View Current Schedule")
        print("4. Generate Routine")
        print("5. Save and Exit")
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                faculty_system.add_faculty_interactive()
            elif choice == "2":
                faculty_system.interactive_course_assignment()
            elif choice == "3":
                faculty_system.print_schedule_summary()
            elif choice == "4":
                break
            elif choice == "5":
                faculty_system.save_faculty_data()
                print("👋 Faculty data saved. Generating routine...")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except (EOFError, KeyboardInterrupt):
            print("\n🔄 Interactive mode interrupted. Using current data...")
            break
    
    # Convert faculty courses to Activity objects
    activities = []
    for course in faculty_system.courses:
        activity = Activity(
            id=len(activities) + 1,
            start=course['start_time'],
            end=course['end_time'],
            weight=course['credits'],
            name=course['course_name'],
            room=course['room']
        )
        # Add faculty and course code information
        activity.faculty = course['faculty_name']
        activity.course_code = course['course_code']
        activities.append(activity)
    
    return activities


def create_default_faculty_schedule() -> List[Activity]:
    """
    Create a default faculty schedule when no input data is available
    
    Returns:
        List of default activities
    """
    print("📋 Creating default faculty schedule...")
    
    # Create some sample faculty schedule
    default_activities = [
        Activity(1, 480, 570, 3.0, "Software Engineering", "302"),      # 08:00-09:30
        Activity(2, 590, 680, 3.0, "Database Systems", "303"),          # 09:50-11:20
        Activity(3, 700, 790, 3.0, "Computer Networks", "304"),         # 11:40-13:10
        Activity(4, 840, 930, 3.0, "Operating Systems", "504"),         # 14:00-15:30
        Activity(5, 950, 1040, 3.0, "Machine Learning", "1003"),        # 15:50-17:20
    ]
    
    # Add faculty and course code information
    faculties = ["Dr. Ahmed Rahman", "Prof. Fatema Khatun", "Dr. Mohammad Ali", "Ms. Rashida Begum", "Mr. Karim Hassan"]
    course_codes = ["CSE4401", "CSE3401", "CSE3301", "CSE3201", "CSE4501"]
    
    for i, activity in enumerate(default_activities):
        activity.faculty = faculties[i % len(faculties)]
        activity.course_code = course_codes[i % len(course_codes)]
    
    print(f"✅ Generated {len(default_activities)} default activities")
    return default_activities


def handle_comprehensive_routine(activities: List[Activity]) -> str:
    """
    Handle comprehensive routine generation for all batches with conflict-free scheduling
    
    Args:
        activities: List of all activities
        
    Returns:
        Path to generated routine
    """
    print("\n🔄 Generating comprehensive conflict-free routine for all batches...")
    
    try:
        # Load sample routine data from JSON (all batches and sections)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, "data", "sample_routine_data.json")
        
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            return None
            
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Use the SampleRoutineGenerator for comprehensive routine
        # This ensures the table format matches the sample routine exactly:
        # - Rows organized by days and rooms
        # - Columns organized by time slots
        # - Each cell containing batch, section, course code, and faculty information
        print("🌟 Using sample routine template for departmental-wide schedule")
        
        try:
            # Import and use SampleRoutineGenerator
            from src.utils.sample_routine_generator import SampleRoutineGenerator
            sample_generator = SampleRoutineGenerator()
            
            # Generate comprehensive routine using the loaded data
            output_dir = os.path.join(script_dir, "output")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create timestamp for unique output file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_output = os.path.join(output_dir, f"comprehensive_departmental_routine_{timestamp}")
            
            # Generate both PDF and HTML formats in sample routine style
            # This will create a table with batch, section, course code, faculty name in a single cell
            html_file = sample_generator.create_enhanced_html_routine(data_file, f"{base_output}.html")
            pdf_file = sample_generator.generate_enhanced_pdf(data_file, f"{base_output}.pdf")
            
            if pdf_file or html_file:
                if pdf_file:
                    print(f"✅ Comprehensive departmental routine generated (PDF): {pdf_file}")
                if html_file:
                    print(f"🌐 Comprehensive departmental routine generated (HTML): {html_file}")
                
                # Open the HTML file in the browser for the user to see
                print("\n🌐 Opening comprehensive routine in browser...")
                if html_file and os.path.exists(html_file):
                    try:
                        import webbrowser
                        webbrowser.open(f"file://{os.path.abspath(html_file)}")
                    except Exception as e:
                        print(f"⚠️ Could not open browser automatically: {e}")
                
                return html_file or pdf_file
        
        except (ImportError, AttributeError) as e:
            print(f"⚠️ Could not use SampleRoutineGenerator: {e}")
            
        # Fall back to Sample Routine Helper
        try:
            print("🔄 Trying alternative sample routine generator...")
            from src.utils.sample_routine_generator import SampleRoutineGenerator
            sample_generator = SampleRoutineGenerator()
            
            output_dir = os.path.join(script_dir, "output")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_output = os.path.join(output_dir, f"comprehensive_departmental_routine_{timestamp}")
            
            html_file, pdf_file = sample_generator.generate_all_formats(data_file, base_output)
            
            if pdf_file or html_file:
                print(f"✅ Comprehensive departmental routine generated successfully!")
                return html_file or pdf_file
        except Exception as e:
            print(f"⚠️ Alternative generator also failed: {e}")
        
        # Last resort: Use the ComprehensiveRoutineGenerator with specific modifications
        # to match the sample routine format
        print("🔄 Using fallback comprehensive routine generator with sample format...")
        generator = ComprehensiveRoutineGenerator()
        
        # Override the template to match the sample routine format
        generator.use_sample_format = True  # This flag should be checked in the generator class
        
        output_file_base = os.path.join(output_dir, "comprehensive_routine_spring_2025")
        
        # Generate both formats (PDF first, then HTML)
        pdf_file = generator.generate_comprehensive_routine_pdf(data_file, f"{output_file_base}.pdf")
        html_file = generator.generate_html_routine(data_file, f"{output_file_base}.html")
        
        if pdf_file or html_file:
            print(f"✅ Comprehensive departmental routine generated (fallback): {pdf_file or html_file}")
            return pdf_file or html_file
        else:
            print("❌ Failed to generate comprehensive routine with all methods")
            return None
    except Exception as e:
        print(f"❌ Error generating comprehensive routine: {str(e)}")
        return None
            
    except Exception as e:
        print(f"❌ Error generating comprehensive routine: {e}")
        # Fallback to simple comprehensive routine
        print("🔄 Falling back to enhanced comprehensive routine...")
        
        pdf_gen = EnhancedPDFGenerator()
        return pdf_gen.generate_comprehensive_routine({
            "All Departments": activities
        })


def handle_batch_routine(activities: List[Activity], batch_code: str) -> str:
    """
    Handle batch-wise routine generation
    
    Args:
        activities: List of activities for the batch
        batch_code: Batch code
        
    Returns:
        Path to generated routine
    """
    print(f"\n🔄 Generating routine for batch {batch_code}...")
    
    pdf_gen = EnhancedPDFGenerator()
    return pdf_gen.generate_batch_routine(activities, batch_code)


def handle_section_routine(activities: List[Activity], batch_code: str, section: str) -> str:
    """
    Handle section-wise routine generation
    
    Args:
        activities: List of activities for the section
        batch_code: Batch code
        section: Section name
        
    Returns:
        Path to generated routine
    """
    print(f"\n🔄 Generating routine for {batch_code} Section {section}...")
    
    pdf_gen = EnhancedPDFGenerator()
    
    # Add sample faculty information to activities if not present
    faculties = ["Dr. Ahmed Rahman", "Prof. Fatema Khatun", "Dr. Mohammad Ali", "Ms. Rashida Begum", "Mr. Karim Hassan"]
    for i, activity in enumerate(activities):
        if not hasattr(activity, 'faculty') or not activity.faculty:
            activity.faculty = faculties[i % len(faculties)]
        if not hasattr(activity, 'course_code') or not activity.course_code:
            activity.course_code = f"CSE{activity.id + 100:03d}"
    
    return pdf_gen.generate_section_routine(activities, batch_code, section)


def handle_reference_based_routine() -> str:
    """
    Handle reference-based routine generation using predefined data
    that matches the reference PDF format exactly
    
    Returns:
        Path to generated routine
    """
    print("\n🔄 Generating reference-based comprehensive routine...")
    print("📋 Using predefined course data with available rooms: 302, 303, 304, 504, 1003")
    
    generator = ReferencePDFRoutineGenerator()
    
    # Get project root and data file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "data", "reference_based_routine_data.json")
    output_dir = os.path.join(script_dir, "output")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    base_output = os.path.join(output_dir, "reference_based_comprehensive_routine")
    
    try:
        html_file, pdf_file = generator.generate_all_formats(data_file, base_output)
        
        if html_file and pdf_file:
            print(f"✅ Reference-based routine generated successfully!")
            print(f"🌐 HTML: {html_file}")
            print(f"📄 PDF: {pdf_file}")
            return pdf_file
        else:
            print("❌ Failed to generate reference-based routine")
            return ""
    except Exception as e:
        print(f"❌ Error generating reference-based routine: {e}")
        return ""


def handle_sample_based_routine() -> str:
    """
    Handle sample-based routine generation using enhanced UI and faculty preferences
    
    Returns:
        Path to generated routine
    """
    print("\n🔄 Generating sample-based comprehensive routine...")
    print("📋 Using enhanced UI design with faculty preferences and optimized scheduling")
    print("🎯 Ensuring minimal gaps between classes for students")
    
    generator = SampleRoutineGenerator()
    
    # Get project root and data file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "data", "sample_routine_data.json")
    output_dir = os.path.join(script_dir, "output")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    base_output = os.path.join(output_dir, "enhanced_sample_routine")
    
    try:
        html_file, pdf_file = generator.generate_all_formats(data_file, base_output)
        
        if html_file and pdf_file:
            print(f"✅ Sample-based routine generated successfully!")
            print(f"🌐 HTML: {html_file}")
            print(f"📄 PDF: {pdf_file}")
            return pdf_file
        else:
            print("❌ Failed to generate sample-based routine")
            return ""
    except Exception as e:
        print(f"❌ Error generating sample-based routine: {e}")
        return ""


def process_enhanced_routine(user_input: Dict, activities: List[Activity]) -> str:
    """
    Process enhanced routine generation based on user input
    
    Args:
        user_input: User input dictionary
        activities: List of activities
        
    Returns:
        Path to generated routine
    """
    routine_type = user_input.get("routine_type", "section")
    batch = user_input.get("batch", "BCSE24")
    section = user_input.get("section", "A")
    
    if routine_type == "faculty":
        # Import the updated faculty handler
        try:
            from src.utils.routine_handler import handle_faculty_input_routine
        except ImportError:
            # Fallback to local implementation if import fails
            pass
            
        # Faculty input mode - get activities from faculty system
        faculty_activities = handle_faculty_input_routine()
        
        if not faculty_activities:
            print("❌ No courses assigned through faculty input system")
            return None
            
        # Create an enhanced PDF with faculty-specific schedule
        print("\n🎓 Generating faculty-specific routine...")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"faculty_routine_{timestamp}")
        
        # Use enhanced PDF generator for faculty routine
        pdf_gen = EnhancedPDFGenerator()
        # Set custom output directory for faculty schedule
        pdf_gen.output_dir = os.path.dirname(output_file)
        result = pdf_gen.generate_section_routine(
            faculty_activities,
            "Faculty",
            "Input",
            semester="Spring 2025"
        )
        
        if result:
            print(f"✅ Faculty input routine generated successfully: {result}")
            return result
        else:
            print("❌ Failed to generate faculty input routine")
            return None
    
    # Handle comprehensive routine with improved implementation
    if routine_type == "comprehensive":
        # Import the updated comprehensive handler
        try:
            from src.utils.routine_handler import handle_comprehensive_routine
        except ImportError:
            # Fallback to local implementation if import fails
            pass
        return handle_comprehensive_routine(activities)
    elif routine_type == "batch":
        return handle_batch_routine(activities, batch)
    elif routine_type == "section":
        return handle_section_routine(activities, batch, section)
    elif routine_type == "reference":
        return handle_reference_based_routine()
    elif routine_type == "sample":
        return handle_sample_based_routine()
    else:
        print(f"❌ Unknown routine type: {routine_type}")
        return None


def print_realistic_schedule(activities: List[Activity]):
    """
    Print a realistic schedule with day and time information
    
    Args:
        activities: List of scheduled activities
    """
    if not activities:
        print("❌ No activities to display")
        return
    
    print("\n" + "="*100)
    print("📅 REALISTIC CLASS SCHEDULE")
    print("="*100)
    
    # Check if activities have original day/time information
    has_day_info = any(hasattr(activity, 'day') and hasattr(activity, 'time_slot') for activity in activities)
    
    if has_day_info:
        # Display with original day/time information
        days_schedule = {}
        for activity in activities:
            day = getattr(activity, 'day', 'Unknown')
            if day not in days_schedule:
                days_schedule[day] = []
            days_schedule[day].append(activity)
        
        # Sort days in order
        day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        
        for day in day_order:
            if day in days_schedule:
                print(f"\n📅 {day.upper()}")
                print("-" * 90)
                
                # Sort activities by start time
                day_activities = sorted(days_schedule[day], key=lambda x: x.start)
                
                for activity in day_activities:
                    time_slot = getattr(activity, 'time_slot', f"{activity.start//60:02d}:{activity.start%60:02d}-{activity.end//60:02d}:{activity.end%60:02d}")
                    print(f"  {time_slot:<12} | {activity.course_code:<8} | {activity.name:<30} | {activity.faculty:<20} | Room: {activity.room}")
    else:
        # Display with scheduled times (fallback)
        print("\n📋 SCHEDULED ACTIVITIES")
        print("-" * 90)
        print(f"{'Time':<12} | {'Code':<8} | {'Course Name':<30} | {'Faculty':<20} | {'Room':<8}")
        print("-" * 90)
        
        # Sort activities by start time
        sorted_activities = sorted(activities, key=lambda x: x.start)
        
        for activity in sorted_activities:
            # Convert minutes to hours:minutes format
            start_hour = activity.start // 60
            start_min = activity.start % 60
            end_hour = activity.end // 60
            end_min = activity.end % 60
            time_display = f"{start_hour:02d}:{start_min:02d}-{end_hour:02d}:{end_min:02d}"
            
            print(f"  {time_display:<12} | {activity.course_code:<8} | {activity.name:<30} | {activity.faculty:<20} | {activity.room:<8}")
    
    print("\n" + "="*100)
    print(f"📊 Total Classes: {len(activities)}")
    print(f"📊 Total Credit Hours: {sum(activity.weight for activity in activities):.1f}")
    print("="*100)


def main():
    """Main application function"""
    print_banner()
    
    # Check if any command line arguments were provided
    if len(sys.argv) > 1:
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description="Enhanced Conflict-Free Class Scheduling System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py                              (Interactive mode - enhanced features)
  python main.py --algorithm graph-coloring
  python main.py --run-all --enhanced
  python main.py --init-db
  python main.py --comprehensive --enhanced  (Generate comprehensive routine)
  python main.py --academic-routine          (Generate academic routine with proper time slots)
  python main.py --input data/courses.csv --basic-pdf
            """
        )
        
        # Algorithm selection
        parser.add_argument('--algorithm', choices=['graph-coloring', 'dynamic-prog', 'backtracking', 'genetic'],
                        default='graph-coloring', help='Algorithm to use')
        parser.add_argument('--run-all', action='store_true', help='Run all 4 algorithms and compare results')
        parser.add_argument('--preserve-schedule', action='store_true', help='Preserve realistic schedule without optimization')
        
        # Input/Output options
        parser.add_argument('--input', help='Input file with activities data')
        parser.add_argument('--output', help='Output file for results')
        
        # PDF Generation
        parser.add_argument('--basic-pdf', action='store_true', help='Generate basic PDF output')
        parser.add_argument('--academic-pdf', action='store_true', help='Generate university-branded academic PDF')
        parser.add_argument('--enhanced', action='store_true', help='Use enhanced PDF generator (default)')
        
        # Routine Type Selection
        parser.add_argument('--comprehensive', action='store_true', help='Generate comprehensive routine for all batches')
        parser.add_argument('--academic-routine', action='store_true', help='Generate comprehensive academic routine with proper time slots')
        parser.add_argument('--batch-wise', action='store_true', help='Generate batch-wise routine')
        parser.add_argument('--faculty-input', action='store_true', help='Use faculty interactive input system')
        
        # Academic options
        parser.add_argument('--batch', help='Specify batch code (e.g., BCSE24)')
        parser.add_argument('--section', default='A', help='Specify section name (A or B)')
        parser.add_argument('--semester', default='Spring 2025', help='Semester information')
        
        # Database options
        parser.add_argument('--use-database', action='store_true', help='Use database for input')
        parser.add_argument('--init-db', action='store_true', help='Initialize/reset database with sample data')
        parser.add_argument('--no-database', action='store_true', help='Disable database integration')
        
        # Other options
        parser.add_argument('--visualize', action='store_true', help='Enable visualization output')
        
        args = parser.parse_args()
        
        # Handle preserve schedule flag
        if args.preserve_schedule:
            args.algorithm = "preserve"
        
        # Set default enhanced mode unless basic PDF or academic PDF is explicitly requested
        if not args.basic_pdf and not args.academic_pdf:
            args.enhanced = True
            
        # Determine routine type based on flags
        if args.comprehensive:
            args.routine_type = "comprehensive"
        elif args.academic_routine:
            args.routine_type = "academic_routine"
        elif args.batch_wise:
            args.routine_type = "batch"
        elif args.faculty_input:
            args.routine_type = "faculty"
        else:
            args.routine_type = "section"
    else:
        # No command line arguments provided, use interactive mode
        print("\n🖥️ Interactive Mode: No command line arguments provided.")
        user_input = get_user_input()
        args = create_args_from_user_input(user_input)
        
        # Set enhanced mode by default unless basic PDF is selected
        if not user_input.get("use_basic_pdf", False):
            args.enhanced = True
            
        print("\n✅ Using user-provided parameters for enhanced scheduling.")
    
    # Handle special flags
    # Enhanced mode doesn't automatically require database - only specific routine types do
    if hasattr(args, 'routine_type') and args.routine_type in ["comprehensive", "faculty"]:
        args.use_database = True
    
    if args.no_database:
        args.use_database = False
    
    if args.init_db:
        args.use_database = True
    
    # Show algorithm information
    print_algorithm_info()
    
    # Handle academic routine generation (new comprehensive routine with proper time slots)
    if hasattr(args, 'routine_type') and args.routine_type == "academic_routine":
        print("\n🎓 Generating comprehensive academic routine with proper time slots...")
        generator = ComprehensiveRoutineGenerator()
        data_file = "data/comprehensive_routine_data.json"
        
        # Generate both PDF and HTML
        pdf_file = generator.generate_comprehensive_routine_pdf(data_file)
        html_file = generator.generate_html_routine(data_file)
        
        if pdf_file and html_file:
            print(f"\n✅ Academic routine generation complete!")
            print(f"📄 PDF: {pdf_file}")
            print(f"🌐 HTML: {html_file}")
            return 0
        else:
            print("❌ Failed to generate academic routine")
            return 1

    # Handle reference and sample modes early (before activity loading)
    if hasattr(args, 'routine_type'):
        if args.routine_type == "reference":
            print("\n📋 Reference-based routine generation selected...")
            result = handle_reference_based_routine()
            if result:
                print(f"\n✅ Reference-based routine generation complete!")
                return 0
            else:
                print("❌ Failed to generate reference-based routine")
                return 1
        elif args.routine_type == "sample":
            print("\n🎨 Sample-based routine generation selected...")
            result = handle_sample_based_routine()
            if result:
                print(f"\n✅ Sample-based routine generation complete!")
                return 0
            else:
                print("❌ Failed to generate sample-based routine")
                return 1
    
    # Load activities
    print("\n📂 Loading activities...")
    activities = load_activities(args)
    
    if not activities:
        print("❌ No activities loaded. Exiting.")
        return 1
    
    # Ensure all activities have required attributes
    activities = ensure_activities_attributes(activities)
    
    print(f"✅ Loaded {len(activities)} activities")
    
    # Show the original realistic schedule before algorithms run
    if activities and any(hasattr(activity, 'day') for activity in activities):
        print("\n🔍 ORIGINAL REALISTIC SCHEDULE (Before Algorithm Processing):")
        print_realistic_schedule(activities)
    
    # Process activities
    if args.run_all:
        results = run_all_algorithms(activities)
        
        # Generate output for the best result (highest weight)
        scheduler = ConflictFreeScheduler()
        best_algorithm = max(results.keys(), 
                           key=lambda k: scheduler.calculate_total_weight(results[k]))
        best_result = results[best_algorithm]
        
        # Ensure activities have required attributes
        best_result = ensure_activities_attributes(best_result)
        
        print(f"\n🏆 Best result: {best_algorithm.upper()}")
        
        # Use enhanced PDF generation based on user input
        if hasattr(args, 'routine_type') and args.routine_type in ["comprehensive", "batch", "faculty"]:
            # Use enhanced routine system
            user_input = {
                "routine_type": args.routine_type,
                "batch": args.batch or "BCSE24",
                "section": args.section
            }
            output_path = process_enhanced_routine(user_input, best_result)
            if output_path:
                print(f"\n✅ Enhanced {args.routine_type} routine generated: {output_path}")
        elif hasattr(args, 'basic_pdf') and args.basic_pdf:
            # Basic HTML generation
            pdf_gen = PDFGenerator()
            output_path = pdf_gen.generate_schedule_html(best_result, f"Schedule - {best_algorithm.upper()}")
            print(f"\n✅ Basic HTML schedule generated: {output_path}")
        elif hasattr(args, 'academic_pdf') and args.academic_pdf:
            # Academic PDF generation
            batch_code = args.batch if args.batch else "BCSE24"
            pdf_gen = AcademicPDFGenerator()
            output_path = pdf_gen.generate_academic_schedule(best_result, batch_code, args.section, args.semester)
            print(f"\n✅ Academic PDF generated: {output_path}")
        else:
            # Enhanced section routine (default)
            batch_code = args.batch if args.batch else "BCSE24"
            output_path = handle_section_routine(best_result, batch_code, args.section)
            print(f"\n✅ Enhanced section routine generated: {output_path}")
    
    elif hasattr(args, 'preserve_schedule') and args.preserve_schedule or (hasattr(args, 'algorithm') and args.algorithm == "preserve"):
        # Preserve realistic schedule without optimization
        result = preserve_realistic_schedule(activities)
        
        if result:
            # Print realistic schedule with day and time information
            print_realistic_schedule(result)
            
            # Generate enhanced PDF
            batch_code = args.batch if args.batch else "BCSE24"
            output_path = handle_section_routine(result, batch_code, args.section)
            print(f"\n✅ Enhanced realistic routine generated: {output_path}")
    
    else:
        # Run single algorithm
        result = run_single_algorithm(args.algorithm, activities)
        
        if result:
            # Ensure activities have required attributes
            result = ensure_activities_attributes(result)
            
            # Print realistic schedule with day and time information
            print_realistic_schedule(result)
            
            # Use enhanced PDF generation based on user input
            if hasattr(args, 'routine_type') and args.routine_type in ["comprehensive", "batch", "faculty"]:
                # Use enhanced routine system
                user_input = {
                    "routine_type": args.routine_type,
                    "batch": args.batch or "BCSE24",
                    "section": args.section
                }
                output_path = process_enhanced_routine(user_input, result)
                if output_path:
                    print(f"\n✅ Enhanced {args.routine_type} routine generated: {output_path}")
            elif hasattr(args, 'basic_pdf') and args.basic_pdf:
                # Basic HTML generation
                pdf_gen = PDFGenerator()
                output_path = pdf_gen.generate_schedule_html(result, f"Schedule - {args.algorithm.upper()}")
                print(f"\n✅ Basic HTML schedule generated: {output_path}")
            elif hasattr(args, 'academic_pdf') and args.academic_pdf:
                # Academic PDF generation
                batch_code = args.batch if args.batch else "BCSE24"
                pdf_gen = AcademicPDFGenerator()
                output_path = pdf_gen.generate_academic_schedule(result, batch_code, args.section, args.semester)
                print(f"\n✅ Academic PDF generated: {output_path}")
            else:
                # Enhanced section routine (default)
                batch_code = args.batch if args.batch else "BCSE24"
                output_path = handle_section_routine(result, batch_code, args.section)
                print(f"\n✅ Enhanced section routine generated: {output_path}")
            
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
