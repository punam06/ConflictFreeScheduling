#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Manager for Conflict-Free Scheduling System

This module provides a comprehensive interface for database operations
using SQLAlchemy for production-ready scheduling system.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Time, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime, time
import os


Base = declarative_base()


class BatchStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    GRADUATED = "GRADUATED"


class TeacherStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ON_LEAVE = "ON_LEAVE"


class RoomType(enum.Enum):
    THEORY = "THEORY"
    LAB = "LAB"
    BOTH = "BOTH"


class RoomStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    MAINTENANCE = "MAINTENANCE"
    UNAVAILABLE = "UNAVAILABLE"


class ClassType(enum.Enum):
    THEORY = "THEORY"
    LAB = "LAB"


class CourseStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


# Database Models
class Batch(Base):
    __tablename__ = 'batches'
    
    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    batch_code = Column(String(20), unique=True, nullable=False)
    batch_name = Column(String(100), nullable=False)
    year_level = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    total_sections = Column(Integer, default=2)
    status = Column(Enum(BatchStatus), default=BatchStatus.ACTIVE)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    courses = relationship("Course", back_populates="batch")


class Teacher(Base):
    __tablename__ = 'teachers'
    
    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    designation = Column(String(50))
    department = Column(String(50), default='CSE')
    email = Column(String(100))
    phone = Column(String(20))
    availability_start = Column(Time, default=time(8, 30))
    availability_end = Column(Time, default=time(17, 30))
    external_faculty = Column(Boolean, default=False)
    max_hours_per_day = Column(Integer, default=6)
    max_hours_per_week = Column(Integer, default=30)
    preferred_time_slot = Column(String(20), default='ANY')
    status = Column(Enum(TeacherStatus), default=TeacherStatus.ACTIVE)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    courses = relationship("Course", back_populates="teacher")


class Classroom(Base):
    __tablename__ = 'classrooms'
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String(20), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    room_type = Column(Enum(RoomType), default=RoomType.THEORY)
    building = Column(String(50))
    floor_number = Column(Integer)
    facilities = Column(Text)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(15), unique=True, nullable=False)
    course_title = Column(String(100), nullable=False)
    credit_hours = Column(Float, nullable=False, default=3.0)
    class_type = Column(Enum(ClassType), nullable=False, default=ClassType.THEORY)
    session_duration = Column(Integer, nullable=False, default=90)  # Duration in minutes
    sessions_per_week = Column(Integer, nullable=False, default=2)
    batch_id = Column(Integer, ForeignKey('batches.batch_id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=True)
    description = Column(Text)
    department = Column(String(50), default='CSE')
    status = Column(Enum(CourseStatus), default=CourseStatus.ACTIVE)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    batch = relationship("Batch", back_populates="courses")
    teacher = relationship("Teacher", back_populates="courses")
    prerequisite = relationship("Course", remote_side=[course_id])


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0
    name: str = ""
    room: str = ""
    faculty: str = ""  # Faculty name
    course_code: str = ""  # Course code


class DatabaseManager:
    """Database Manager for Conflict-Free Scheduling System"""
    
    def __init__(self, 
                 host: str = "localhost",
                 database: str = "conflict_free_scheduling",
                 user: str = "root",
                 password: str = "",
                 port: int = 3306):
        """
        Initialize database connection parameters
        
        Args:
            host: MySQL host (default: localhost)
            database: Database name (default: conflict_free_scheduling)
            user: Username (default: root)
            password: Password (default: empty)
            port: Port number (default: 3306)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.engine = None
        self.Session = None
        self.is_connected = False
        
        # Construct database URL
        if password:
            self.database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        else:
            self.database_url = f"mysql+pymysql://{user}@{host}:{port}/{database}"
    
    def initialize(self) -> bool:
        """Initialize database connection and create tables"""
        try:
            # Create engine
            self.engine = create_engine(self.database_url, echo=False)
            
            # Create all tables
            Base.metadata.create_all(self.engine)
            
            # Create session factory
            self.Session = sessionmaker(bind=self.engine)
            
            self.is_connected = True
            print(f"✅ Database initialized successfully: {self.database}")
            return True
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            self.is_connected = False
            return False
    
    def connect(self) -> bool:
        """Connect to database without creating tables"""
        try:
            self.engine = create_engine(self.database_url, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            self.is_connected = True
            print(f"✅ Connected to database: {self.database}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            self.is_connected = False
            return False
    
    def initialize_with_realistic_data(self) -> bool:
        """
        Initialize database with realistic CSE department data
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.connect():
                return False
            
            session = self.Session()
            
            # Check if data already exists
            existing_batches = session.query(Batch).count()
            if existing_batches > 0:
                print("📊 Realistic data already exists")
                session.close()
                return True
            
            print("🔄 Creating realistic CSE department data...")
            
            # 1. Create Batches
            batches_data = [
                {"batch_code": "BCSE24", "batch_name": "B.Sc. in CSE Batch 24", "year_level": 1, "semester": 2},
                {"batch_code": "BCSE23", "batch_name": "B.Sc. in CSE Batch 23", "year_level": 2, "semester": 4},
                {"batch_code": "BCSE22", "batch_name": "B.Sc. in CSE Batch 22", "year_level": 3, "semester": 6},
                {"batch_code": "BCSE21", "batch_name": "B.Sc. in CSE Batch 21", "year_level": 4, "semester": 8}
            ]
            
            batches = []
            for batch_data in batches_data:
                batch = Batch(**batch_data)
                session.add(batch)
                batches.append(batch)
            
            session.flush()  # Get IDs
            
            # 2. Create Real Faculty Members
            faculty_data = [
                {"teacher_code": "NAK001", "full_name": "Nazneen Akter", "designation": "Assistant Professor", "department": "CSE"},
                {"teacher_code": "SZ002", "full_name": "Sobhana Zahan", "designation": "Associate Professor", "department": "CSE"},
                {"teacher_code": "TTS003", "full_name": "Tahmid Tarmin Sukhi", "designation": "Assistant Professor", "department": "CSE"},
                {"teacher_code": "II004", "full_name": "Iyolita Islam", "designation": "Assistant Professor", "department": "CSE"},
                {"teacher_code": "SAS005", "full_name": "Sayma Alam Suha", "designation": "Lecturer", "department": "CSE"},
                {"teacher_code": "SR006", "full_name": "Selim Reja", "designation": "Assistant Professor", "department": "CSE"},
                {"teacher_code": "RA007", "full_name": "Rumana Akter", "designation": "Associate Professor", "department": "CSE"}
            ]
            
            teachers = []
            for faculty in faculty_data:
                teacher = Teacher(**faculty)
                session.add(teacher)
                teachers.append(teacher)
            
            session.flush()  # Get IDs
            
            # 3. Create Realistic Classrooms (provided rooms)
            classroom_data = [
                {"room_code": "302", "capacity": 40, "room_type": RoomType.THEORY, "building": "Academic Building", "floor_number": 3},
                {"room_code": "303", "capacity": 40, "room_type": RoomType.THEORY, "building": "Academic Building", "floor_number": 3},
                {"room_code": "304", "capacity": 35, "room_type": RoomType.THEORY, "building": "Academic Building", "floor_number": 3},
                {"room_code": "504", "capacity": 45, "room_type": RoomType.THEORY, "building": "Academic Building", "floor_number": 5},
                {"room_code": "1003", "capacity": 30, "room_type": RoomType.LAB, "building": "Academic Building", "floor_number": 10}
            ]
            
            classrooms = []
            for room_data in classroom_data:
                classroom = Classroom(**room_data)
                session.add(classroom)
                classrooms.append(classroom)
            
            session.flush()  # Get IDs
            
            # 4. Create Realistic Courses with proper time slots
            courses_data = [
                # BCSE24 (1st Year, 2nd Semester) courses
                {"course_code": "CSE111", "course_title": "Computer Programming", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[0].batch_id, "teacher_id": teachers[0].teacher_id},
                {"course_code": "CSE112", "course_title": "Computer Programming Lab", "credit_hours": 1.5, "class_type": ClassType.LAB, "session_duration": 120, "batch_id": batches[0].batch_id, "teacher_id": teachers[1].teacher_id},
                {"course_code": "CSE121", "course_title": "Discrete Mathematics", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[0].batch_id, "teacher_id": teachers[2].teacher_id},
                {"course_code": "MAT102", "course_title": "Calculus II", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[0].batch_id, "teacher_id": teachers[3].teacher_id},
                {"course_code": "PHY102", "course_title": "Physics II", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[0].batch_id, "teacher_id": teachers[4].teacher_id},
                
                # BCSE23 (2nd Year, 4th Semester) courses
                {"course_code": "CSE213", "course_title": "Data Structures and Algorithms", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[1].batch_id, "teacher_id": teachers[5].teacher_id},
                {"course_code": "CSE214", "course_title": "Data Structures Lab", "credit_hours": 1.5, "class_type": ClassType.LAB, "session_duration": 120, "batch_id": batches[1].batch_id, "teacher_id": teachers[6].teacher_id},
                {"course_code": "CSE221", "course_title": "Database Management Systems", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[1].batch_id, "teacher_id": teachers[0].teacher_id},
                {"course_code": "CSE222", "course_title": "Database Lab", "credit_hours": 1.5, "class_type": ClassType.LAB, "session_duration": 120, "batch_id": batches[1].batch_id, "teacher_id": teachers[1].teacher_id},
                {"course_code": "CSE231", "course_title": "Computer Organization", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[1].batch_id, "teacher_id": teachers[2].teacher_id},
                
                # BCSE22 (3rd Year, 6th Semester) courses
                {"course_code": "CSE313", "course_title": "Software Engineering", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[2].batch_id, "teacher_id": teachers[3].teacher_id},
                {"course_code": "CSE321", "course_title": "Computer Networks", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[2].batch_id, "teacher_id": teachers[4].teacher_id},
                {"course_code": "CSE322", "course_title": "Network Lab", "credit_hours": 1.5, "class_type": ClassType.LAB, "session_duration": 120, "batch_id": batches[2].batch_id, "teacher_id": teachers[5].teacher_id},
                {"course_code": "CSE331", "course_title": "Operating Systems", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[2].batch_id, "teacher_id": teachers[6].teacher_id},
                
                # BCSE21 (4th Year, 8th Semester) courses
                {"course_code": "CSE411", "course_title": "Artificial Intelligence", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[3].batch_id, "teacher_id": teachers[0].teacher_id},
                {"course_code": "CSE421", "course_title": "Machine Learning", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[3].batch_id, "teacher_id": teachers[1].teacher_id},
                {"course_code": "CSE431", "course_title": "Distributed Systems", "credit_hours": 3.0, "class_type": ClassType.THEORY, "session_duration": 90, "batch_id": batches[3].batch_id, "teacher_id": teachers[2].teacher_id}
            ]
            
            courses = []
            for course_data in courses_data:
                course = Course(**course_data)
                session.add(course)
                courses.append(course)
            
            session.commit()
            session.close()
            
            print("✅ Realistic CSE department data created successfully!")
            print(f"   📚 Created {len(batches)} batches")
            print(f"   👨‍🏫 Created {len(teachers)} faculty members")
            print(f"   🏫 Created {len(classrooms)} classrooms")
            print(f"   📖 Created {len(courses)} courses")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize realistic data: {e}")
            if 'session' in locals():
                session.rollback()
                session.close()
            return False
        """Initialize database with sample data"""
        if not self.initialize():
            return False
        
        return self.load_sample_data()
    
    def load_sample_data(self) -> bool:
        """Load sample data into database"""
        if not self.is_connected:
            return False
        
        try:
            session = self.Session()
            
            # Check if data already exists
            if session.query(Batch).count() > 0:
                print("📊 Sample data already exists")
                session.close()
                return True
            
            # Sample Batches
            batches = [
                Batch(batch_code="BCSE22", batch_name="Bachelor of CSE 2022", year_level=4, semester=8),
                Batch(batch_code="BCSE23", batch_name="Bachelor of CSE 2023", year_level=3, semester=6),
                Batch(batch_code="BCSE24", batch_name="Bachelor of CSE 2024", year_level=2, semester=4),
                Batch(batch_code="BCSE25", batch_name="Bachelor of CSE 2025", year_level=1, semester=2),
            ]
            
            # Sample Teachers
            teachers = [
                Teacher(teacher_code="CSE001", full_name="Dr. Ahmed Rahman", designation="Professor", email="ahmed@bup.edu.bd"),
                Teacher(teacher_code="CSE002", full_name="Dr. Fatima Khan", designation="Associate Professor", email="fatima@bup.edu.bd"),
                Teacher(teacher_code="CSE003", full_name="Mr. Karim Hossain", designation="Assistant Professor", email="karim@bup.edu.bd"),
                Teacher(teacher_code="CSE004", full_name="Ms. Rashida Begum", designation="Lecturer", email="rashida@bup.edu.bd"),
                Teacher(teacher_code="CSE005", full_name="Dr. Mohammad Ali", designation="Professor", email="ali@bup.edu.bd"),
            ]
            
            # Sample Classrooms
            classrooms = [
                Classroom(room_code="CSE-101", capacity=40, room_type=RoomType.THEORY, building="CSE Building", floor_number=1),
                Classroom(room_code="CSE-102", capacity=40, room_type=RoomType.THEORY, building="CSE Building", floor_number=1),
                Classroom(room_code="CSE-201", capacity=35, room_type=RoomType.LAB, building="CSE Building", floor_number=2),
                Classroom(room_code="CSE-202", capacity=35, room_type=RoomType.LAB, building="CSE Building", floor_number=2),
                Classroom(room_code="CSE-301", capacity=50, room_type=RoomType.BOTH, building="CSE Building", floor_number=3),
            ]
            
            # Add all to session
            session.add_all(batches)
            session.add_all(teachers)
            session.add_all(classrooms)
            session.commit()
            
            # Sample Courses (need to get IDs after commit)
            courses = [
                Course(course_code="CSE101", course_title="Programming Fundamentals", credit_hours=3.0, 
                      batch_id=4, teacher_id=1, class_type=ClassType.THEORY),
                Course(course_code="CSE102", course_title="Programming Lab", credit_hours=1.0, 
                      batch_id=4, teacher_id=1, class_type=ClassType.LAB),
                Course(course_code="CSE201", course_title="Data Structures", credit_hours=3.0, 
                      batch_id=3, teacher_id=2, class_type=ClassType.THEORY),
                Course(course_code="CSE202", course_title="Data Structures Lab", credit_hours=1.0, 
                      batch_id=3, teacher_id=2, class_type=ClassType.LAB),
                Course(course_code="CSE301", course_title="Algorithms", credit_hours=3.0, 
                      batch_id=2, teacher_id=3, class_type=ClassType.THEORY),
                Course(course_code="CSE401", course_title="Software Engineering", credit_hours=3.0, 
                      batch_id=1, teacher_id=4, class_type=ClassType.THEORY),
            ]
            
            session.add_all(courses)
            session.commit()
            session.close()
            
            print("✅ Sample data loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load sample data: {e}")
            if session:
                session.rollback()
                session.close()
            return False
    
    def get_all_courses(self) -> List[Activity]:
        """Get all courses as Activity objects"""
        if not self.is_connected:
            return []
        
        try:
            session = self.Session()
            courses = session.query(Course).all()
            
            activities = []
            for course in courses:
                # Convert to Activity (using course_id as activity id)
                # For simplicity, use session_duration as time slots
                activity = Activity(
                    id=course.course_id,
                    start=0,  # Will be set by scheduling algorithm
                    end=course.session_duration,  # Duration in minutes
                    weight=course.credit_hours,
                    name=course.course_title,
                    room="",  # Will be assigned by scheduling algorithm
                    faculty=course.instructor_name if hasattr(course, 'instructor_name') else "TBA",
                    course_code=course.course_code if hasattr(course, 'course_code') else f"CSE{course.course_id:03d}"
                )
                activities.append(activity)
            
            session.close()
            return activities
            
        except Exception as e:
            print(f"❌ Failed to get courses: {e}")
            return []
    
    def get_courses_with_titles(self) -> Tuple[List[Activity], List[str]]:
        """Get all courses with their titles"""
        activities = self.get_all_courses()
        titles = [activity.name for activity in activities]
        return activities, titles
    
    def get_courses_by_batch(self, batch_code: str) -> List[Activity]:
        """Get courses for a specific batch"""
        if not self.is_connected:
            return []
        
        try:
            session = self.Session()
            courses = session.query(Course).join(Batch).filter(Batch.batch_code == batch_code).all()
            
            activities = []
            for course in courses:
                activity = Activity(
                    id=course.course_id,
                    start=0,
                    end=course.session_duration,
                    weight=course.credit_hours,
                    name=course.course_title,
                    room="",
                    faculty=course.instructor_name if hasattr(course, 'instructor_name') else "TBA",
                    course_code=course.course_code if hasattr(course, 'course_code') else f"CSE{course.course_id:03d}"
                )
                activities.append(activity)
            
            session.close()
            return activities
            
        except Exception as e:
            print(f"❌ Failed to get courses for batch {batch_code}: {e}")
            return []
    
    def reset_database(self) -> bool:
        """Reset database by dropping and recreating all tables"""
        if not self.engine:
            return False
        
        try:
            # Drop all tables
            Base.metadata.drop_all(self.engine)
            
            # Recreate all tables
            Base.metadata.create_all(self.engine)
            
            print("✅ Database reset successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to reset database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.is_connected = False
            print("✅ Database connection closed")
    
    def create_realistic_time_schedule(self) -> Dict[str, List[Dict]]:
        """
        Create realistic university time schedule
        
        Returns:
            Dictionary with time slots for different days
        """
        # Standard university time slots (based on typical CSE department schedule)
        time_slots = {
            "Sunday": [
                {"slot": "08:30-10:00", "start_minutes": 510, "duration": 90},  # 8:30 AM
                {"slot": "10:00-11:30", "start_minutes": 600, "duration": 90},  # 10:00 AM
                {"slot": "11:30-13:00", "start_minutes": 690, "duration": 90},  # 11:30 AM
                {"slot": "14:00-15:30", "start_minutes": 840, "duration": 90},  # 2:00 PM
                {"slot": "15:30-17:00", "start_minutes": 930, "duration": 90},  # 3:30 PM
            ],
            "Monday": [
                {"slot": "08:30-10:00", "start_minutes": 510, "duration": 90},
                {"slot": "10:00-11:30", "start_minutes": 600, "duration": 90},
                {"slot": "11:30-13:00", "start_minutes": 690, "duration": 90},
                {"slot": "14:00-15:30", "start_minutes": 840, "duration": 90},
                {"slot": "15:30-17:00", "start_minutes": 930, "duration": 90},
            ],
            "Tuesday": [
                {"slot": "08:30-10:00", "start_minutes": 510, "duration": 90},
                {"slot": "10:00-11:30", "start_minutes": 600, "duration": 90},
                {"slot": "11:30-13:00", "start_minutes": 690, "duration": 90},
                {"slot": "14:00-15:30", "start_minutes": 840, "duration": 90},
                {"slot": "15:30-17:00", "start_minutes": 930, "duration": 90},
            ],
            "Wednesday": [
                {"slot": "08:30-10:00", "start_minutes": 510, "duration": 90},
                {"slot": "10:00-11:30", "start_minutes": 600, "duration": 90},
                {"slot": "11:30-13:00", "start_minutes": 690, "duration": 90},
                {"slot": "14:00-15:30", "start_minutes": 840, "duration": 90},
                {"slot": "15:30-17:00", "start_minutes": 930, "duration": 90},
            ],
            "Thursday": [
                {"slot": "08:30-10:00", "start_minutes": 510, "duration": 90},
                {"slot": "10:00-11:30", "start_minutes": 600, "duration": 90},
                {"slot": "11:30-13:00", "start_minutes": 690, "duration": 90},
                {"slot": "14:00-15:30", "start_minutes": 840, "duration": 90},
                {"slot": "15:30-17:00", "start_minutes": 930, "duration": 90},
            ]
        }
        
        # Lab slots (longer duration for lab sessions)
        lab_slots = {
            "Sunday": [
                {"slot": "08:30-10:30", "start_minutes": 510, "duration": 120},  # 2 hour lab
                {"slot": "10:30-12:30", "start_minutes": 630, "duration": 120},
                {"slot": "14:00-16:00", "start_minutes": 840, "duration": 120},
                {"slot": "16:00-18:00", "start_minutes": 960, "duration": 120},
            ],
            "Tuesday": [
                {"slot": "08:30-10:30", "start_minutes": 510, "duration": 120},
                {"slot": "10:30-12:30", "start_minutes": 630, "duration": 120},
                {"slot": "14:00-16:00", "start_minutes": 840, "duration": 120},
                {"slot": "16:00-18:00", "start_minutes": 960, "duration": 120},
            ],
            "Thursday": [
                {"slot": "08:30-10:30", "start_minutes": 510, "duration": 120},
                {"slot": "10:30-12:30", "start_minutes": 630, "duration": 120},
                {"slot": "14:00-16:00", "start_minutes": 840, "duration": 120},
                {"slot": "16:00-18:00", "start_minutes": 960, "duration": 120},
            ]
        }
        
        return {"theory": time_slots, "lab": lab_slots}

    def get_realistic_activities_by_batch(self, batch_code: str) -> List[Activity]:
        """
        Get realistic activities for a specific batch with proper time slots
        
        Args:
            batch_code: Batch code (e.g., 'BCSE24')
        
        Returns:
            List of Activity objects with realistic scheduling
        """
        if not self.is_connected:
            return []
        
        try:
            session = self.Session()
            courses = session.query(Course).join(Batch).join(Teacher).filter(Batch.batch_code == batch_code).all()
            
            # Get time schedule
            schedule = self.create_realistic_time_schedule()
            
            activities = []
            room_assignments = ["302", "303", "304", "504", "1003"]  # Available rooms
            current_room_index = 0
            
            # Assign realistic time slots
            theory_day_index = 0
            lab_day_index = 0
            theory_slot_index = 0
            lab_slot_index = 0
            
            theory_days = list(schedule["theory"].keys())
            lab_days = list(schedule["lab"].keys())
            
            for course in courses:
                # Determine time slot based on course type
                if course.class_type == ClassType.LAB:
                    # Lab course - use lab schedule
                    day = lab_days[lab_day_index % len(lab_days)]
                    slots = schedule["lab"][day]
                    slot = slots[lab_slot_index % len(slots)]
                    
                    lab_slot_index += 1
                    if lab_slot_index >= len(slots):
                        lab_slot_index = 0
                        lab_day_index += 1
                        
                    room = "1003"  # Lab room
                else:
                    # Theory course - use theory schedule
                    day = theory_days[theory_day_index % len(theory_days)]
                    slots = schedule["theory"][day]
                    slot = slots[theory_slot_index % len(slots)]
                    
                    theory_slot_index += 1
                    if theory_slot_index >= len(slots):
                        theory_slot_index = 0
                        theory_day_index += 1
                        
                    # Assign theory room
                    room = room_assignments[current_room_index % 4]  # First 4 rooms for theory
                    current_room_index += 1
                
                activity = Activity(
                    id=course.course_id,
                    start=slot["start_minutes"],
                    end=slot["start_minutes"] + slot["duration"],
                    weight=course.credit_hours,
                    name=course.course_title,
                    room=room,
                    faculty=course.teacher.full_name,
                    course_code=course.course_code
                )
                
                # Add day and time slot information
                activity.day = day
                activity.time_slot = slot["slot"]
                
                activities.append(activity)
            session.close()
            return activities
            
        except Exception as e:
            print(f"❌ Failed to get realistic activities for batch {batch_code}: {e}")
            return []
        
    def get_all_realistic_activities(self) -> List[Activity]:
        """
        Get all realistic activities across all batches with proper time slots
        
        Returns:
            List of Activity objects with realistic scheduling for all batches
        """
        if not self.is_connected:
            return []
        
        try:
            session = self.Session()
            batches = session.query(Batch).all()
            
            all_activities = []
            
            for batch in batches:
                batch_activities = self.get_realistic_activities_by_batch(batch.batch_code)
                
                # Offset time slots for different batches to avoid conflicts
                batch_offset = (batch.batch_id - 1) * 5 * 90  # 5 slots * 90 minutes per slot
                
                for activity in batch_activities:
                    # Create a copy with offset time
                    offset_activity = Activity(
                        id=activity.id + (batch.batch_id - 1) * 100,  # Unique ID
                        start=activity.start + batch_offset,
                        end=activity.end + batch_offset,
                        weight=activity.weight,
                        name=activity.name,
                        room=activity.room,
                        faculty=activity.faculty,
                        course_code=activity.course_code
                    )
                    
                    # Preserve original day and time slot for display
                    if hasattr(activity, 'day'):
                        offset_activity.day = activity.day
                    if hasattr(activity, 'time_slot'):
                        offset_activity.time_slot = activity.time_slot
                    
                    # Add batch information
                    offset_activity.batch = batch.batch_code
                    
                    all_activities.append(offset_activity)
            
            session.close()
            return all_activities
            
        except Exception as e:
            print(f"❌ Failed to get all realistic activities: {e}")
            return []
