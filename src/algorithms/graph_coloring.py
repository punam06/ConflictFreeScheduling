#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Graph Coloring Algorithm for Conflict-Free Scheduling

This module implements graph coloring to solve scheduling conflicts.
Each activity is a vertex, conflicts are edges, and colors represent time slots.
"""

from typing import List, Dict, Set
from collections import defaultdict
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


class GraphColoringScheduler:
    """Graph Coloring Algorithm for Conflict-Free Scheduling"""
    
    @staticmethod
    def coloring_schedule(activities: List[Activity]) -> List[Activity]:
        """
        Solve scheduling using graph coloring (greedy approach)
        
        Args:
            activities: Vector of activities to schedule
            
        Returns:
            Vector of scheduled activities with assigned time slots
            
        Time Complexity: O(V²), Space Complexity: O(V)
        """
        if not activities:
            return []
        
        # Build conflict graph
        conflict_graph = GraphColoringScheduler.build_conflict_graph(activities)
        
        # Assign colors (time slots) to activities
        color_assignment = GraphColoringScheduler.assign_colors(activities, conflict_graph)
        
        # Create scheduled activities with assigned time slots
        scheduled_activities = []
        
        # Group activities by color (time slot)
        color_groups = defaultdict(list)
        for activity in activities:
            color = color_assignment[activity.id]
            if color >= 0:
                color_groups[color].append(activity)
        
        # Schedule each color group sequentially
        current_time = 0
        for color, group in color_groups.items():
            # Sort activities in group by original start time to maintain some order
            group.sort(key=lambda a: a.start)
            
            # Schedule activities in this color group non-conflictingly
            for activity in group:
                scheduled = Activity(
                    id=activity.id,
                    start=current_time,
                    end=current_time + (activity.end - activity.start),
                    weight=activity.weight,
                    name=activity.name,
                    room=activity.room
                )
                scheduled_activities.append(scheduled)
                current_time = scheduled.end + 1  # Add gap to prevent edge conflicts
        
        return scheduled_activities
    
    @staticmethod
    def welsh_powell_coloring(activities: List[Activity]) -> int:
        """
        Welsh-Powell graph coloring algorithm
        
        Args:
            activities: Vector of activities
            
        Returns:
            Minimum number of colors (time slots) needed
        """
        if not activities:
            return 0
        
        conflict_graph = GraphColoringScheduler.build_conflict_graph(activities)
        
        # Calculate degree of each vertex
        degree_list = []  # (degree, activity_id)
        for activity in activities:
            degree = len(conflict_graph[activity.id])
            degree_list.append((degree, activity.id))
        
        # Sort by degree (descending order)
        degree_list.sort(reverse=True)
        
        colors = {}
        max_color = 0
        
        for _, activity_id in degree_list:
            # Find the smallest color not used by neighbors
            used_colors = set()
            for neighbor in conflict_graph[activity_id]:
                if neighbor in colors:
                    used_colors.add(colors[neighbor])
            
            color = 0
            while color in used_colors:
                color += 1
            
            colors[activity_id] = color
            max_color = max(max_color, color)
        
        return max_color + 1  # Number of colors needed
    
    @staticmethod
    def build_conflict_graph(activities: List[Activity]) -> Dict[int, List[int]]:
        """
        Build conflict graph from activities
        
        Args:
            activities: Vector of activities
            
        Returns:
            Adjacency list representation of conflict graph
        """
        graph = {activity.id: [] for activity in activities}
        
        # Add edges for conflicting activities
        n = len(activities)
        for i in range(n):
            for j in range(i + 1, n):
                if GraphColoringScheduler.has_time_conflict(activities[i], activities[j]):
                    graph[activities[i].id].append(activities[j].id)
                    graph[activities[j].id].append(activities[i].id)
        
        return graph
    
    @staticmethod
    def has_time_conflict(a1: Activity, a2: Activity) -> bool:
        """
        Check if two activities conflict in time
        
        Args:
            a1: First activity
            a2: Second activity
            
        Returns:
            True if there's a time conflict, False otherwise
        """
        return not (a1.end <= a2.start or a2.end <= a1.start)
    
    @staticmethod
    def assign_colors(activities: List[Activity], graph: Dict[int, List[int]]) -> Dict[int, int]:
        """
        Assign colors using greedy approach
        
        Args:
            activities: Vector of activities
            graph: Conflict graph as adjacency list
            
        Returns:
            Dictionary mapping activity IDs to color assignments
        """
        color_map = {}
        
        for activity in activities:
            # Get colors used by neighbors
            neighbor_colors = set()
            for neighbor_id in graph[activity.id]:
                if neighbor_id in color_map:
                    neighbor_colors.add(color_map[neighbor_id])
            
            # Find the smallest color not used by neighbors
            color = 0
            while color in neighbor_colors:
                color += 1
            
            # Assign this color to the activity
            color_map[activity.id] = color
        
        return color_map
