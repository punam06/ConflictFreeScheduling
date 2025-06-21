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
    
    def initialize_with_sample_data(self) -> bool:
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
                    room=""  # Will be assigned by scheduling algorithm
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
                    room=""
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
