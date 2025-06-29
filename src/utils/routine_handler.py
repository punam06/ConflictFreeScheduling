# Enhanced Routine Handlers
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import from scheduler.py
from src.scheduler import Activity
from src.utils.enhanced_pdf_generator import EnhancedPDFGenerator
from src.utils.comprehensive_routine_generator import ComprehensiveRoutineGenerator
from src.utils.sample_routine_generator import SampleRoutineGenerator

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
        # Load comprehensive routine data from JSON (all batches and sections)
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_file = os.path.join(script_dir, "data", "sample_routine_data.json")
        
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            return None
            
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Use the comprehensive routine generator with proper conflict-free scheduling
        generator = ComprehensiveRoutineGenerator()
        
        # Generate comprehensive routine using the loaded data
        output_dir = os.path.join(script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create timestamp for unique output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_output = os.path.join(output_dir, f"comprehensive_departmental_routine_{timestamp}")
        
        # Generate both PDF and HTML formats
        base_output_pdf = f"{base_output}.pdf"
        base_output_html = f"{base_output}.html"
        
        # Use the comprehensive routine generator instead of sample routine generator
        pdf_file = generator.generate_comprehensive_routine_pdf(data_file, base_output_pdf)
        html_file = generator.generate_html_routine(data_file, base_output_html)
        
        if pdf_file or html_file:
            if pdf_file:
                print(f"✅ Comprehensive departmental routine generated (PDF): {pdf_file}")
            if html_file:
                print(f"🌐 Comprehensive departmental routine generated (HTML): {html_file}")
            return html_file or pdf_file
        else:
            # Fall back to sample routine generator if comprehensive generator fails
            print("⚠️ Falling back to sample routine generator...")
            sample_generator = SampleRoutineGenerator()
            
            # Use generate_all_formats which returns both HTML and PDF files
            html_file, pdf_file = sample_generator.generate_all_formats(data_file, base_output)
            
            if pdf_file or html_file:
                print(f"✅ Comprehensive departmental routine generated (fallback): {pdf_file or html_file}")
                return pdf_file or html_file
            else:
                print("❌ Failed to generate comprehensive routine")
                return None
                
    except Exception as e:
        print(f"❌ Error generating comprehensive routine: {str(e)}")
        # Fallback to simple comprehensive routine
        print("🔄 Falling back to enhanced comprehensive routine...")
        
        pdf_gen = EnhancedPDFGenerator()
        return pdf_gen.generate_comprehensive_routine({
            "All Departments": activities
        })


from src.utils.faculty_input import FacultyInputSystem

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
    
    # If still no data, create it from our default faculty schedule
    if not data_loaded or not faculty_system.courses:
        print("\nℹ️ No valid faculty data found, using default faculty schedule")
        return create_default_faculty_schedule()
    
    # Data was loaded successfully
    print(f"📊 Loaded {len(faculty_system.faculties)} faculty members and {len(faculty_system.courses)} courses")
    
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


# Handle interactive faculty input (helper function)
def handle_interactive_faculty_input(faculty_system):
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


# Create default faculty schedule when no input data is available
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
    
    print(f"✅ Generated {len(default_activities)} default faculty activities")
    return default_activities
