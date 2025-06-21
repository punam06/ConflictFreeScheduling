#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Parser for Conflict-Free Scheduling System

This module provides file parsing capabilities for reading activity data
from various file formats.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import csv
import json
import os


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0
    name: str = ""
    room: str = ""


class FileParser:
    """File Parser for Activity Data"""
    
    @staticmethod
    def parse_csv(filename: str) -> List[Activity]:
        """
        Parse activities from CSV file
        
        Expected CSV format:
        id,start,end,weight,name,room
        1,0,90,3.0,Programming Fundamentals,CSE-101
        
        Args:
            filename: Path to CSV file
            
        Returns:
            List of activities
        """
        activities = []
        
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return activities
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    activity = Activity(
                        id=int(row.get('id', 0)),
                        start=int(row.get('start', 0)),
                        end=int(row.get('end', 0)),
                        weight=float(row.get('weight', 1.0)),
                        name=row.get('name', ''),
                        room=row.get('room', '')
                    )
                    activities.append(activity)
            
            print(f"✅ Loaded {len(activities)} activities from {filename}")
            
        except Exception as e:
            print(f"❌ Error parsing CSV file {filename}: {e}")
        
        return activities
    
    @staticmethod
    def parse_json(filename: str) -> List[Activity]:
        """
        Parse activities from JSON file
        
        Expected JSON format:
        {
            "activities": [
                {
                    "id": 1,
                    "start": 0,
                    "end": 90,
                    "weight": 3.0,
                    "name": "Programming Fundamentals",
                    "room": "CSE-101"
                }
            ]
        }
        
        Args:
            filename: Path to JSON file
            
        Returns:
            List of activities
        """
        activities = []
        
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return activities
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                activity_data = data.get('activities', [])
                
                for item in activity_data:
                    activity = Activity(
                        id=item.get('id', 0),
                        start=item.get('start', 0),
                        end=item.get('end', 0),
                        weight=item.get('weight', 1.0),
                        name=item.get('name', ''),
                        room=item.get('room', '')
                    )
                    activities.append(activity)
            
            print(f"✅ Loaded {len(activities)} activities from {filename}")
            
        except Exception as e:
            print(f"❌ Error parsing JSON file {filename}: {e}")
        
        return activities
    
    @staticmethod
    def parse_text(filename: str) -> List[Activity]:
        """
        Parse activities from simple text file
        
        Expected text format (space-separated):
        # Comments start with #
        id start end weight name
        1 0 90 3.0 Programming_Fundamentals
        2 100 180 3.0 Data_Structures
        
        Args:
            filename: Path to text file
            
        Returns:
            List of activities
        """
        activities = []
        
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return activities
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    
                    if len(parts) < 4:
                        print(f"⚠️ Skipping line {line_num}: insufficient data")
                        continue
                    
                    try:
                        activity = Activity(
                            id=int(parts[0]),
                            start=int(parts[1]),
                            end=int(parts[2]),
                            weight=float(parts[3]),
                            name=parts[4].replace('_', ' ') if len(parts) > 4 else '',
                            room=parts[5] if len(parts) > 5 else ''
                        )
                        activities.append(activity)
                        
                    except ValueError as e:
                        print(f"⚠️ Skipping line {line_num}: invalid data format - {e}")
            
            print(f"✅ Loaded {len(activities)} activities from {filename}")
            
        except Exception as e:
            print(f"❌ Error parsing text file {filename}: {e}")
        
        return activities
    
    @staticmethod
    def write_csv(activities: List[Activity], filename: str) -> bool:
        """
        Write activities to CSV file
        
        Args:
            activities: List of activities to write
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                writer.writerow(['id', 'start', 'end', 'weight', 'name', 'room'])
                
                # Write activities
                for activity in activities:
                    writer.writerow([
                        activity.id,
                        activity.start,
                        activity.end,
                        activity.weight,
                        activity.name,
                        activity.room
                    ])
            
            print(f"✅ Saved {len(activities)} activities to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error writing CSV file {filename}: {e}")
            return False
    
    @staticmethod
    def write_json(activities: List[Activity], filename: str) -> bool:
        """
        Write activities to JSON file
        
        Args:
            activities: List of activities to write
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                "activities": [
                    {
                        "id": activity.id,
                        "start": activity.start,
                        "end": activity.end,
                        "weight": activity.weight,
                        "name": activity.name,
                        "room": activity.room
                    }
                    for activity in activities
                ],
                "metadata": {
                    "total_activities": len(activities),
                    "total_weight": sum(activity.weight for activity in activities),
                    "generated_at": str(datetime.now())
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(activities)} activities to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error writing JSON file {filename}: {e}")
            return False
    
    @staticmethod
    def generate_sample_data(filename: str = "data/sample_activities.csv", 
                           count: int = 10) -> bool:
        """
        Generate sample activity data for testing
        
        Args:
            filename: Output filename
            count: Number of sample activities to generate
            
        Returns:
            True if successful, False otherwise
        """
        import random
        
        # Sample course names
        course_names = [
            "Programming Fundamentals", "Data Structures", "Algorithms",
            "Database Systems", "Software Engineering", "Computer Networks",
            "Operating Systems", "Computer Graphics", "Artificial Intelligence",
            "Machine Learning", "Web Development", "Mobile App Development",
            "Cybersecurity", "Human-Computer Interaction", "Distributed Systems"
        ]
        
        # Sample rooms
        rooms = ["CSE-101", "CSE-102", "CSE-201", "CSE-202", "CSE-301", "LAB-1", "LAB-2"]
        
        activities = []
        
        for i in range(count):
            # Generate random activity
            duration = random.choice([90, 120, 180])  # 1.5, 2, or 3 hours
            start_time = random.randint(0, 12) * 60  # Start between 0-12 hours (in minutes)
            
            activity = Activity(
                id=i + 1,
                start=start_time,
                end=start_time + duration,
                weight=random.choice([1.0, 1.5, 3.0, 4.0]),  # Credit hours
                name=random.choice(course_names),
                room=random.choice(rooms)
            )
            activities.append(activity)
        
        # Sort by start time to make it more realistic
        activities.sort(key=lambda a: a.start)
        
        # Update IDs to be sequential
        for i, activity in enumerate(activities):
            activity.id = i + 1
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        return FileParser.write_csv(activities, filename)


# Import datetime at the top level to avoid import errors
from datetime import datetime
