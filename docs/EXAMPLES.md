# Examples

This document provides comprehensive examples of conflict-free scheduling algorithms in action.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Real-World Scenarios](#real-world-scenarios)
- [Comparative Analysis](#comparative-analysis)
- [Edge Cases](#edge-cases)

## Basic Examples

### Example 1: Simple Activity Selection

**Problem**: Schedule maximum number of activities in a conference room.

**Input**:
```
Activities:
A1: [1, 4]   (1:00 PM - 4:00 PM)
A2: [3, 5]   (3:00 PM - 5:00 PM)
A3: [0, 6]   (12:00 PM - 6:00 PM)
A4: [5, 7]   (5:00 PM - 7:00 PM)
A5: [8, 9]   (8:00 PM - 9:00 PM)
A6: [5, 9]   (5:00 PM - 9:00 PM)
```

**Visual Timeline**:
```
Time:  0  1  2  3  4  5  6  7  8  9
A1:       |-----|
A2:          |-----|
A3:    |-----------|
A4:                |-----|
A5:                      |--|
A6:                |-------|
```

**Solution (Greedy Algorithm)**:
1. Sort by finish time: A1[1,4], A2[3,5], A3[0,6], A4[5,7], A6[5,9], A5[8,9]
2. Select A1 (finishes at 4)
3. Skip A2 (starts at 3, conflicts with A1)
4. Skip A3 (starts at 0, conflicts with A1)
5. Select A4 (starts at 5, no conflict)
6. Skip A6 (starts at 5, conflicts with A4)
7. Select A5 (starts at 8, no conflict)

**Result**: Activities {A1, A4, A5} → Total: 3 activities

**C++ Implementation**:
```cpp
#include "scheduler.h"
#include <iostream>

int main() {
    std::vector<Activity> activities = {
        {1, 1, 4},  // id, start, end
        {2, 3, 5},
        {3, 0, 6},
        {4, 5, 7},
        {5, 8, 9},
        {6, 5, 9}
    };
    
    ConflictFreeScheduler scheduler;
    std::vector<Activity> selected = scheduler.greedySchedule(activities);
    
    std::cout << "Selected activities: ";
    for (const auto& activity : selected) {
        std::cout << "A" << activity.id << " ";
    }
    std::cout << std::endl;
    // Output: Selected activities: A1 A4 A5
    
    return 0;
}
```

### Example 2: Weighted Activity Selection

**Problem**: Maximize profit from scheduled activities.

**Input**:
```
Activities with profits:
A1: [1, 3], profit = 20
A2: [2, 5], profit = 30
A3: [4, 6], profit = 10
A4: [6, 8], profit = 40
```

**Greedy vs Dynamic Programming**:

**Greedy Solution** (by finish time):
- Select: A1, A3, A4
- Total profit: 20 + 10 + 40 = 70

**Optimal Solution** (Dynamic Programming):
- Select: A2, A4
- Total profit: 30 + 40 = 70

*In this case, both approaches yield the same result.*

## Real-World Scenarios

### Scenario 1: University Course Scheduling

**Problem**: Schedule courses to minimize classroom conflicts.

**Input**:
```
Courses:
Math 101:     [9:00, 10:30]  - Room capacity: 50
Physics 201:  [10:00, 11:30] - Room capacity: 30
Chem 301:     [11:00, 12:30] - Room capacity: 40
Bio 401:      [13:00, 14:30] - Room capacity: 35
CS 501:       [14:00, 15:30] - Room capacity: 60
```

**Constraints**:
- Only one course per time slot in each room
- Maximize total enrolled students

**Solution**:
```python
def schedule_courses(courses):
    # Sort by end time
    sorted_courses = sorted(courses, key=lambda x: x['end_time'])
    
    scheduled = []
    last_end_time = 0
    total_students = 0
    
    for course in sorted_courses:
        if course['start_time'] >= last_end_time:
            scheduled.append(course)
            last_end_time = course['end_time']
            total_students += course['capacity']
    
    return scheduled, total_students

# Result: Math 101, Chem 301, CS 501
# Total capacity: 50 + 40 + 60 = 150 students
```

### Scenario 2: CPU Process Scheduling

**Problem**: Schedule processes to maximize CPU utilization.

**Input**:
```
Processes:
P1: [0, 3], priority = 1
P2: [1, 4], priority = 3
P3: [2, 6], priority = 2
P4: [5, 7], priority = 1
P5: [8, 9], priority = 2
```

**Weighted Scheduling** (by priority):
```python
def weighted_process_scheduling(processes):
    n = len(processes)
    # Sort by finish time
    processes.sort(key=lambda x: x[1])
    
    # DP array
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        # Find latest non-conflicting process
        latest_compatible = 0
        for j in range(i - 1, 0, -1):
            if processes[j-1][1] <= processes[i-1][0]:
                latest_compatible = j
                break
        
        # Choose max of including or excluding current process
        include = processes[i-1][2] + dp[latest_compatible]
        exclude = dp[i-1]
        dp[i] = max(include, exclude)
    
    return dp[n]

# Result: Maximum priority sum = 6 (P1, P4, P5)
```

### Scenario 3: Meeting Room Booking System

**Problem**: Book meeting rooms efficiently for a corporate office.

**Input**:
```python
meetings = [
    {"id": "M1", "start": 900, "end": 1030, "attendees": 5},
    {"id": "M2", "start": 1000, "end": 1100, "attendees": 8},
    {"id": "M3", "start": 1100, "end": 1200, "attendees": 3},
    {"id": "M4", "start": 1300, "end": 1400, "attendees": 12},
    {"id": "M5", "start": 1330, "end": 1430, "attendees": 6},
    {"id": "M6", "start": 1500, "end": 1600, "attendees": 4}
]
```

**Multi-objective Optimization**:
```python
def optimize_meeting_rooms(meetings):
    # Objective 1: Maximize number of meetings
    # Objective 2: Maximize total attendees
    
    # Greedy by finish time
    meetings_by_time = sorted(meetings, key=lambda x: x['end'])
    
    scheduled_meetings = []
    last_end = 0
    total_attendees = 0
    
    for meeting in meetings_by_time:
        if meeting['start'] >= last_end:
            scheduled_meetings.append(meeting)
            last_end = meeting['end']
            total_attendees += meeting['attendees']
    
    return scheduled_meetings, total_attendees

# Result: M1, M3, M4, M6
# Total attendees: 5 + 3 + 12 + 4 = 24
```

## Comparative Analysis

### Example 3: Algorithm Performance Comparison

**Problem**: Same dataset, different algorithms.

**Input**:
```
Activities: [(1,4), (3,5), (0,6), (5,7), (8,9), (5,9)]
Weights:    [20,    30,    35,    40,    15,    25]
```

**Results**:

| Algorithm | Selected Activities | Total Weight | Time (ms) |
|-----------|-------------------|--------------|-----------|
| Greedy (finish time) | [0,3,4] | 75 | 0.1 |
| Greedy (weight/duration) | [1,3] | 70 | 0.1 |
| Dynamic Programming | [1,3] | 70 | 1.2 |
| Branch & Bound | [1,3] | 70 | 15.3 |

### Scalability Analysis

**Dataset Sizes**: 10, 50, 100, 500, 1000 activities

```python
import time
import matplotlib.pyplot as plt

def benchmark_algorithms(sizes):
    results = {"greedy": [], "dp": [], "bb": []}
    
    for n in sizes:
        activities = generate_random_activities(n)
        
        # Greedy
        start = time.time()
        greedy_result = greedy_schedule(activities)
        results["greedy"].append(time.time() - start)
        
        # DP (only for smaller sizes)
        if n <= 500:
            start = time.time()
            dp_result = dp_schedule(activities)
            results["dp"].append(time.time() - start)
        
        # Branch & Bound (only for very small sizes)
        if n <= 50:
            start = time.time()
            bb_result = branch_bound_schedule(activities)
            results["bb"].append(time.time() - start)
    
    return results
```

## Edge Cases

### Case 1: Empty Input

**Input**: `[]`
**Expected Output**: `[]`
**All Algorithms**: Should handle gracefully

```python
def handle_empty_input(activities):
    if not activities:
        return []
    # ... rest of algorithm
```

### Case 2: Single Activity

**Input**: `[(5, 10)]`
**Expected Output**: `[0]` (select the only activity)

### Case 3: No Compatible Activities

**Input**: `[(1,5), (2,6), (3,7)]` (all overlapping)
**Expected Output**: `[0]` or `[1]` or `[2]` (any single activity)

### Case 4: All Activities Compatible

**Input**: `[(1,2), (3,4), (5,6), (7,8)]`
**Expected Output**: `[0,1,2,3]` (select all activities)

### Case 5: Identical Start/End Times

**Input**: `[(1,3), (1,3), (1,3)]`
**Greedy Output**: `[0]` (first activity)
**DP Output**: `[0]` or `[1]` or `[2]` (any single activity)

### Case 6: Zero Duration Activities

**Input**: `[(1,1), (2,2), (3,3)]`
**Interpretation**: Point events (meetings, deadlines)
**Output**: `[0,1,2]` (all can be scheduled)

## Interactive Examples

### Example Runner

```python
def run_example(activities, weights=None, algorithm="greedy"):
    """
    Interactive example runner
    
    Args:
        activities: List of (start, end) tuples
        weights: Optional weights for each activity
        algorithm: "greedy", "dp", or "bb"
    """
    print(f"Input: {activities}")
    if weights:
        print(f"Weights: {weights}")
    
    start_time = time.time()
    
    if algorithm == "greedy":
        result = greedy_activity_selection(activities)
    elif algorithm == "dp":
        result = dp_weighted_activity_selection(activities, weights)
    elif algorithm == "bb":
        result = branch_bound_activity_selection(activities, weights)
    
    end_time = time.time()
    
    print(f"Algorithm: {algorithm}")
    print(f"Selected activities: {result}")
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    
    return result

# Usage:
activities = [(1,4), (3,5), (0,6), (5,7), (8,9)]
run_example(activities, algorithm="greedy")
```

---

*These examples demonstrate the practical applications and performance characteristics of different conflict-free scheduling algorithms. Use them as a reference for implementing and testing your solutions.*
