#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Faculty Input System for Conflict-Free Scheduling System

This module provides robust faculty input functionality for course scheduling
with advanced validation, conflict detection, and user-friendly interfaces.
"""

from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
import json
import os
import re
from datetime import datetime, time
import csv


@dataclass
class FacultyInput:
    """Enhanced class representing faculty input information"""
    name: str
    email: str = ""
    department: str = "CSE"
    available_times: List[Tuple[int, int]] = field(default_factory=list)
    preferred_courses: List[str] = field(default_factory=list)
    max_hours_per_week: int = 18
    room_preferences: List[str] = field(default_factory=list)
    phone: str = ""
    designation: str = "Lecturer"
    specialization: List[str] = field(default_factory=list)
    unavailable_days: List[str] = field(default_factory=list)  # ['Saturday', 'Sunday']
    
    def __post_init__(self):
        """Validate faculty input after initialization"""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Faculty name cannot be empty")
        
        if self.email and not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")
        
        if self.max_hours_per_week < 1 or self.max_hours_per_week > 40:
            raise ValueError("Max hours per week must be between 1 and 40")
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_total_available_hours(self) -> float:
        """Calculate total available hours per week"""
        total_minutes = sum([(end - start) * 30 for start, end in self.available_times])
        return total_minutes / 60
    
    def conflicts_with_time(self, start: int, end: int) -> bool:
        """Check if given time conflicts with available times"""
        for avail_start, avail_end in self.available_times:
            if not (end <= avail_start or start >= avail_end):
                return False  # No conflict found in this slot
        return True  # Conflicts with all available slots


class ConflictDetector:
    """Enhanced conflict detection for scheduling"""
    
    @staticmethod
    def detect_faculty_conflicts(courses: List[Dict]) -> List[Dict]:
        """Detect conflicts between faculty schedules"""
        conflicts = []
        
        for i, course1 in enumerate(courses):
            for j, course2 in enumerate(courses[i+1:], i+1):
                # Same faculty scheduling conflict
                if (course1['faculty_name'] == course2['faculty_name'] and
                    course1['room'] == course2['room']):
                    if ConflictDetector._time_overlap(course1, course2):
                        conflicts.append({
                            'type': 'faculty_time_room',
                            'courses': [course1, course2],
                            'description': f"Faculty {course1['faculty_name']} has conflicting schedules in {course1['room']}"
                        })
                
                # Room conflict
                elif course1['room'] == course2['room']:
                    if ConflictDetector._time_overlap(course1, course2):
                        conflicts.append({
                            'type': 'room',
                            'courses': [course1, course2],
                            'description': f"Room {course1['room']} has scheduling conflict"
                        })
        
        return conflicts
    
    @staticmethod
    def _time_overlap(course1: Dict, course2: Dict) -> bool:
        """Check if two courses have time overlap"""
        return not (course1['end_time'] <= course2['start_time'] or 
                   course1['start_time'] >= course2['end_time'])
    
    @staticmethod
    def detect_workload_issues(faculties: List[FacultyInput], courses: List[Dict]) -> List[Dict]:
        """Detect faculty workload issues"""
        issues = []
        
        for faculty in faculties:
            faculty_courses = [c for c in courses if c['faculty_name'] == faculty.name]
            total_hours = sum(course['duration'] for course in faculty_courses) / 60
            
            if total_hours > faculty.max_hours_per_week:
                issues.append({
                    'type': 'overload',
                    'faculty': faculty.name,
                    'scheduled_hours': total_hours,
                    'max_hours': faculty.max_hours_per_week,
                    'description': f"{faculty.name} is overloaded: {total_hours:.1f}h > {faculty.max_hours_per_week}h"
                })
            elif total_hours < faculty.max_hours_per_week * 0.5:
                issues.append({
                    'type': 'underload',
                    'faculty': faculty.name,
                    'scheduled_hours': total_hours,
                    'max_hours': faculty.max_hours_per_week,
                    'description': f"{faculty.name} is underutilized: {total_hours:.1f}h < {faculty.max_hours_per_week * 0.5:.1f}h"
                })
        
        return issues


class EnhancedFacultyInputSystem:
    """Enhanced system for handling faculty input and automatic scheduling"""
    
    def __init__(self):
        """Initialize enhanced faculty input system"""
        self.faculties = []
        self.courses = []
        self.rooms = [
            "CSE-401", "CSE-402", "CSE-403", "CSE-404", "CSE-405", 
            "CSE-Lab1", "CSE-Lab2", "CSE-Lab3", "Physics-Lab", "Math-201",
            "CSE-501", "CSE-502", "CSE-503", "Auditorium", "Seminar-Room"
        ]
        self.departments = ["CSE", "EEE", "ME", "CE", "ECE", "Math", "Physics", "Chemistry"]
        self.designations = ["Professor", "Associate Professor", "Assistant Professor", 
                           "Lecturer", "Senior Lecturer", "Adjunct Professor"]
        self.data_dir = "data"
        self.conflict_detector = ConflictDetector()
        os.makedirs(self.data_dir, exist_ok=True)
    
    def validate_input(self, prompt: str, validation_func, error_msg: str, default=None) -> any:
        """Generic input validation with retry mechanism"""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input and default is not None:
                    return default
                
                if validation_func(user_input):
                    return user_input
                else:
                    print(f"❌ {error_msg}")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Input interrupted")
                return default if default is not None else ""
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def add_faculty_interactive(self) -> Optional[FacultyInput]:
        """Enhanced interactive faculty input with validation"""
        print("\n" + "="*70)
        print("🎓 ENHANCED FACULTY INFORMATION SYSTEM")
        print("="*70)
        
        try:
            # Name validation
            name = self.validate_input(
                "👨‍🏫 Enter faculty name: ",
                lambda x: len(x.strip()) >= 2,
                "Name must be at least 2 characters long"
            )
            if not name:
                return None
            
            # Check for duplicate names
            if any(f.name.lower() == name.lower() for f in self.faculties):
                print(f"⚠️ Faculty with name '{name}' already exists!")
                overwrite = input("Do you want to update existing faculty? (y/n): ").lower() == 'y'
                if not overwrite:
                    return None
                # Remove existing faculty
                self.faculties = [f for f in self.faculties if f.name.lower() != name.lower()]
            
            # Email validation
            email = self.validate_input(
                "📧 Enter email address (optional): ",
                lambda x: not x or re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', x),
                "Invalid email format",
                default=""
            )
            
            # Department selection
            print(f"\n🏢 Available departments: {', '.join(self.departments)}")
            department = self.validate_input(
                "Enter department (default: CSE): ",
                lambda x: not x or x.upper() in self.departments,
                f"Department must be one of: {', '.join(self.departments)}",
                default="CSE"
            ).upper()
            
            # Designation selection
            print(f"\n👔 Available designations: {', '.join(self.designations)}")
            designation = self.validate_input(
                "Enter designation (default: Lecturer): ",
                lambda x: not x or x in self.designations,
                f"Designation must be one of: {', '.join(self.designations)}",
                default="Lecturer"
            )
            
            # Phone number
            phone = self.validate_input(
                "� Enter phone number (optional): ",
                lambda x: not x or (x.replace('+', '').replace('-', '').replace(' ', '').isdigit() and len(x) >= 10),
                "Invalid phone number format",
                default=""
            )
            
            # Specialization
            print("\n🎯 Enter areas of specialization (one per line, 'done' to finish):")
            specialization = []
            while True:
                spec = input("Enter specialization or 'done': ").strip()
                if spec.lower() == 'done':
                    break
                if spec:
                    specialization.append(spec)
                    print(f"  ✅ Added: {spec}")
            
            # Available time slots with enhanced interface
            available_times = self._get_available_times_interactive()
            
            # Preferred courses
            preferred_courses = self._get_preferred_courses_interactive()
            
            # Max hours validation
            max_hours = self.validate_input(
                "\n⏳ Maximum hours per week (1-40, default: 18): ",
                lambda x: not x or (x.isdigit() and 1 <= int(x) <= 40),
                "Hours must be between 1 and 40",
                default="18"
            )
            max_hours = int(max_hours) if max_hours else 18
            
            # Room preferences
            room_preferences = self._get_room_preferences_interactive()
            
            # Unavailable days
            unavailable_days = self._get_unavailable_days_interactive()
            
            faculty = FacultyInput(
                name=name,
                email=email,
                department=department,
                designation=designation,
                phone=phone,
                specialization=specialization,
                available_times=available_times,
                preferred_courses=preferred_courses,
                max_hours_per_week=max_hours,
                room_preferences=room_preferences,
                unavailable_days=unavailable_days
            )
            
            self.faculties.append(faculty)
            print(f"\n✅ Faculty {name} added successfully!")
            print(f"   📊 Available hours: {faculty.get_total_available_hours():.1f} hours/week")
            return faculty
            
        except Exception as e:
            print(f"❌ Error adding faculty: {e}")
            return None
    def _get_available_times_interactive(self) -> List[Tuple[int, int]]:
        """Interactive time slot input with visual guide"""
        print("\n⏰ AVAILABLE TIME SLOTS")
        print("="*50)
        print("📅 Time Reference Guide:")
        print("   0 = 8:00 AM    8 = 12:00 PM   16 = 4:00 PM")
        print("   2 = 9:00 AM   10 = 1:00 PM    18 = 5:00 PM")
        print("   4 = 10:00 AM  12 = 2:00 PM    20 = 6:00 PM")
        print("   6 = 11:00 AM  14 = 3:00 PM    22 = 7:00 PM")
        print("\n💡 Examples:")
        print("   '0-4' = 8:00 AM to 10:00 AM")
        print("   '8-12' = 12:00 PM to 2:00 PM")
        print("   '14-18' = 3:00 PM to 5:00 PM")
        
        available_times = []
        while True:
            try:
                time_input = input("\nEnter time slot (start-end) or 'done' to finish: ").strip()
                if time_input.lower() == 'done':
                    break
                
                if '-' in time_input:
                    start, end = map(int, time_input.split('-'))
                    
                    # Validation
                    if start < 0 or end > 24 or start >= end:
                        print("  ❌ Invalid time range. Start must be < End, and within 0-24.")
                        continue
                    
                    # Check for overlaps
                    overlap = False
                    for existing_start, existing_end in available_times:
                        if not (end <= existing_start or start >= existing_end):
                            print(f"  ❌ Overlaps with existing slot: {self._format_time_slot(existing_start)} - {self._format_time_slot(existing_end)}")
                            overlap = True
                            break
                    
                    if not overlap:
                        available_times.append((start, end))
                        start_time = self._format_time_slot(start)
                        end_time = self._format_time_slot(end)
                        print(f"  ✅ Added: {start_time} - {end_time}")
                else:
                    print("  ❌ Invalid format. Use start-end (e.g., 0-4)")
                    
            except ValueError:
                print("  ❌ Invalid format. Use numbers only.")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Time input interrupted")
                break
        
        if not available_times:
            print("⚠️ No time slots entered. Adding default 9 AM - 5 PM slot.")
            available_times = [(2, 18)]  # 9 AM to 5 PM
        
        return available_times
    
    def _get_preferred_courses_interactive(self) -> List[str]:
        """Interactive course preference input"""
        print("\n📚 PREFERRED COURSES")
        print("="*30)
        print("Enter course codes you prefer to teach")
        print("Examples: CSE101, CSE201, MAT101")
        
        preferred_courses = []
        while True:
            try:
                course = input("Enter course code or 'done' to finish: ").strip()
                if course.lower() == 'done':
                    break
                if course:
                    course_upper = course.upper()
                    if course_upper not in preferred_courses:
                        preferred_courses.append(course_upper)
                        print(f"  ✅ Added: {course_upper}")
                    else:
                        print(f"  ⚠️ {course_upper} already added")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Course input interrupted")
                break
        
        return preferred_courses
    
    def _get_room_preferences_interactive(self) -> List[str]:
        """Interactive room preference input"""
        print("\n🏠 ROOM PREFERENCES")
        print("="*30)
        print("Available rooms:")
        for i, room in enumerate(self.rooms, 1):
            print(f"  {i:2d}. {room}")
        
        room_preferences = []
        while True:
            try:
                room_input = input("Enter room name/number or 'done' to finish: ").strip()
                if room_input.lower() == 'done':
                    break
                
                # Check if input is a number (room selection by index)
                if room_input.isdigit():
                    idx = int(room_input) - 1
                    if 0 <= idx < len(self.rooms):
                        room = self.rooms[idx]
                        if room not in room_preferences:
                            room_preferences.append(room)
                            print(f"  ✅ Added: {room}")
                        else:
                            print(f"  ⚠️ {room} already added")
                    else:
                        print(f"  ❌ Invalid room number. Choose 1-{len(self.rooms)}")
                else:
                    # Direct room name input
                    if room_input in self.rooms:
                        if room_input not in room_preferences:
                            room_preferences.append(room_input)
                            print(f"  ✅ Added: {room_input}")
                        else:
                            print(f"  ⚠️ {room_input} already added")
                    else:
                        print(f"  ❌ Room {room_input} not available")
                        
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Room input interrupted")
                break
        
        return room_preferences
    
    def _get_unavailable_days_interactive(self) -> List[str]:
        """Interactive unavailable days input"""
        print("\n📅 UNAVAILABLE DAYS")
        print("="*25)
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        unavailable_days = []
        while True:
            try:
                print("Available days:")
                for i, day in enumerate(days, 1):
                    status = "❌" if day in unavailable_days else "✅"
                    print(f"  {i}. {status} {day}")
                
                day_input = input("Enter day number to toggle or 'done' to finish: ").strip()
                if day_input.lower() == 'done':
                    break
                
                if day_input.isdigit():
                    idx = int(day_input) - 1
                    if 0 <= idx < len(days):
                        day = days[idx]
                        if day in unavailable_days:
                            unavailable_days.remove(day)
                            print(f"  ✅ {day} is now available")
                        else:
                            unavailable_days.append(day)
                            print(f"  ❌ {day} is now unavailable")
                    else:
                        print(f"  ❌ Invalid day number. Choose 1-{len(days)}")
                else:
                    print("  ❌ Please enter a number")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Day input interrupted")
                break
        
        return unavailable_days
    
    def add_course_for_faculty(self, faculty_name: str, course_code: str, 
                              course_name: str, credits: float, duration: int = 90) -> Optional[Dict]:
        """Enhanced course assignment with conflict detection"""
        
        # Find faculty
        faculty = next((f for f in self.faculties if f.name == faculty_name), None)
        if not faculty:
            print(f"❌ Faculty {faculty_name} not found!")
            return None
        
        # Validate course code format
        if not re.match(r'^[A-Z]{2,4}\d{3,4}$', course_code.upper()):
            print(f"⚠️ Course code {course_code} may not follow standard format (e.g., CSE101)")
        
        # Find available time slot for the faculty
        available_slot = None
        for start, end in faculty.available_times:
            # Check if the duration fits in this time slot
            slot_duration = (end - start) * 30  # Convert to minutes
            if slot_duration >= duration:
                potential_slot = (start, start + (duration // 30))
                
                # Check for conflicts with existing courses
                conflict = False
                for existing_course in self.courses:
                    if (existing_course['faculty_name'] == faculty_name and
                        not (potential_slot[1] <= existing_course['start_time'] or 
                             potential_slot[0] >= existing_course['end_time'])):
                        conflict = True
                        break
                
                if not conflict:
                    available_slot = potential_slot
                    break
        
        if not available_slot:
            print(f"❌ No available time slot found for {faculty_name}")
            print(f"   Required duration: {duration} minutes")
            print(f"   Available slots: {[f'{self._format_time_slot(s)} - {self._format_time_slot(e)}' for s, e in faculty.available_times]}")
            return None
        
        # Allocate room with enhanced logic
        allocated_room = self._allocate_room_enhanced(available_slot, faculty.room_preferences, course_code)
        
        # Create course entry
        course = {
            'course_code': course_code.upper(),
            'course_name': course_name,
            'faculty_name': faculty_name,
            'credits': credits,
            'duration': duration,
            'start_time': available_slot[0],
            'end_time': available_slot[1],
            'room': allocated_room,
            'department': faculty.department,
            'created_at': datetime.now().isoformat()
        }
        
        self.courses.append(course)
        print(f"✅ Course {course_code} assigned to {faculty_name}")
        print(f"   📅 Time: {self._format_time_slot(available_slot[0])} - {self._format_time_slot(available_slot[1])}")
        print(f"   🏠 Room: {allocated_room}")
        print(f"   💳 Credits: {credits}")
        
        return course
    
    def _allocate_room_enhanced(self, time_slot: Tuple[int, int], preferences: List[str] = None, 
                               course_code: str = "") -> str:
        """Enhanced room allocation with lab detection"""
        
        # Determine if course needs a lab
        needs_lab = any(keyword in course_code.upper() for keyword in ['LAB', 'PRAC', 'PROJECT'])
        
        # Filter rooms based on course requirements
        suitable_rooms = self.rooms
        if needs_lab:
            suitable_rooms = [room for room in self.rooms if 'Lab' in room]
        
        # Check preferred rooms first
        if preferences:
            for room in preferences:
                if room in suitable_rooms and self._is_room_available(room, time_slot):
                    return room
        
        # Check all suitable rooms
        for room in suitable_rooms:
            if self._is_room_available(room, time_slot):
                return room
        
        # If no suitable room found, check all rooms
        for room in self.rooms:
            if self._is_room_available(room, time_slot):
                return room + " (⚠️ Not optimal)"
        
        return "TBD (❌ No rooms available)"
    
    def _is_room_available(self, room: str, time_slot: Tuple[int, int]) -> bool:
        """Enhanced room availability check"""
        for course in self.courses:
            if course['room'] == room or course['room'].startswith(room):
                # Check for time conflict
                course_start = course['start_time']
                course_end = course['end_time']
                
                if not (time_slot[1] <= course_start or time_slot[0] >= course_end):
                    return False
        return True
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive schedule report with analytics"""
        
        # Detect conflicts
        conflicts = self.conflict_detector.detect_faculty_conflicts(self.courses)
        workload_issues = self.conflict_detector.detect_workload_issues(self.faculties, self.courses)
        
        # Room utilization analysis
        room_usage = {}
        for course in self.courses:
            room = course['room']
            if room not in room_usage:
                room_usage[room] = []
            room_usage[room].append(course)
        
        # Faculty workload analysis
        faculty_analysis = {}
        for faculty in self.faculties:
            faculty_courses = [c for c in self.courses if c['faculty_name'] == faculty.name]
            total_hours = sum(course['duration'] for course in faculty_courses) / 60
            
            faculty_analysis[faculty.name] = {
                'total_courses': len(faculty_courses),
                'total_hours': total_hours,
                'max_hours': faculty.max_hours_per_week,
                'utilization': (total_hours / faculty.max_hours_per_week) * 100 if faculty.max_hours_per_week > 0 else 0,
                'available_hours': faculty.get_total_available_hours(),
                'courses': faculty_courses,
                'preferred_times': faculty.available_times,
                'available_slots': self._get_available_slots_for_faculty(faculty)
            }
        
        report = {
            'summary': {
                'total_faculties': len(self.faculties),
                'total_courses': len(self.courses),
                'total_rooms_used': len([r for r in room_usage.keys() if not r.startswith('TBD')]),
                'conflicts_detected': len(conflicts),
                'workload_issues': len(workload_issues)
            },
            'faculty_analysis': faculty_analysis,
            'room_utilization': {
                room: {
                    'courses_scheduled': len(courses),
                    'total_hours': sum(c['duration'] for c in courses) / 60,
                    'utilization_percentage': (sum(c['duration'] for c in courses) / (8 * 60)) * 100  # Assuming 8-hour workday
                } 
                for room, courses in room_usage.items()
            },
            'conflicts': conflicts,
            'workload_issues': workload_issues,
            'generated_at': datetime.now().isoformat()
        }
        
        return report

    def _get_available_slots_for_faculty(self, faculty: FacultyInput) -> List[Tuple[int, int]]:
        """Get available time slots for a faculty member considering their preferred times and current schedule"""
        available_slots = []
        
        for pref_start, pref_end in faculty.available_times:
            # Check each 30-minute slot within the preferred time range
            current_slot = pref_start
            while current_slot < pref_end:
                slot_end = current_slot + 1  # 30-minute slot
                
                # Check if this slot is free (no courses scheduled)
                is_free = True
                for course in self.courses:
                    if course['faculty_name'] == faculty.name:
                        course_start = course['start_time']
                        course_end = course['end_time']
                        
                        # Check if there's an overlap
                        if not (slot_end <= course_start or current_slot >= course_end):
                            is_free = False
                            break
                
                if is_free:
                    available_slots.append((current_slot, slot_end))
                
                current_slot += 1
        
        return available_slots

    def generate_faculty_routine_html(self) -> str:
        """Generate HTML routine showing faculty schedules with preferred time highlights"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Faculty Schedule with Preferred Times</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    text-align: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .faculty-section {{
                    background: white;
                    margin: 20px 0;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .faculty-name {{
                    color: #2c3e50;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                .schedule-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .schedule-table th {{
                    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                    color: white;
                    padding: 15px 8px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 14px;
                }}
                .schedule-table td {{
                    padding: 12px 8px;
                    text-align: center;
                    border: 1px solid #ecf0f1;
                    vertical-align: middle;
                    min-height: 60px;
                    font-size: 12px;
                }}
                .time-slot {{
                    background: #ecf0f1;
                    font-weight: bold;
                    color: #2c3e50;
                    width: 100px;
                }}
                .scheduled-class {{
                    background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 8px;
                }}
                .available-preferred {{
                    background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 8px;
                    border: 2px dashed #d63031;
                }}
                .unavailable {{
                    background: #ddd;
                    color: #7f8c8d;
                }}
                .legend {{
                    margin: 20px 0;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .legend-item {{
                    display: inline-block;
                    margin: 5px 15px;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .legend-scheduled {{
                    background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                    color: white;
                }}
                .legend-available {{
                    background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
                    color: white;
                    border: 2px dashed #d63031;
                }}
                .legend-unavailable {{
                    background: #ddd;
                    color: #7f8c8d;
                }}
                .faculty-info {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    border-left: 4px solid #3498db;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📅 Faculty Schedule with Preferred Time Analysis</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="legend">
                <h3>📊 Legend:</h3>
                <span class="legend-item legend-scheduled">Scheduled Classes</span>
                <span class="legend-item legend-available">Available in Preferred Times</span>
                <span class="legend-item legend-unavailable">Unavailable/Outside Preferences</span>
            </div>
        """
        
        # Generate schedule for each faculty
        time_slots = [(i, i+1) for i in range(0, 24)]  # 30-minute slots from 8 AM to 8 PM
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        
        for faculty in self.faculties:
            available_slots = self._get_available_slots_for_faculty(faculty)
            faculty_courses = [c for c in self.courses if c['faculty_name'] == faculty.name]
            
            html_content += f"""
            <div class="faculty-section">
                <div class="faculty-name">👨‍🏫 {faculty.name}</div>
                <div class="faculty-info">
                    <strong>Department:</strong> {faculty.department} | 
                    <strong>Email:</strong> {faculty.email or 'Not provided'} | 
                    <strong>Max Hours/Week:</strong> {faculty.max_hours_per_week}h<br>
                    <strong>Preferred Times:</strong> {', '.join([f'{self._format_time_slot(s)} - {self._format_time_slot(e)}' for s, e in faculty.available_times]) if faculty.available_times else 'Not specified'}<br>
                    <strong>Available Slots in Preferred Times:</strong> {len(available_slots)} slots
                </div>
                
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            {''.join([f'<th>{day}</th>' for day in days])}
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for time_start, time_end in time_slots:
                if time_start < 0 or time_start > 22:  # Only show 8 AM to 10 PM
                    continue
                    
                html_content += f"""
                        <tr>
                            <td class="time-slot">{self._format_time_slot(time_start)}</td>
                """
                
                for day in days:
                    # Check if faculty has a class at this time
                    scheduled_course = None
                    for course in faculty_courses:
                        if course['start_time'] <= time_start < course['end_time']:
                            scheduled_course = course
                            break
                    
                    if scheduled_course:
                        # Scheduled class
                        html_content += f"""
                            <td class="scheduled-class">
                                {scheduled_course['course_code']}<br>
                                {scheduled_course['course_name']}<br>
                                Room: {scheduled_course['room']}
                            </td>
                        """
                    elif (time_start, time_end) in available_slots:
                        # Available in preferred time
                        html_content += f"""
                            <td class="available-preferred">
                                Available<br>
                                (Preferred Time)
                            </td>
                        """
                    else:
                        # Check if this time is within faculty's preferred times
                        in_preferred = False
                        for pref_start, pref_end in faculty.available_times:
                            if pref_start <= time_start < pref_end:
                                in_preferred = True
                                break
                        
                        if in_preferred:
                            html_content += f"""
                                <td class="unavailable">
                                    Occupied<br>
                                    (Preferred Time)
                                </td>
                            """
                        else:
                            html_content += f"""
                                <td class="unavailable">
                                    Outside<br>
                                    Preferences
                                </td>
                            """
                
                html_content += """
                        </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content

    def save_faculty_routine_html(self, filename: str = None) -> str:
        """Save faculty routine HTML to file and return the filename"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"faculty_routine_{timestamp}.html"
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        try:
            html_content = self.generate_faculty_routine_html()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Faculty routine HTML saved to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving faculty routine HTML: {e}")
            return None

    def generate_enhanced_faculty_schedule(self) -> Dict:
        """Generate enhanced faculty schedule with preferred time analysis"""
        schedule_data = {
            'faculties': [],
            'summary': {
                'total_faculties': len(self.faculties),
                'total_courses': len(self.courses),
                'generated_at': datetime.now().isoformat()
            }
        }
        
        for faculty in self.faculties:
            available_slots = self._get_available_slots_for_faculty(faculty)
            faculty_courses = [c for c in self.courses if c['faculty_name'] == faculty.name]
            
            faculty_schedule = {
                'name': faculty.name,
                'email': faculty.email,
                'department': faculty.department,
                'designation': faculty.designation,
                'preferred_times': [
                    {
                        'start': start,
                        'end': end,
                        'formatted': f"{self._format_time_slot(start)} - {self._format_time_slot(end)}"
                    }
                    for start, end in faculty.available_times
                ],
                'available_slots': [
                    {
                        'start': start,
                        'end': end,
                        'formatted': f"{self._format_time_slot(start)} - {self._format_time_slot(end)}"
                    }
                    for start, end in available_slots
                ],
                'scheduled_courses': faculty_courses,
                'statistics': {
                    'total_courses': len(faculty_courses),
                    'total_hours': sum(course['duration'] for course in faculty_courses) / 60,
                    'available_preferred_slots': len(available_slots),
                    'utilization': (sum(course['duration'] for course in faculty_courses) / 60 / faculty.max_hours_per_week) * 100 if faculty.max_hours_per_week > 0 else 0
                }
            }
            
            schedule_data['faculties'].append(faculty_schedule)
        
        return schedule_data
    def save_faculty_data(self, filename: str = "faculty_data.json") -> bool:
        """Enhanced save with backup and validation"""
        
        filepath = os.path.join(self.data_dir, filename)
        backup_filepath = filepath + ".backup"
        
        try:
            # Create backup if file exists
            if os.path.exists(filepath):
                import shutil
                shutil.copy2(filepath, backup_filepath)
                print(f"📋 Backup created: {backup_filepath}")
            
            data = {
                'version': '2.0',
                'created_at': datetime.now().isoformat(),
                'faculties': [
                    {
                        'name': f.name,
                        'email': f.email,
                        'department': f.department,
                        'designation': f.designation,
                        'phone': f.phone,
                        'specialization': f.specialization,
                        'available_times': f.available_times,
                        'preferred_courses': f.preferred_courses,
                        'max_hours_per_week': f.max_hours_per_week,
                        'room_preferences': f.room_preferences,
                        'unavailable_days': f.unavailable_days
                    }
                    for f in self.faculties
                ],
                'courses': self.courses,
                'summary': {
                    'total_faculties': len(self.faculties),
                    'total_courses': len(self.courses)
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Faculty data saved successfully to {filepath}")
            print(f"   📊 {len(self.faculties)} faculties, {len(self.courses)} courses")
            return True
            
        except Exception as e:
            print(f"❌ Error saving faculty data: {e}")
            return False
    
    def load_faculty_data(self, filename: str = "faculty_data.json") -> bool:
        """Enhanced load with validation and migration"""
        
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ File {filepath} not found")
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Handle version compatibility
            version = data.get('version', '1.0')
            if version == '1.0':
                print("🔄 Migrating from version 1.0...")
                data = self._migrate_from_v1(data)
            
            # Load faculties with enhanced validation
            self.faculties = []
            for f_data in data.get('faculties', []):
                try:
                    faculty = FacultyInput(
                        name=f_data['name'],
                        email=f_data.get('email', ''),
                        department=f_data.get('department', 'CSE'),
                        designation=f_data.get('designation', 'Lecturer'),
                        phone=f_data.get('phone', ''),
                        specialization=f_data.get('specialization', []),
                        available_times=f_data.get('available_times', []),
                        preferred_courses=f_data.get('preferred_courses', []),
                        max_hours_per_week=f_data.get('max_hours_per_week', 18),
                        room_preferences=f_data.get('room_preferences', []),
                        unavailable_days=f_data.get('unavailable_days', [])
                    )
                    self.faculties.append(faculty)
                except Exception as e:
                    print(f"⚠️ Error loading faculty {f_data.get('name', 'Unknown')}: {e}")
            
            self.courses = data.get('courses', [])
            print(f"✅ Faculty data loaded successfully from {filepath}")
            print(f"   📊 {len(self.faculties)} faculties, {len(self.courses)} courses")
            return True
            
        except Exception as e:
            print(f"❌ Error loading faculty data: {e}")
            return False
    
    def _migrate_from_v1(self, data: Dict) -> Dict:
        """Migrate data from version 1.0 to 2.0"""
        migrated_data = {
            'version': '2.0',
            'created_at': datetime.now().isoformat(),
            'faculties': [],
            'courses': data.get('courses', [])
        }
        
        for f_data in data.get('faculties', []):
            migrated_faculty = {
                'name': f_data['name'],
                'email': f_data.get('email', ''),
                'department': f_data.get('department', 'CSE'),
                'designation': 'Lecturer',  # Default for v1 data
                'phone': '',
                'specialization': [],
                'available_times': f_data.get('available_times', []),
                'preferred_courses': f_data.get('preferred_courses', []),
                'max_hours_per_week': f_data.get('max_hours_per_week', 18),
                'room_preferences': f_data.get('room_preferences', []),
                'unavailable_days': []
            }
            migrated_data['faculties'].append(migrated_faculty)
        
        return migrated_data
    
    def export_to_csv(self, filename: str = "faculty_schedule.csv") -> bool:
        """Export schedule to CSV format"""
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header
                writer.writerow([
                    'Faculty Name', 'Course Code', 'Course Name', 'Department',
                    'Start Time', 'End Time', 'Duration (min)', 'Room', 'Credits'
                ])
                
                # Data rows
                for course in self.courses:
                    writer.writerow([
                        course['faculty_name'],
                        course['course_code'],
                        course['course_name'],
                        course['department'],
                        self._format_time_slot(course['start_time']),
                        self._format_time_slot(course['end_time']),
                        course['duration'],
                        course['room'],
                        course['credits']
                    ])
            
            print(f"✅ Schedule exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return False
    def interactive_course_assignment(self) -> bool:
        """Enhanced interactive course assignment"""
        
        if not self.faculties:
            print("❌ No faculties added yet. Please add faculties first.")
            return False
        
        print("\n" + "="*70)
        print("📚 ENHANCED COURSE ASSIGNMENT SYSTEM")
        print("="*70)
        
        # Show faculty list with current workload
        print("\n👥 Available Faculties:")
        for i, faculty in enumerate(self.faculties, 1):
            faculty_courses = [c for c in self.courses if c['faculty_name'] == faculty.name]
            current_hours = sum(course['duration'] for course in faculty_courses) / 60
            utilization = (current_hours / faculty.max_hours_per_week) * 100
            
            status = "🟢" if utilization < 70 else "🟡" if utilization < 90 else "🔴"
            print(f"  {i:2d}. {status} {faculty.name} ({faculty.department})")
            print(f"      📊 {current_hours:.1f}h/{faculty.max_hours_per_week}h ({utilization:.1f}%)")
            if faculty.specialization:
                print(f"      🎯 Specialization: {', '.join(faculty.specialization)}")
        
        success_count = 0
        while True:
            print("\n" + "-"*50)
            faculty_choice = input("Select faculty number or 'done' to finish: ").strip()
            
            if faculty_choice.lower() == 'done':
                break
            
            try:
                faculty_idx = int(faculty_choice) - 1
                if 0 <= faculty_idx < len(self.faculties):
                    faculty = self.faculties[faculty_idx]
                    
                    if self._assign_course_to_faculty(faculty):
                        success_count += 1
                else:
                    print("❌ Invalid faculty number")
            except ValueError:
                print("❌ Please enter a valid number")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Course assignment interrupted")
                break
        
        print(f"\n✅ Successfully assigned {success_count} courses")
        return success_count > 0
    
    def _assign_course_to_faculty(self, faculty: FacultyInput) -> bool:
        """Assign a single course to a faculty member"""
        
        print(f"\n👨‍🏫 Assigning course to: {faculty.name}")
        print(f"   📅 Available time slots: {len(faculty.available_times)}")
        print(f"   🎯 Preferred courses: {', '.join(faculty.preferred_courses) if faculty.preferred_courses else 'None specified'}")
        
        # Course code input with validation
        while True:
            course_code = input("📖 Enter course code (e.g., CSE101): ").strip().upper()
            if not course_code:
                print("  ❌ Course code cannot be empty")
                continue
            
            # Check for duplicate
            existing = any(c['course_code'] == course_code for c in self.courses)
            if existing:
                print(f"  ⚠️ Course {course_code} already exists!")
                overwrite = input("  Do you want to assign it to another faculty? (y/n): ").lower() == 'y'
                if not overwrite:
                    continue
            break
        
        course_name = input("� Enter course name: ").strip()
        if not course_name:
            course_name = f"Course {course_code}"
        
        # Credits input with validation
        while True:
            credits_input = input("💳 Enter credit hours (0.5-6.0, default: 3.0): ").strip()
            if not credits_input:
                credits = 3.0
                break
            try:
                credits = float(credits_input)
                if 0.5 <= credits <= 6.0:
                    break
                else:
                    print("  ❌ Credits must be between 0.5 and 6.0")
            except ValueError:
                print("  ❌ Please enter a valid number")
        
        # Duration input with validation
        while True:
            duration_input = input("⏱️ Enter duration in minutes (30-180, default: 90): ").strip()
            if not duration_input:
                duration = 90
                break
            try:
                duration = int(duration_input)
                if 30 <= duration <= 180:
                    break
                else:
                    print("  ❌ Duration must be between 30 and 180 minutes")
            except ValueError:
                print("  ❌ Please enter a valid number")
        
        # Attempt to assign the course
        result = self.add_course_for_faculty(faculty.name, course_code, course_name, credits, duration)
        
        if result:
            # Show updated faculty workload
            faculty_courses = [c for c in self.courses if c['faculty_name'] == faculty.name]
            total_hours = sum(course['duration'] for course in faculty_courses) / 60
            utilization = (total_hours / faculty.max_hours_per_week) * 100
            
            print(f"   📊 Updated workload: {total_hours:.1f}h/{faculty.max_hours_per_week}h ({utilization:.1f}%)")
            
            if utilization > 100:
                print("   ⚠️ WARNING: Faculty is now overloaded!")
            elif utilization > 90:
                print("   ⚠️ WARNING: Faculty workload is very high!")
            
            return True
        
        return False
    
    def print_enhanced_schedule_summary(self):
        """Enhanced schedule summary with analytics"""
        
        if not self.courses:
            print("❌ No courses scheduled yet.")
            return
        
        print("\n" + "="*90)
        print("📋 ENHANCED FACULTY SCHEDULE SUMMARY")
        print("="*90)
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report()
        
        # Print faculty details
        for faculty in self.faculties:
            faculty_analysis = report['faculty_analysis'].get(faculty.name, {})
            
            print(f"\n👨‍🏫 {faculty.name} ({faculty.designation})")
            print(f"   📧 {faculty.email} | 📱 {faculty.phone}")
            print(f"   � {faculty.department} Department")
            if faculty.specialization:
                print(f"   🎯 Specialization: {', '.join(faculty.specialization)}")
            
            print("-" * 70)
            
            faculty_courses = faculty_analysis.get('courses', [])
            if faculty_courses:
                for course in faculty_courses:
                    start_time = self._format_time_slot(course['start_time'])
                    end_time = self._format_time_slot(course['end_time'])
                    print(f"  📖 {course['course_code']}: {course['course_name']}")
                    print(f"     ⏰ {start_time} - {end_time} | 🏠 {course['room']} | 💳 {course['credits']} credits")
                
                total_hours = faculty_analysis.get('total_hours', 0)
                utilization = faculty_analysis.get('utilization', 0)
                available_hours = faculty_analysis.get('available_hours', 0)
                
                status = "🟢 Good" if utilization < 70 else "🟡 High" if utilization < 90 else "🔴 Overloaded"
                print(f"     📊 Workload: {total_hours:.1f}h/{faculty.max_hours_per_week}h ({utilization:.1f}%) {status}")
                print(f"     � Available: {available_hours:.1f}h/week")
            else:
                print("     📝 No courses assigned")
        
        # Print summary statistics
        summary = report['summary']
        print(f"\n📊 SUMMARY STATISTICS")
        print("="*50)
        print(f"👥 Total Faculties: {summary['total_faculties']}")
        print(f"📚 Total Courses: {summary['total_courses']}")
        print(f"🏠 Rooms Used: {summary['total_rooms_used']}")
        print(f"⚠️ Conflicts: {summary['conflicts_detected']}")
        print(f"⚡ Workload Issues: {summary['workload_issues']}")
        
        # Print conflicts if any
        if report['conflicts']:
            print(f"\n⚠️ CONFLICTS DETECTED")
            print("-" * 30)
            for conflict in report['conflicts']:
                print(f"❌ {conflict['description']}")
        
        # Print workload issues if any
        if report['workload_issues']:
            print(f"\n⚡ WORKLOAD ISSUES")
            print("-" * 25)
            for issue in report['workload_issues']:
                print(f"⚠️ {issue['description']}")
        
        # Print room utilization
        print(f"\n🏠 ROOM UTILIZATION")
        print("-" * 25)
        for room, util in report['room_utilization'].items():
            if not room.startswith('TBD'):
                print(f"   {room}: {util['courses_scheduled']} courses, {util['total_hours']:.1f}h ({util['utilization_percentage']:.1f}%)")
    
    def _format_time_slot(self, slot: int) -> str:
        """Enhanced time formatting"""
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


# Maintain backward compatibility
FacultyInputSystem = EnhancedFacultyInputSystem


def main():
    """Enhanced main function for faculty input system"""
    
    system = EnhancedFacultyInputSystem()
    
    while True:
        print("\n" + "="*70)
        print("🎓 ENHANCED FACULTY INPUT SYSTEM - MAIN MENU")
        print("="*70)
        print("1. 👨‍🏫 Add Faculty Member")
        print("2. 📚 Assign Courses to Faculty")  
        print("3. 📋 View Enhanced Schedule Summary")
        print("4. 💾 Save Faculty Data")
        print("5. 📂 Load Faculty Data")
        print("6. 📊 Generate Comprehensive Report")
        print("7. 📤 Export to CSV")
        print("8. 🔍 Detect Conflicts")
        print("9. 👋 Exit")
        
        choice = input("\nSelect option (1-9): ").strip()
        
        try:
            if choice == '1':
                system.add_faculty_interactive()
            elif choice == '2':
                system.interactive_course_assignment()
            elif choice == '3':
                system.print_enhanced_schedule_summary()
            elif choice == '4':
                system.save_faculty_data()
            elif choice == '5':
                system.load_faculty_data()
            elif choice == '6':
                report = system.generate_comprehensive_report()
                print(f"\n� Comprehensive Report Generated")
                print(f"Conflicts: {len(report['conflicts'])}, Workload Issues: {len(report['workload_issues'])}")
            elif choice == '7':
                system.export_to_csv()
            elif choice == '8':
                conflicts = system.conflict_detector.detect_faculty_conflicts(system.courses)
                workload_issues = system.conflict_detector.detect_workload_issues(system.faculties, system.courses)
                print(f"\n🔍 Conflict Detection Results:")
                print(f"   ⚠️ Schedule Conflicts: {len(conflicts)}")
                print(f"   ⚡ Workload Issues: {len(workload_issues)}")
                for conflict in conflicts:
                    print(f"   ❌ {conflict['description']}")
                for issue in workload_issues:
                    print(f"   ⚠️ {issue['description']}")
            elif choice == '9':
                print("�👋 Thank you for using Enhanced Faculty Input System!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
                
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
