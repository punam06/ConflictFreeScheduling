#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conflict-Free Scheduling System - Main Scheduler Class
This module provides the core scheduling functionality for conflict-free scheduling.
"""

from typing import List, Tuple
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


@dataclass
class Task:
    """Class representing a task with additional metadata"""
    id: int
    start: int
    end: int
    name: str = ""
    room: str = ""
    
    def __str__(self) -> str:
        return f"Task {self.id} ({self.name}): room={self.room}, time={self.start}-{self.end}"


class ConflictFreeScheduler:
    """
    Main class for conflict-free scheduling algorithms
    Implements 4 core algorithms:
    1. Graph Coloring - For conflict resolution using graph theory
    2. Dynamic Programming - For optimal weighted activity selection
    3. Backtracking - For exhaustive optimal solutions
    4. Genetic Algorithm - For evolutionary optimization
    """
    
    def __init__(self):
        """Initialize scheduler"""
        pass
    
    def graph_coloring_schedule(self, activities: List[Activity]) -> List[Activity]:
        """
        Schedule activities using graph coloring algorithm
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of scheduled activities
        """
        # This is a facade that will call the actual implementation
        from algorithms.graph_coloring import GraphColoringScheduler
        return GraphColoringScheduler.coloring_schedule(activities)
    
    def dp_schedule(self, activities: List[Activity]) -> List[Activity]:
        """
        Schedule activities using dynamic programming algorithm
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of scheduled activities
        """
        from algorithms.dynamic_programming import DynamicProgrammingScheduler
        return DynamicProgrammingScheduler.solve_weighted_activity_selection(activities)
    
    def backtracking_schedule(self, activities: List[Activity]) -> List[Activity]:
        """
        Schedule activities using backtracking algorithm
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of scheduled activities
        """
        from algorithms.backtracking import BacktrackingScheduler
        return BacktrackingScheduler.optimal_schedule(activities)
    
    def genetic_algorithm_schedule(self, activities: List[Activity]) -> List[Activity]:
        """
        Schedule activities using genetic algorithm
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of scheduled activities
        """
        from algorithms.genetic_algorithm import GeneticAlgorithmScheduler, GAConfig
        config = GAConfig(50, 100, 0.8, 0.1, 5)  # Default configuration
        return GeneticAlgorithmScheduler.evolve_schedule(activities, config)
    
    # Utility functions
    def has_conflict(self, a1: Activity, a2: Activity) -> bool:
        """Check if two activities have time conflict"""
        return not (a1.end <= a2.start or a2.end <= a1.start)
    
    def calculate_total_weight(self, activities: List[Activity]) -> float:
        """Calculate the total weight of a list of activities"""
        return sum(activity.weight for activity in activities)
    
    def print_schedule(self, schedule: List[Activity]) -> None:
        """Print the schedule in a formatted table"""
        if not schedule:
            print("No activities scheduled.")
            return
        
        print("\n=== SCHEDULED ACTIVITIES ===")
        print(f"{'ID':5} {'Start':8} {'End':8} {'Duration':10} {'Weight':10}")
        print("-" * 41)
        
        for activity in schedule:
            duration = activity.end - activity.start
            print(f"{activity.id:5d} {activity.start:8d} {activity.end:8d} {duration:10d} {activity.weight:10.1f}")
        
        print("-" * 41)
        print(f"Total Activities: {len(schedule)}")
        print(f"Total Weight: {self.calculate_total_weight(schedule):.2f}")
    
    # Helper functions
    @staticmethod
    def sort_by_end_time(activities: List[Activity]) -> List[Activity]:
        """Sort activities by end time"""
        return sorted(activities, key=lambda a: a.end)
    
    @staticmethod
    def sort_by_start_time(activities: List[Activity]) -> List[Activity]:
        """Sort activities by start time"""
        return sorted(activities, key=lambda a: a.start)
    
    @staticmethod
    def find_latest_non_conflicting(activities: List[Activity], index: int) -> int:
        """Find the latest non-conflicting activity before the given index"""
        for i in range(index - 1, -1, -1):
            if activities[i].end <= activities[index].start:
                return i
        return -1
