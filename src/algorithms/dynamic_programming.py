#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dynamic Programming Algorithm for Conflict-Free Scheduling

This module implements dynamic programming for weighted activity selection.
Uses memoization for optimal performance.
"""

from typing import List, Dict
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


class DynamicProgrammingScheduler:
    """Dynamic Programming Algorithm for Weighted Activity Selection"""
    
    @staticmethod
    def solve_weighted_activity_selection(activities: List[Activity]) -> List[Activity]:
        """
        Solve weighted activity selection using dynamic programming
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of selected activities with maximum weight
            
        Time Complexity: O(n log n), Space Complexity: O(n)
        """
        if not activities:
            return []
        
        # Sort activities by end time
        activities = sorted(activities, key=lambda a: a.end)
        n = len(activities)
        
        # Build memoization table for dynamic programming
        memo = {}
        
        # Find the latest non-conflicting activity for each activity
        latest_non_conflicting = []
        for i in range(n):
            latest = DynamicProgrammingScheduler.find_latest_non_conflicting(activities, i)
            latest_non_conflicting.append(latest)
        
        def dp(index: int) -> float:
            """
            DP function to find maximum weight up to index
            
            Args:
                index: Current activity index
                
            Returns:
                Maximum weight achievable up to this index
            """
            if index < 0:
                return 0
            
            if index in memo:
                return memo[index]
            
            # Option 1: Don't include current activity
            without_current = dp(index - 1)
            
            # Option 2: Include current activity
            with_current = activities[index].weight
            if latest_non_conflicting[index] >= 0:
                with_current += dp(latest_non_conflicting[index])
            
            memo[index] = max(without_current, with_current)
            return memo[index]
        
        # Calculate maximum weight
        max_weight = dp(n - 1)
        
        # Reconstruct the solution
        selected_activities = []
        i = n - 1
        while i >= 0:
            # Check if current activity is included in optimal solution
            without_current = dp(i - 1) if i > 0 else 0
            with_current = activities[i].weight
            if latest_non_conflicting[i] >= 0:
                with_current += dp(latest_non_conflicting[i])
            
            if with_current >= without_current:
                # Current activity is included
                selected_activities.append(activities[i])
                i = latest_non_conflicting[i]
            else:
                # Current activity is not included
                i -= 1
        
        # Reverse to get chronological order
        selected_activities.reverse()
        
        return selected_activities
    
    @staticmethod
    def find_latest_non_conflicting(activities: List[Activity], index: int) -> int:
        """
        Find the latest non-conflicting activity before the given index
        
        Args:
            activities: List of activities (sorted by end time)
            index: Current activity index
            
        Returns:
            Index of latest non-conflicting activity, or -1 if none found
        """
        for i in range(index - 1, -1, -1):
            if activities[i].end <= activities[index].start:
                return i
        return -1
    
    @staticmethod
    def solve_unweighted_activity_selection(activities: List[Activity]) -> List[Activity]:
        """
        Solve unweighted activity selection (classic greedy approach)
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            List of selected activities (maximum count)
            
        Time Complexity: O(n log n), Space Complexity: O(1)
        """
        if not activities:
            return []
        
        # Sort activities by end time
        activities = sorted(activities, key=lambda a: a.end)
        
        selected = []
        last_end_time = float('-inf')
        
        for activity in activities:
            if activity.start >= last_end_time:
                selected.append(activity)
                last_end_time = activity.end
        
        return selected
    
    @staticmethod
    def solve_with_different_strategies(activities: List[Activity]) -> Dict[str, List[Activity]]:
        """
        Solve using different DP strategies for comparison
        
        Args:
            activities: List of activities to schedule
            
        Returns:
            Dictionary containing results from different strategies
        """
        results = {}
        
        # Strategy 1: Maximum weight
        results['max_weight'] = DynamicProgrammingScheduler.solve_weighted_activity_selection(activities)
        
        # Strategy 2: Maximum count (unweighted)
        results['max_count'] = DynamicProgrammingScheduler.solve_unweighted_activity_selection(activities)
        
        # Strategy 3: Earliest deadline first
        earliest_deadline = sorted(activities, key=lambda a: a.end)
        results['earliest_deadline'] = DynamicProgrammingScheduler._greedy_selection(earliest_deadline)
        
        # Strategy 4: Shortest job first
        shortest_job = sorted(activities, key=lambda a: a.end - a.start)
        results['shortest_job'] = DynamicProgrammingScheduler._greedy_selection(shortest_job)
        
        return results
    
    @staticmethod
    def _greedy_selection(activities: List[Activity]) -> List[Activity]:
        """
        Helper method for greedy selection
        
        Args:
            activities: Pre-sorted list of activities
            
        Returns:
            List of selected activities using greedy approach
        """
        if not activities:
            return []
        
        selected = [activities[0]]
        last_end_time = activities[0].end
        
        for i in range(1, len(activities)):
            if activities[i].start >= last_end_time:
                selected.append(activities[i])
                last_end_time = activities[i].end
        
        return selected
