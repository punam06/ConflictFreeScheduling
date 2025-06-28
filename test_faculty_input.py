#!/usr/bin/env python3
"""
Faculty Input System Test Script
================================

This script demonstrates the faculty input format and tests the faculty routine generation.

FACULTY INPUT FORMAT:
====================

1. Time Slots (30-minute intervals starting from 8:00 AM):
   - 0 = 8:00 AM    - 12 = 2:00 PM
   - 2 = 9:00 AM    - 14 = 3:00 PM  
   - 4 = 10:00 AM   - 16 = 4:00 PM
   - 6 = 11:00 AM   - 18 = 5:00 PM
   - 8 = 12:00 PM   - 20 = 6:00 PM
   - 10 = 1:00 PM   - 22 = 7:00 PM

2. Available Times: List of [start, end] time slot ranges
   Example: [0, 4] = 8:00 AM to 10:00 AM

3. Course Codes: 4-digit format (CSE4401, CSE3321, etc.)

4. Rooms: Available rooms from ['302', '303', '304', '504', '1003']
"""

import sys
import os
import json

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.faculty_input import FacultyInputSystem

def format_time_slot(slot):
    """Convert time slot to readable format"""
    hours = 8 + (slot // 2)
    minutes = 30 * (slot % 2)
    return f"{hours:02d}:{minutes:02d}"

def demonstrate_faculty_input():
    """Demonstrate faculty input format"""
    
    print("=" * 80)
    print("🎓 FACULTY INPUT SYSTEM - FORMAT DEMONSTRATION")
    print("=" * 80)
    
    print("\n📋 FACULTY INPUT FORMAT:")
    print("-" * 40)
    
    print("\n⏰ Time Slot Reference:")
    for i in range(0, 24, 2):
        time_str = format_time_slot(i)
        print(f"  {i:2d} = {time_str}")
    
    print("\n👨‍🏫 Faculty Information Fields:")
    print("  - Name: Full name of faculty member")
    print("  - Email: Faculty email address") 
    print("  - Department: Usually 'CSE'")
    print("  - Available Times: List of [start, end] time ranges")
    print("  - Preferred Courses: List of 4-digit course codes")
    print("  - Max Hours Per Week: Maximum teaching hours (default: 18)")
    print("  - Room Preferences: Preferred room numbers")
    
    print("\n📚 Course Assignment Fields:")
    print("  - Course Code: 4-digit format (CSE4401, CSE3321, etc.)")
    print("  - Course Name: Full course name")
    print("  - Faculty Name: Must match faculty name exactly")
    print("  - Credits: Course credit hours (typically 1.5 or 3.0)")
    print("  - Duration: Class duration in minutes (default: 90)")
    
    print("\n🏠 Available Rooms:")
    print("  ['302', '303', '304', '504', '1003']")

def test_faculty_system():
    """Test faculty system with sample data"""
    
    print("\n" + "=" * 80)
    print("🧪 TESTING FACULTY INPUT SYSTEM")
    print("=" * 80)
    
    # Load test data
    test_file = "faculty_input_test.json"  # Just the filename, not the full path
    
    faculty_system = FacultyInputSystem()
    
    # Load faculty data
    if faculty_system.load_faculty_data(test_file):
        print(f"✅ Loaded faculty data from {test_file}")
    else:
        print(f"❌ Failed to load faculty data from {test_file}")
        return
    
    # Display loaded data
    print("\n📊 LOADED FACULTY DATA:")
    print("-" * 50)
    
    for i, faculty in enumerate(faculty_system.faculties, 1):
        print(f"\n{i}. {faculty.name}")
        print(f"   📧 Email: {faculty.email}")
        print(f"   🏢 Department: {faculty.department}")
        print(f"   ⏰ Available Times:")
        for start, end in faculty.available_times:
            start_time = format_time_slot(start)
            end_time = format_time_slot(end)
            print(f"      {start_time} - {end_time}")
        print(f"   📚 Preferred Courses: {', '.join(faculty.preferred_courses)}")
        print(f"   ⏳ Max Hours/Week: {faculty.max_hours_per_week}")
        print(f"   🏠 Room Preferences: {', '.join(faculty.room_preferences)}")
    
    print(f"\n📚 ASSIGNED COURSES ({len(faculty_system.courses)}):")
    print("-" * 50)
    
    for i, course in enumerate(faculty_system.courses, 1):
        start_time = format_time_slot(course['start_time'])
        end_time = format_time_slot(course['end_time'])
        print(f"\n{i}. {course['course_code']} - {course['course_name']}")
        print(f"   👨‍🏫 Faculty: {course['faculty_name']}")
        print(f"   ⏰ Time: {start_time} - {end_time}")
        print(f"   🏠 Room: {course['room']}")
        print(f"   📊 Credits: {course['credits']}")
    
    # Generate schedule summary
    schedule = faculty_system.generate_faculty_schedule()
    
    print(f"\n📈 SCHEDULE SUMMARY:")
    print("-" * 50)
    print(f"  Total Faculties: {schedule['summary']['total_faculties']}")
    print(f"  Total Courses: {schedule['summary']['total_courses']}")
    print(f"  Rooms Used: {schedule['summary']['rooms_used']}")
    
    print(f"\n👨‍🏫 FACULTY UTILIZATION:")
    print("-" * 50)
    for faculty_data in schedule['faculties']:
        utilization = faculty_data['utilization']
        status = "✅" if utilization <= 100 else "⚠️"
        print(f"  {faculty_data['name']}: {utilization:.1f}% {status}")
        print(f"    Hours: {faculty_data['total_hours']:.1f}/{faculty_data['max_hours']}")
    
    return faculty_system

def run_faculty_routine_generation(faculty_system):
    """Generate routine using faculty system"""
    
    print("\n" + "=" * 80)
    print("📅 GENERATING FACULTY ROUTINE")
    print("=" * 80)
    
    # Convert faculty courses to Activity objects for routine generation
    from scheduler import Activity
    
    activities = []
    for course in faculty_system.courses:
        # Convert time slots to minutes (each slot = 30 minutes, starting from 8:00 AM)
        start_minutes = 480 + (course['start_time'] * 30)  # 8:00 AM = 480 minutes
        end_minutes = 480 + (course['end_time'] * 30)
        
        activity = Activity(
            id=len(activities) + 1,
            start=start_minutes,
            end=end_minutes,
            weight=course['credits'],
            name=course['course_name'],
            room=course['room']
        )
        # Add faculty and course code information
        activity.faculty = course['faculty_name']
        activity.course_code = course['course_code']
        activities.append(activity)
    
    print(f"✅ Converted {len(activities)} courses to activities")
    
    # Use enhanced PDF generation
    from utils.enhanced_pdf_generator import EnhancedPDFGenerator
    
    pdf_gen = EnhancedPDFGenerator()
    output_path = pdf_gen.generate_section_routine(activities, "FACULTY", "INPUT")
    
    print(f"✅ Faculty routine generated: {output_path}")
    
    # Print schedule in readable format
    print(f"\n📅 FACULTY SCHEDULE:")
    print("-" * 80)
    
    # Group by day (simulate days for display)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    activities_per_day = len(activities) // len(days) + 1
    
    for day_idx, day in enumerate(days):
        day_activities = activities[day_idx * activities_per_day:(day_idx + 1) * activities_per_day]
        
        if day_activities:
            print(f"\n📅 {day}:")
            print("-" * 60)
            
            for activity in day_activities:
                start_hour = activity.start // 60
                start_min = activity.start % 60
                end_hour = activity.end // 60
                end_min = activity.end % 60
                time_str = f"{start_hour:02d}:{start_min:02d}-{end_hour:02d}:{end_min:02d}"
                
                print(f"  {time_str} | {activity.course_code} | {activity.name}")
                print(f"           | Faculty: {activity.faculty} | Room: {activity.room}")
    
    return output_path

if __name__ == "__main__":
    try:
        # Demonstrate format
        demonstrate_faculty_input()
        
        # Test faculty system
        faculty_system = test_faculty_system()
        
        if faculty_system:
            # Generate routine
            output_path = run_faculty_routine_generation(faculty_system)
            
            print(f"\n🎉 Faculty Input System Test Completed Successfully!")
            print(f"📄 Generated routine: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
