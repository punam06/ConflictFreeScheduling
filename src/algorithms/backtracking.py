#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backtracking Algorithm for Conflict-Free Scheduling

This module implements backtracking for exhaustive optimal solutions.
Uses pruning for efficiency.
"""

from typing import List, Set
from dataclasses import dataclass
import copy


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0  # Default weight for unweighted problems
    name: str = ""
    room: str = ""


class BacktrackingScheduler:
    """Backtracking Algorithm for Exhaustive Optimal Solutions"""
    
    @staticmethod
    def optimal_schedule(activities: List[Activity]) -> List[Activity]:
        """
        Find optimal schedule using backtracking
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of activities in optimal schedule
            
        Time Complexity: O(2^n) worst case, Space Complexity: O(n)
        """
        if not activities:
            return []
        
        # Sort activities by start time for better pruning
        activities = sorted(activities, key=lambda a: a.start)
        
        best_solution = []
        best_weight = 0.0
        
        def backtrack(index: int, current_solution: List[Activity], 
                     current_weight: float, last_end_time: int) -> None:
            """
            Recursive backtracking function
            
            Args:
                index: Current activity index
                current_solution: Current partial solution
                current_weight: Weight of current solution
                last_end_time: End time of last scheduled activity
            """
            nonlocal best_solution, best_weight
            
            # Base case: processed all activities
            if index == len(activities):
                if current_weight > best_weight:
                    best_weight = current_weight
                    best_solution = copy.deepcopy(current_solution)
                return
            
            # Pruning: if we can't possibly beat the best solution
            remaining_weight = sum(act.weight for act in activities[index:])
            if current_weight + remaining_weight <= best_weight:
                return
            
            current_activity = activities[index]
            
            # Option 1: Don't include current activity
            backtrack(index + 1, current_solution, current_weight, last_end_time)
            
            # Option 2: Include current activity (if no conflict)
            if current_activity.start >= last_end_time:
                current_solution.append(current_activity)
                backtrack(index + 1, current_solution, 
                         current_weight + current_activity.weight, 
                         current_activity.end)
                current_solution.pop()  # Backtrack
        
        backtrack(0, [], 0.0, 0)
        return best_solution
    
    @staticmethod
    def find_all_valid_schedules(activities: List[Activity]) -> List[List[Activity]]:
        """
        Find all valid (conflict-free) schedules
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of all valid schedules
        """
        if not activities:
            return [[]]
        
        all_schedules = []
        
        def backtrack(index: int, current_solution: List[Activity], 
                     last_end_time: int) -> None:
            """
            Recursive function to find all valid schedules
            
            Args:
                index: Current activity index
                current_solution: Current partial solution
                last_end_time: End time of last scheduled activity
            """
            if index == len(activities):
                all_schedules.append(copy.deepcopy(current_solution))
                return
            
            current_activity = activities[index]
            
            # Option 1: Don't include current activity
            backtrack(index + 1, current_solution, last_end_time)
            
            # Option 2: Include current activity (if no conflict)
            if current_activity.start >= last_end_time:
                current_solution.append(current_activity)
                backtrack(index + 1, current_solution, current_activity.end)
                current_solution.pop()  # Backtrack
        
        # Sort activities by start time
        activities = sorted(activities, key=lambda a: a.start)
        backtrack(0, [], 0)
        
        return all_schedules
    
    @staticmethod
    def schedule_with_constraints(activities: List[Activity], 
                                 mandatory_activities: Set[int],
                                 forbidden_activities: Set[int]) -> List[Activity]:
        """
        Find optimal schedule with mandatory and forbidden activities
        
        Args:
            activities: List of activities to schedule
            mandatory_activities: Set of activity IDs that must be included
            forbidden_activities: Set of activity IDs that must be excluded
            
        Returns:
            List of activities in optimal constrained schedule
        """
        if not activities:
            return []
        
        # Filter out forbidden activities
        valid_activities = [act for act in activities if act.id not in forbidden_activities]
        
        # Check if mandatory activities are feasible
        mandatory_acts = [act for act in valid_activities if act.id in mandatory_activities]
        if not BacktrackingScheduler._is_feasible(mandatory_acts):
            return []  # Mandatory activities conflict with each other
        
        best_solution = []
        best_weight = 0.0
        
        def backtrack(index: int, current_solution: List[Activity], 
                     current_weight: float, last_end_time: int,
                     mandatory_included: Set[int]) -> None:
            """
            Recursive backtracking with constraints
            """
            nonlocal best_solution, best_weight
            
            if index == len(valid_activities):
                # Check if all mandatory activities are included
                if mandatory_included == mandatory_activities:
                    if current_weight > best_weight:
                        best_weight = current_weight
                        best_solution = copy.deepcopy(current_solution)
                return
            
            current_activity = valid_activities[index]
            is_mandatory = current_activity.id in mandatory_activities
            
            # Option 1: Don't include current activity (if not mandatory)
            if not is_mandatory:
                backtrack(index + 1, current_solution, current_weight, 
                         last_end_time, mandatory_included)
            
            # Option 2: Include current activity (if no conflict)
            if current_activity.start >= last_end_time:
                current_solution.append(current_activity)
                new_mandatory = mandatory_included | {current_activity.id} if is_mandatory else mandatory_included
                backtrack(index + 1, current_solution, 
                         current_weight + current_activity.weight, 
                         current_activity.end, new_mandatory)
                current_solution.pop()  # Backtrack
        
        # Sort activities by start time
        valid_activities = sorted(valid_activities, key=lambda a: a.start)
        backtrack(0, [], 0.0, 0, set())
        
        return best_solution
    
    @staticmethod
    def _is_feasible(activities: List[Activity]) -> bool:
        """
        Check if a set of activities can be scheduled without conflicts
        
        Args:
            activities: List of activities to check
            
        Returns:
            True if feasible, False otherwise
        """
        if len(activities) <= 1:
            return True
        
        # Sort by start time
        activities = sorted(activities, key=lambda a: a.start)
        
        for i in range(len(activities) - 1):
            if activities[i].end > activities[i + 1].start:
                return False  # Conflict found
        
        return True
    
    @staticmethod
    def schedule_with_time_windows(activities: List[Activity], 
                                  time_windows: List[tuple]) -> List[Activity]:
        """
        Schedule activities within specific time windows
        
        Args:
            activities: List of activities to schedule
            time_windows: List of (start, end) time windows
            
        Returns:
            List of scheduled activities within time windows
        """
        if not activities or not time_windows:
            return []
        
        # Filter activities that fit within at least one time window
        valid_activities = []
        for activity in activities:
            for window_start, window_end in time_windows:
                if (activity.start >= window_start and 
                    activity.end <= window_end):
                    valid_activities.append(activity)
                    break
        
        return BacktrackingScheduler.optimal_schedule(valid_activities)
