#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Routine Generator for Conflict-Free Scheduling System

This module provides advanced routine generation capabilities with
faculty constraints, room optimization, and comprehensive scheduling.
"""

from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, time
import random
from collections import defaultdict


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0
    name: str = ""
    room: str = ""


@dataclass
class Course:
    """Enhanced course representation"""
    id: int
    course_code: str
    course_title: str
    credit_hours: float
    session_duration: int  # minutes
    sessions_per_week: int
    batch_code: str
    teacher_code: str
    class_type: str  # THEORY, LAB
    prerequisite_ids: List[int] = None


@dataclass
class TimeSlot:
    """Time slot representation"""
    id: int
    day: str
    start_time: time
    end_time: time
    duration: int  # minutes


@dataclass
class Room:
    """Room representation"""
    id: int
    room_code: str
    capacity: int
    room_type: str  # THEORY, LAB, BOTH
    building: str


@dataclass
class Teacher:
    """Teacher representation"""
    id: int
    teacher_code: str
    full_name: str
    department: str
    external_faculty: bool = False
    max_hours_per_day: int = 6
    max_hours_per_week: int = 30
    availability_start: time = time(8, 30)
    availability_end: time = time(17, 30)


class EnhancedRoutineGenerator:
    """Enhanced routine generator with advanced scheduling capabilities"""
    
    def __init__(self, database_manager=None):
        """
        Initialize the enhanced routine generator
        
        Args:
            database_manager: Optional database manager for data loading
        """
        self.database_manager = database_manager
        self.prioritize_external_faculty = True
        self.minimize_gaps = True
        self.balance_room_usage = True
        self.max_tries_per_course = 50
        
        # Data containers
        self.all_courses: List[Course] = []
        self.all_time_slots: List[TimeSlot] = []
        self.all_rooms: List[Room] = []
        self.all_teachers: List[Teacher] = []
        
        # Scheduling state
        self.scheduled_activities: List[Activity] = []
        self.room_schedule: Dict[str, List[Activity]] = defaultdict(list)
        self.teacher_schedule: Dict[str, List[Activity]] = defaultdict(list)
        
        print("🎓 Enhanced Routine Generator initialized")
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        print("📚 Loading sample data...")
        
        # Sample time slots (Monday to Friday, 8:30 AM to 5:30 PM)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        slot_id = 1
        
        for day in days:
            for hour in range(8, 18):  # 8 AM to 5 PM
                for minute in [30] if hour == 8 else [0, 30]:
                    if hour == 17 and minute == 30:  # Don't go past 5:30 PM
                        break
                    
                    start_time = time(hour, minute)
                    end_time = time(hour + 1, minute) if minute == 0 else time(hour + 1, 0)
                    
                    time_slot = TimeSlot(
                        id=slot_id,
                        day=day,
                        start_time=start_time,
                        end_time=end_time,
                        duration=90  # 1.5 hours
                    )
                    self.all_time_slots.append(time_slot)
                    slot_id += 1
        
        # Sample rooms
        self.all_rooms = [
            Room(1, "CSE-101", 40, "THEORY", "CSE Building"),
            Room(2, "CSE-102", 40, "THEORY", "CSE Building"),
            Room(3, "CSE-201", 35, "LAB", "CSE Building"),
            Room(4, "CSE-202", 35, "LAB", "CSE Building"),
            Room(5, "CSE-301", 50, "BOTH", "CSE Building"),
        ]
        
        # Sample teachers
        self.all_teachers = [
            Teacher(1, "CSE001", "Dr. Ahmed Rahman", "CSE", False, 6, 30),
            Teacher(2, "CSE002", "Dr. Fatima Khan", "CSE", False, 6, 30),
            Teacher(3, "CSE003", "Mr. Karim Hossain", "CSE", False, 6, 30),
            Teacher(4, "CSE004", "Ms. Rashida Begum", "CSE", True, 4, 20),  # External faculty
            Teacher(5, "CSE005", "Dr. Mohammad Ali", "CSE", False, 6, 30),
        ]
        
        # Sample courses
        self.all_courses = [
            Course(1, "CSE101", "Programming Fundamentals", 3.0, 90, 2, "BCSE25", "CSE001", "THEORY"),
            Course(2, "CSE102", "Programming Lab", 1.0, 90, 1, "BCSE25", "CSE001", "LAB"),
            Course(3, "CSE201", "Data Structures", 3.0, 90, 2, "BCSE24", "CSE002", "THEORY"),
            Course(4, "CSE202", "Data Structures Lab", 1.0, 90, 1, "BCSE24", "CSE002", "LAB"),
            Course(5, "CSE301", "Algorithms", 3.0, 90, 2, "BCSE23", "CSE003", "THEORY"),
            Course(6, "CSE401", "Software Engineering", 3.0, 90, 2, "BCSE22", "CSE004", "THEORY"),
            Course(7, "CSE402", "Database Systems", 3.0, 90, 2, "BCSE22", "CSE005", "THEORY"),
            Course(8, "CSE403", "Database Lab", 1.0, 90, 1, "BCSE22", "CSE005", "LAB"),
        ]
        
        print(f"   📚 Courses loaded: {len(self.all_courses)}")
        print(f"   ⏰ Time slots: {len(self.all_time_slots)}")
        print(f"   🏢 Rooms: {len(self.all_rooms)}")
        print(f"   👥 Teachers: {len(self.all_teachers)}")
    
    def generate_comprehensive_routine(self) -> List[Activity]:
        """
        Generate a comprehensive routine using advanced algorithms
        
        Returns:
            List of scheduled activities
        """
        print("🚀 Generating comprehensive routine...")
        
        if not self.all_courses:
            self.load_sample_data()
        
        # Clear previous scheduling state
        self.scheduled_activities.clear()
        self.room_schedule.clear()
        self.teacher_schedule.clear()
        
        # Sort courses by priority (external faculty first, then by credit hours)
        sorted_courses = self._prioritize_courses()
        
        scheduled_count = 0
        failed_count = 0
        
        for course in sorted_courses:
            print(f"🔄 Scheduling {course.course_code}: {course.course_title}")
            
            success = self._schedule_course(course)
            
            if success:
                scheduled_count += 1
                print(f"   ✅ Scheduled successfully")
            else:
                failed_count += 1
                print(f"   ❌ Failed to schedule")
        
        print(f"\n📊 Scheduling Results:")
        print(f"   ✅ Successfully scheduled: {scheduled_count}")
        print(f"   ❌ Failed to schedule: {failed_count}")
        print(f"   📈 Success rate: {(scheduled_count / len(sorted_courses)) * 100:.1f}%")
        
        return self.scheduled_activities
    
    def _prioritize_courses(self) -> List[Course]:
        """Prioritize courses for scheduling"""
        def priority_key(course):
            # Priority factors:
            # 1. External faculty courses first
            # 2. Higher credit hours
            # 3. Lab courses after theory courses
            teacher = next((t for t in self.all_teachers if t.teacher_code == course.teacher_code), None)
            external_priority = 0 if teacher and teacher.external_faculty else 1
            credit_priority = -course.credit_hours  # Negative for descending order
            type_priority = 0 if course.class_type == "THEORY" else 1
            
            return (external_priority, credit_priority, type_priority)
        
        return sorted(self.all_courses, key=priority_key)
    
    def _schedule_course(self, course: Course) -> bool:
        """
        Attempt to schedule a single course
        
        Args:
            course: Course to schedule
            
        Returns:
            True if successfully scheduled, False otherwise
        """
        # Find suitable time slots for this course
        suitable_slots = self._find_suitable_time_slots(course)
        
        if not suitable_slots:
            return False
        
        # Find suitable rooms
        suitable_rooms = self._find_suitable_rooms(course)
        
        if not suitable_rooms:
            return False
        
        # Try to schedule for the required number of sessions per week
        sessions_scheduled = 0
        attempts = 0
        
        while sessions_scheduled < course.sessions_per_week and attempts < self.max_tries_per_course:
            attempts += 1
            
            # Try each time slot
            for time_slot in suitable_slots:
                if sessions_scheduled >= course.sessions_per_week:
                    break
                
                # Try each room
                for room in suitable_rooms:
                    if self._can_schedule_at_slot(course, time_slot, room):
                        # Create activity
                        activity = Activity(
                            id=len(self.scheduled_activities) + 1,
                            start=time_slot.id,
                            end=time_slot.id + 1,  # Single time slot
                            weight=course.credit_hours,
                            name=f"{course.course_code}: {course.course_title}",
                            room=room.room_code
                        )
                        
                        # Add to schedules
                        self.scheduled_activities.append(activity)
                        self.room_schedule[room.room_code].append(activity)
                        self.teacher_schedule[course.teacher_code].append(activity)
                        
                        sessions_scheduled += 1
                        break
        
        return sessions_scheduled > 0
    
    def _find_suitable_time_slots(self, course: Course) -> List[TimeSlot]:
        """Find time slots suitable for the course"""
        teacher = next((t for t in self.all_teachers if t.teacher_code == course.teacher_code), None)
        
        if not teacher:
            return self.all_time_slots
        
        suitable_slots = []
        
        for slot in self.all_time_slots:
            # Check teacher availability
            if (slot.start_time >= teacher.availability_start and 
                slot.end_time <= teacher.availability_end):
                suitable_slots.append(slot)
        
        return suitable_slots
    
    def _find_suitable_rooms(self, course: Course) -> List[Room]:
        """Find rooms suitable for the course"""
        suitable_rooms = []
        
        for room in self.all_rooms:
            # Check room type compatibility
            if (room.room_type == "BOTH" or 
                room.room_type == course.class_type):
                suitable_rooms.append(room)
        
        return suitable_rooms
    
    def _can_schedule_at_slot(self, course: Course, time_slot: TimeSlot, room: Room) -> bool:
        """Check if course can be scheduled at specific time slot and room"""
        
        # Check room availability
        for activity in self.room_schedule[room.room_code]:
            if activity.start == time_slot.id:  # Same time slot
                return False
        
        # Check teacher availability
        for activity in self.teacher_schedule[course.teacher_code]:
            if activity.start == time_slot.id:  # Same time slot
                return False
        
        return True
    
    def get_schedule_by_batch(self, batch_code: str) -> List[Activity]:
        """Get schedule for a specific batch"""
        batch_activities = []
        
        for activity in self.scheduled_activities:
            # Find the course for this activity
            course = next((c for c in self.all_courses 
                          if f"{c.course_code}: {c.course_title}" == activity.name), None)
            
            if course and course.batch_code == batch_code:
                batch_activities.append(activity)
        
        return batch_activities
    
    def get_teacher_schedule(self, teacher_code: str) -> List[Activity]:
        """Get schedule for a specific teacher"""
        return self.teacher_schedule.get(teacher_code, [])
    
    def get_room_utilization(self) -> Dict[str, float]:
        """Calculate room utilization percentages"""
        utilization = {}
        total_slots = len(self.all_time_slots)
        
        for room in self.all_rooms:
            used_slots = len(self.room_schedule[room.room_code])
            utilization[room.room_code] = (used_slots / total_slots) * 100
        
        return utilization
    
    def print_schedule_summary(self):
        """Print a summary of the generated schedule"""
        print("\n=== Schedule Summary ===")
        print(f"Total activities scheduled: {len(self.scheduled_activities)}")
        
        # Batch-wise summary
        batch_counts = defaultdict(int)
        for activity in self.scheduled_activities:
            course = next((c for c in self.all_courses 
                          if f"{c.course_code}: {c.course_title}" == activity.name), None)
            if course:
                batch_counts[course.batch_code] += 1
        
        print("\nBatch-wise distribution:")
        for batch, count in batch_counts.items():
            print(f"  {batch}: {count} activities")
        
        # Room utilization
        utilization = self.get_room_utilization()
        print("\nRoom utilization:")
        for room_code, util in utilization.items():
            print(f"  {room_code}: {util:.1f}%")


# Example usage
if __name__ == "__main__":
    generator = EnhancedRoutineGenerator()
    schedule = generator.generate_comprehensive_routine()
    generator.print_schedule_summary()
    
    print(f"\n✅ Generated {len(schedule)} scheduled activities")
