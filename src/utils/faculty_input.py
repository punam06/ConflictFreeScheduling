#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Faculty Input System for Conflict-Free Scheduling System

This module provides faculty input functionality for course scheduling.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
import os


@dataclass
class FacultyInput:
    """Class representing faculty input information"""
    name: str
    email: str = ""
    department: str = "CSE"
    available_times: List[Tuple[int, int]] = None  # List of (start, end) time slots
    preferred_courses: List[str] = None
    max_hours_per_week: int = 18
    room_preferences: List[str] = None


class FacultyInputSystem:
    """System for handling faculty input and automatic scheduling"""
    
    def __init__(self):
        """Initialize faculty input system"""
        self.faculties = []
        self.rooms = [
            "CSE-401", "CSE-402", "CSE-403", "CSE-404", "CSE-405", 
            "CSE-Lab1", "CSE-Lab2", "CSE-Lab3", "Physics-Lab", "Math-201"
        ]
        self.courses = []
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def add_faculty_interactive(self) -> FacultyInput:
        """Interactive faculty input"""
        print("\\n" + "="*60)
        print("🎓 Faculty Information Input System")
        print("="*60)
        
        name = input("👨‍🏫 Enter faculty name: ").strip()
        email = input("📧 Enter email address: ").strip()
        department = input("🏢 Enter department (default: CSE): ").strip() or "CSE"
        
        print("\\n⏰ Available Time Slots:")
        print("Please enter your available time slots.")
        print("Time slots are in 30-minute intervals starting from 8:00 AM")
        print("Example: 0 = 8:00 AM, 2 = 9:00 AM, 4 = 10:00 AM, etc.")
        print("Enter time ranges as start-end (e.g., 0-4 for 8:00 AM - 10:00 AM)")
        
        available_times = []
        while True:
            time_input = input("Enter time slot (start-end) or 'done' to finish: ").strip()
            if time_input.lower() == 'done':
                break
            
            try:
                if '-' in time_input:
                    start, end = map(int, time_input.split('-'))
                    available_times.append((start, end))
                    start_time = self._format_time_slot(start)
                    end_time = self._format_time_slot(end)
                    print(f"  ✅ Added: {start_time} - {end_time}")
                else:
                    print("  ❌ Invalid format. Use start-end (e.g., 0-4)")
            except ValueError:
                print("  ❌ Invalid format. Use numbers only.")
        
        print("\\n📚 Preferred Courses:")
        print("Enter course codes you prefer to teach (e.g., CSE101, CSE201)")
        
        preferred_courses = []
        while True:
            course = input("Enter course code or 'done' to finish: ").strip()
            if course.lower() == 'done':
                break
            if course:
                preferred_courses.append(course.upper())
                print(f"  ✅ Added: {course.upper()}")
        
        max_hours = input("\\n⏳ Maximum hours per week (default: 18): ").strip()
        max_hours = int(max_hours) if max_hours.isdigit() else 18
        
        print("\\n🏠 Room Preferences:")
        print("Available rooms:", ", ".join(self.rooms))
        
        room_preferences = []
        while True:
            room = input("Enter preferred room or 'done' to finish: ").strip()
            if room.lower() == 'done':
                break
            if room in self.rooms:
                room_preferences.append(room)
                print(f"  ✅ Added: {room}")
            elif room:
                print(f"  ❌ Room {room} not available. Available: {', '.join(self.rooms)}")
        
        faculty = FacultyInput(
            name=name,
            email=email,
            department=department,
            available_times=available_times,
            preferred_courses=preferred_courses,
            max_hours_per_week=max_hours,
            room_preferences=room_preferences
        )
        
        self.faculties.append(faculty)
        print(f"\\n✅ Faculty {name} added successfully!")
        return faculty
    
    def add_course_for_faculty(self, faculty_name: str, course_code: str, 
                              course_name: str, credits: float, duration: int = 90):
        """Add a course for a specific faculty"""
        
        # Find faculty
        faculty = next((f for f in self.faculties if f.name == faculty_name), None)
        if not faculty:
            print(f"❌ Faculty {faculty_name} not found!")
            return None
        
        # Find available time slot for the faculty
        available_slot = None
        for start, end in faculty.available_times:
            # Check if the duration fits in this time slot
            slot_duration = (end - start) * 30  # Convert to minutes
            if slot_duration >= duration:
                available_slot = (start, start + (duration // 30))
                break
        
        if not available_slot:
            print(f"❌ No available time slot found for {faculty_name}")
            return None
        
        # Allocate room
        allocated_room = self._allocate_room(available_slot, faculty.room_preferences)
        
        # Create course entry
        course = {
            'course_code': course_code,
            'course_name': course_name,
            'faculty_name': faculty_name,
            'credits': credits,
            'duration': duration,
            'start_time': available_slot[0],
            'end_time': available_slot[1],
            'room': allocated_room,
            'department': faculty.department
        }
        
        self.courses.append(course)
        print(f"✅ Course {course_code} assigned to {faculty_name}")
        print(f"   Time: {self._format_time_slot(available_slot[0])} - {self._format_time_slot(available_slot[1])}")
        print(f"   Room: {allocated_room}")
        
        return course
    
    def _allocate_room(self, time_slot: Tuple[int, int], preferences: List[str] = None) -> str:
        """Allocate room based on availability and preferences"""
        
        # Check preferred rooms first
        if preferences:
            for room in preferences:
                if self._is_room_available(room, time_slot):
                    return room
        
        # Check all available rooms
        for room in self.rooms:
            if self._is_room_available(room, time_slot):
                return room
        
        return "TBD"
    
    def _is_room_available(self, room: str, time_slot: Tuple[int, int]) -> bool:
        """Check if room is available at given time slot"""
        
        for course in self.courses:
            if course['room'] == room:
                # Check for time conflict
                course_start = course['start_time']
                course_end = course['end_time']
                
                if not (time_slot[1] <= course_start or time_slot[0] >= course_end):
                    return False
        
        return True
    
    def generate_faculty_schedule(self) -> Dict:
        """Generate complete schedule based on faculty input"""
        
        schedule = {
            'faculties': [],
            'courses': self.courses,
            'summary': {
                'total_faculties': len(self.faculties),
                'total_courses': len(self.courses),
                'rooms_used': len(set(course['room'] for course in self.courses if course['room'] != 'TBD'))
            }
        }
        
        for faculty in self.faculties:
            faculty_courses = [course for course in self.courses if course['faculty_name'] == faculty.name]
            total_hours = sum(course['duration'] for course in faculty_courses) / 60
            
            faculty_data = {
                'name': faculty.name,
                'email': faculty.email,
                'department': faculty.department,
                'courses': faculty_courses,
                'total_hours': total_hours,
                'max_hours': faculty.max_hours_per_week,
                'utilization': (total_hours / faculty.max_hours_per_week) * 100 if faculty.max_hours_per_week > 0 else 0
            }
            
            schedule['faculties'].append(faculty_data)
        
        return schedule
    
    def save_faculty_data(self, filename: str = "faculty_data.json"):
        """Save faculty data to file"""
        
        filepath = os.path.join(self.data_dir, filename)
        
        data = {
            'faculties': [
                {
                    'name': f.name,
                    'email': f.email,
                    'department': f.department,
                    'available_times': f.available_times,
                    'preferred_courses': f.preferred_courses,
                    'max_hours_per_week': f.max_hours_per_week,
                    'room_preferences': f.room_preferences
                }
                for f in self.faculties
            ],
            'courses': self.courses
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Faculty data saved to {filepath}")
    
    def load_faculty_data(self, filename: str = "faculty_data.json") -> bool:
        """Load faculty data from file"""
        
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ File {filepath} not found")
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.faculties = [
                FacultyInput(
                    name=f['name'],
                    email=f['email'],
                    department=f['department'],
                    available_times=f['available_times'],
                    preferred_courses=f['preferred_courses'],
                    max_hours_per_week=f['max_hours_per_week'],
                    room_preferences=f['room_preferences']
                )
                for f in data['faculties']
            ]
            
            self.courses = data['courses']
            print(f"✅ Faculty data loaded from {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading faculty data: {e}")
            return False
    
    def interactive_course_assignment(self):
        """Interactive course assignment for faculties"""
        
        if not self.faculties:
            print("❌ No faculties added yet. Please add faculties first.")
            return
        
        print("\\n" + "="*60)
        print("📚 Course Assignment System")
        print("="*60)
        
        print("\\nAvailable Faculties:")
        for i, faculty in enumerate(self.faculties, 1):
            print(f"  {i}. {faculty.name} ({faculty.department})")
        
        while True:
            print("\\n" + "-"*40)
            faculty_choice = input("Select faculty number (or 'done' to finish): ").strip()
            
            if faculty_choice.lower() == 'done':
                break
            
            try:
                faculty_idx = int(faculty_choice) - 1
                if 0 <= faculty_idx < len(self.faculties):
                    faculty = self.faculties[faculty_idx]
                    
                    print(f"\\n👨‍🏫 Adding course for: {faculty.name}")
                    course_code = input("📖 Enter course code (e.g., CSE101): ").strip().upper()
                    course_name = input("📚 Enter course name: ").strip()
                    
                    credits_input = input("💳 Enter credit hours (default: 3.0): ").strip()
                    credits = float(credits_input) if credits_input else 3.0
                    
                    duration_input = input("⏱️ Enter duration in minutes (default: 90): ").strip()
                    duration = int(duration_input) if duration_input else 90
                    
                    self.add_course_for_faculty(faculty.name, course_code, course_name, credits, duration)
                else:
                    print("❌ Invalid faculty number")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _format_time_slot(self, slot: int) -> str:
        """Format time slot to readable time"""
        base_hour = 8
        total_minutes = slot * 30
        hours = base_hour + (total_minutes // 60)
        minutes = total_minutes % 60
        
        hours = hours % 24
        
        if hours == 0:
            hour_12 = 12
            am_pm = "AM"
        elif hours < 12:
            hour_12 = hours
            am_pm = "AM"
        elif hours == 12:
            hour_12 = 12
            am_pm = "PM"
        else:
            hour_12 = hours - 12
            am_pm = "PM"
        
        return f"{hour_12}:{minutes:02d} {am_pm}"
    
    def print_schedule_summary(self):
        """Print schedule summary"""
        
        if not self.courses:
            print("❌ No courses scheduled yet.")
            return
        
        print("\\n" + "="*80)
        print("📋 FACULTY SCHEDULE SUMMARY")
        print("="*80)
        
        for faculty in self.faculties:
            faculty_courses = [course for course in self.courses if course['faculty_name'] == faculty.name]
            
            if faculty_courses:
                print(f"\\n👨‍🏫 {faculty.name} ({faculty.email})")
                print("-" * 50)
                
                for course in faculty_courses:
                    start_time = self._format_time_slot(course['start_time'])
                    end_time = self._format_time_slot(course['end_time'])
                    print(f"  📖 {course['course_code']}: {course['course_name']}")
                    print(f"     ⏰ {start_time} - {end_time} | 🏠 {course['room']} | 💳 {course['credits']} credits")
                
                total_hours = sum(course['duration'] for course in faculty_courses) / 60
                utilization = (total_hours / faculty.max_hours_per_week) * 100
                print(f"     📊 Total: {total_hours:.1f}h/{faculty.max_hours_per_week}h ({utilization:.1f}% utilization)")


def main():
    """Main function for faculty input system"""
    
    system = FacultyInputSystem()
    
    while True:
        print("\\n" + "="*60)
        print("🎓 FACULTY INPUT SYSTEM - MAIN MENU")
        print("="*60)
        print("1. Add Faculty Member")
        print("2. Assign Courses to Faculty")
        print("3. View Schedule Summary")
        print("4. Save Faculty Data")
        print("5. Load Faculty Data")
        print("6. Exit")
        
        choice = input("\\nSelect option (1-6): ").strip()
        
        if choice == '1':
            system.add_faculty_interactive()
        elif choice == '2':
            system.interactive_course_assignment()
        elif choice == '3':
            system.print_schedule_summary()
        elif choice == '4':
            system.save_faculty_data()
        elif choice == '5':
            system.load_faculty_data()
        elif choice == '6':
            print("👋 Thank you for using Faculty Input System!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
