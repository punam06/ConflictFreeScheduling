"""
Database Module for Conflict-Free Scheduling

This module provides database functionality:
- DatabaseManager: Core ORM integration with SQLAlchemy
- Data models: Batch, Teacher, Course, and Classroom models
"""

try:
    import sqlalchemy
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False

from .database_manager import DatabaseManager, Activity
from .database_manager import Batch, Teacher, Course, Classroom
