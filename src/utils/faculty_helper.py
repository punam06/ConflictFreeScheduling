# Helper functions for faculty input processing 
import json
import os
from typing import List, Dict, Any
from datetime import datetime
from scheduler import Activity

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

def load_faculty_data(faculty_system, file_path=None) -> bool:
    """Load faculty data from JSON file"""
    try:
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            with open("data/faculty_data.json", 'r') as f:
                data = json.load(f)
        
        if 'faculties' in data:
            faculty_system.faculties = data['faculties']
        
        if 'courses' in data:
            faculty_system.courses = data['courses']
        
        return True
    except Exception as e:
        print(f"Error loading faculty data: {e}")
        return False
