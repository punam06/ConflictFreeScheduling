#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Activity Class Definition
========================

Common Activity class for the Conflict-Free Scheduling System
This module provides a centralized Activity class to avoid conflicts.

Author: Punam
Version: 2.0 (Enhanced)
"""

from dataclasses import dataclass


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0  # Default weight for unweighted problems
    name: str = ""
    room: str = ""
    faculty: str = ""  # Faculty name
    course_code: str = ""  # Course code
    
    def __str__(self) -> str:
        return f"Activity {self.id}: start={self.start}, end={self.end}, weight={self.weight}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_duration(self) -> int:
        """Get the duration of the activity"""
        return self.end - self.start
    
    def overlaps_with(self, other: 'Activity') -> bool:
        """Check if this activity overlaps with another activity"""
        return not (self.end <= other.start or other.end <= self.start)
    
    def to_dict(self) -> dict:
        """Convert activity to dictionary"""
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'weight': self.weight,
            'name': self.name,
            'room': self.room,
            'faculty': self.faculty,
            'course_code': self.course_code
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        """Create activity from dictionary"""
        return cls(
            id=data.get('id', 0),
            start=data.get('start', 0),
            end=data.get('end', 0),
            weight=data.get('weight', 1.0),
            name=data.get('name', ''),
            room=data.get('room', ''),
            faculty=data.get('faculty', ''),
            course_code=data.get('course_code', '')
        )
