#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for the Conflict-Free Scheduling System
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scheduler import Activity, ConflictFreeScheduler
from utils.file_parser import FileParser


class TestActivity(unittest.TestCase):
    """Test Activity class"""
    
    def test_activity_creation(self):
        """Test creating an Activity object"""
        activity = Activity(1, 0, 90, 3.0, "Test Course", "CSE-101")
        
        self.assertEqual(activity.id, 1)
        self.assertEqual(activity.start, 0)
        self.assertEqual(activity.end, 90)
        self.assertEqual(activity.weight, 3.0)
        self.assertEqual(activity.name, "Test Course")
        self.assertEqual(activity.room, "CSE-101")
    
    def test_activity_str(self):
        """Test Activity string representation"""
        activity = Activity(1, 0, 90, 3.0)
        expected = "Activity 1: start=0, end=90, weight=3.0"
        self.assertEqual(str(activity), expected)


class TestConflictFreeScheduler(unittest.TestCase):
    """Test ConflictFreeScheduler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scheduler = ConflictFreeScheduler()
        self.activities = [
            Activity(1, 0, 90, 3.0, "Course A"),
            Activity(2, 100, 190, 3.0, "Course B"),
            Activity(3, 50, 140, 1.0, "Course C"),  # Conflicts with A
            Activity(4, 200, 290, 3.0, "Course D"),
        ]
    
    def test_has_conflict(self):
        """Test conflict detection"""
        # No conflict
        self.assertFalse(self.scheduler.has_conflict(self.activities[0], self.activities[1]))
        
        # Has conflict
        self.assertTrue(self.scheduler.has_conflict(self.activities[0], self.activities[2]))
    
    def test_calculate_total_weight(self):
        """Test total weight calculation"""
        total_weight = self.scheduler.calculate_total_weight(self.activities)
        expected = 3.0 + 3.0 + 1.0 + 3.0
        self.assertEqual(total_weight, expected)
    
    def test_sort_by_end_time(self):
        """Test sorting by end time"""
        sorted_activities = ConflictFreeScheduler.sort_by_end_time(self.activities)
        end_times = [activity.end for activity in sorted_activities]
        self.assertEqual(end_times, sorted(end_times))
    
    def test_sort_by_start_time(self):
        """Test sorting by start time"""
        sorted_activities = ConflictFreeScheduler.sort_by_start_time(self.activities)
        start_times = [activity.start for activity in sorted_activities]
        self.assertEqual(start_times, sorted(start_times))


class TestFileParser(unittest.TestCase):
    """Test FileParser class"""
    
    def test_generate_sample_data(self):
        """Test sample data generation"""
        test_file = "test_sample.csv"
        
        # Generate sample data
        success = FileParser.generate_sample_data(test_file, 5)
        self.assertTrue(success)
        
        # Parse the generated data
        activities = FileParser.parse_csv(test_file)
        self.assertEqual(len(activities), 5)
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == '__main__':
    unittest.main()
