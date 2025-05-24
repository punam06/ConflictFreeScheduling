# API Reference

This document provides a comprehensive API reference for the Conflict-Free Scheduling C++ library.

## Table of Contents

- [Core Data Structures](#core-data-structures)
- [Main Scheduler Class](#main-scheduler-class)
- [Algorithm Classes](#algorithm-classes)
- [Utility Functions](#utility-functions)
- [Error Handling](#error-handling)

## Core Data Structures

### Activity Structure

```cpp
struct Activity {
    int id;
    int start;
    int end;
    double weight = 1.0;  // Default weight for unweighted problems
    
    // Constructors
    Activity(int id, int start, int end);
    Activity(int id, int start, int end, double weight);
    
    // Utility methods
    int duration() const { return end - start; }
    bool conflictsWith(const Activity& other) const;
};
```

**Example Usage:**
```cpp
Activity course1(1, 9, 11, 50.0);  // Data Structures: 9-11 AM, 50 students
Activity course2(2, 10, 12, 45.0); // Algorithms: 10-12 PM, 45 students
```

### Task Structure

```cpp
struct Task {
    int id;
    int start;
    int end;
    std::string name;
    std::string room;
    
    // Constructors
    Task(int id, int start, int end);
    Task(int id, int start, int end, const std::string& name, const std::string& room);
};
```

## Main Scheduler Class

### ConflictFreeScheduler

```cpp
class ConflictFreeScheduler {
public:
    ConflictFreeScheduler() = default;
    ~ConflictFreeScheduler() = default;
    
    // Greedy algorithms
    std::vector<Activity> greedySchedule(std::vector<Activity> activities);
    std::vector<int> greedyActivitySelection(std::vector<Activity> activities);
    std::vector<Activity> greedyWeightedSchedule(std::vector<Activity> activities);
    
    // Dynamic Programming algorithms
    std::vector<Activity> dpSchedule(std::vector<Activity> activities);
    std::vector<Activity> dpWeightedSchedule(std::vector<Activity> activities);
    
    // Branch and Bound algorithms
    std::vector<Activity> branchAndBoundSchedule(std::vector<Activity> activities);
    
    // Utility functions
    bool hasConflict(const Activity& a1, const Activity& a2) const;
    double calculateTotalWeight(const std::vector<Activity>& activities) const;
    void printSchedule(const std::vector<Activity>& schedule) const;
};
```

### Core Methods

#### `std::vector<Activity> greedySchedule(std::vector<Activity> activities)`

Implements the greedy algorithm for activity selection problem using finish time ordering.

**Parameters:**
- `activities` (std::vector<Activity>): Vector of Activity objects

**Returns:**
- `std::vector<Activity>`: Vector of selected activities that don't conflict

**Time Complexity:** O(n log n)  
**Space Complexity:** O(1)

**Example:**
```cpp
ConflictFreeScheduler scheduler;
std::vector<Activity> activities = {
    {1, 1, 4, 20.0}, {2, 3, 5, 30.0}, {3, 0, 6, 35.0}, 
    {4, 5, 7, 25.0}, {5, 8, 9, 15.0}
};

std::vector<Activity> selected = scheduler.greedySchedule(activities);
std::cout << "Selected " << selected.size() << " activities" << std::endl;
```

---

#### `std::vector<Activity> dpSchedule(std::vector<Activity> activities)`

Optimal solution using dynamic programming approach.

**Parameters:**
- `activities` (std::vector<Activity>): Vector of Activity objects

**Returns:**
- `std::vector<Activity>`: Optimal set of non-conflicting activities

**Time Complexity:** O(n²) naive implementation, O(n log n) optimized  
**Space Complexity:** O(n)

**Example:**
```cpp
ConflictFreeScheduler scheduler;
std::vector<Activity> activities = {
    {1, 1, 4, 10.0}, {2, 3, 5, 20.0}, {3, 0, 6, 30.0}
};

std::vector<Activity> optimal = scheduler.dpSchedule(activities);
double totalWeight = scheduler.calculateTotalWeight(optimal);
```

---

#### `std::vector<Activity> branchAndBoundSchedule(std::vector<Activity> activities)`

Exact solution using branch and bound technique.

**Parameters:**
- `activities` (std::vector<Activity>): Vector of Activity objects

**Returns:**
- `std::vector<Activity>`: Optimal set of activities

**Time Complexity:** O(2^n) worst case, better on average with pruning  
**Space Complexity:** O(n)

**Example:**
```cpp
ConflictFreeScheduler scheduler;
std::vector<Activity> activities = {
    {1, 1, 3, 50.0}, {2, 2, 4, 30.0}, {3, 3, 5, 20.0}
};

std::vector<Activity> result = scheduler.branchAndBoundSchedule(activities);
```

## Algorithm Classes

### GreedyAlgorithms

```cpp
class GreedyAlgorithms {
public:
    static std::vector<Activity> activitySelection(std::vector<Activity> activities);
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    static std::vector<Activity> maxUtilizationSelection(std::vector<Activity> activities);

private:
    static bool compareByEndTime(const Activity& a, const Activity& b);
    static bool compareByWeightRatio(const Activity& a, const Activity& b);
    static bool hasConflict(const Activity& a, const Activity& b);
};
```

#### `static std::vector<Activity> activitySelection(std::vector<Activity> activities)`

Classical greedy activity selection algorithm.

**Parameters:**
- `activities` (std::vector<Activity>): Activities to schedule

**Returns:**
- `std::vector<Activity>`: Selected non-conflicting activities

**Algorithm Steps:**
1. Sort activities by finish time
2. Select first activity
3. For each remaining activity, select if it doesn't conflict with last selected
4. Return selected activities

**Example:**
```cpp
std::vector<Activity> activities = {
    {1, 1, 4}, {2, 3, 5}, {3, 0, 6}, {4, 5, 7}, {5, 8, 9}
};

std::vector<Activity> result = GreedyAlgorithms::activitySelection(activities);
// Typically selects activities: 1, 4, 5 (IDs)
```

### DynamicProgramming

```cpp
class DynamicProgramming {
public:
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    static std::vector<Activity> optimizedSelection(std::vector<Activity> activities);
    
private:
    static int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
    static void reconstructSolution(const std::vector<Activity>& activities, 
                                   const std::vector<int>& dp, 
                                   std::vector<Activity>& result, int index);
};
```

#### `static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities)`

Optimal weighted activity selection using dynamic programming.

**Parameters:**
- `activities` (std::vector<Activity>): Weighted activities

**Returns:**
- `std::vector<Activity>`: Optimal set maximizing total weight

**Algorithm:**
```
dp[i] = max(weight[i] + dp[latest_non_conflicting[i]], dp[i-1])
```

**Example:**
```cpp
std::vector<Activity> activities = {
    {1, 1, 3, 100}, {2, 2, 4, 200}, {3, 3, 5, 300}
};

std::vector<Activity> optimal = DynamicProgramming::weightedActivitySelection(activities);
```

### BranchAndBound

```cpp
class BranchAndBound {
public:
    static std::vector<Activity> exactSolution(std::vector<Activity> activities, 
                                              int timeLimit = 60);
    
private:
    struct Node {
        std::vector<bool> selected;
        double currentWeight;
        double upperBound;
        int level;
    };
    
    static double calculateUpperBound(const std::vector<Activity>& activities, 
                                     const Node& node);
    static bool isValidSolution(const std::vector<Activity>& activities, 
                               const std::vector<bool>& selected);
};
```

## Utility Functions

### Input/Output Operations

#### File Reading

```cpp
namespace FileIO {
    std::vector<Activity> readActivitiesFromCSV(const std::string& filepath);
    std::vector<Activity> readActivitiesFromJSON(const std::string& filepath);
    void writeResultsToFile(const std::vector<Activity>& results, 
                           const std::string& filepath, 
                           const std::string& format = "csv");
}
```

**CSV Format:**
```csv
id,start,end,weight
1,9,11,50
2,10,12,45
3,13,15,40
```

**Usage Example:**
```cpp
std::vector<Activity> activities = FileIO::readActivitiesFromCSV("courses.csv");
ConflictFreeScheduler scheduler;
std::vector<Activity> result = scheduler.greedySchedule(activities);
FileIO::writeResultsToFile(result, "output.csv");
```

### Data Generation

```cpp
namespace DataGenerator {
    std::vector<Activity> generateRandomActivities(int n, 
                                                  int timeRange = 100, 
                                                  int maxDuration = 20, 
                                                  int seed = -1);
    
    std::vector<Activity> generateWorstCaseInput(int n);
    std::vector<Activity> generateCourseScheduleData();
}
```

**Example:**
```cpp
// Generate 50 random activities for testing
std::vector<Activity> testData = DataGenerator::generateRandomActivities(50, 100, 10, 42);

// Generate realistic course schedule
std::vector<Activity> courses = DataGenerator::generateCourseScheduleData();
```

### Performance Analysis

```cpp
namespace Performance {
    struct BenchmarkResult {
        double executionTime;
        size_t memoryUsage;
        int activitiesSelected;
        double totalWeight;
        std::string algorithmName;
    };
    
    BenchmarkResult benchmarkAlgorithm(
        std::function<std::vector<Activity>(std::vector<Activity>)> algorithm,
        const std::vector<Activity>& testData,
        const std::string& algorithmName
    );
    
    void compareAlgorithms(const std::vector<Activity>& testData);
}
```

**Example:**
```cpp
std::vector<Activity> testData = DataGenerator::generateRandomActivities(1000);

// Benchmark individual algorithm
auto greedyBenchmark = Performance::benchmarkAlgorithm(
    [](std::vector<Activity> acts) { 
        ConflictFreeScheduler s; 
        return s.greedySchedule(acts); 
    },
    testData,
    "Greedy"
);

// Compare all algorithms
Performance::compareAlgorithms(testData);
```

### Visualization

```cpp
namespace Visualization {
    void printScheduleTimeline(const std::vector<Activity>& activities,
                              const std::vector<Activity>& selected);
    
    void generateGanttChart(const std::vector<Activity>& selected,
                           const std::string& outputFile = "schedule.txt");
    
    void printAlgorithmComparison(const std::vector<Performance::BenchmarkResult>& results);
}
```

**Example:**
```cpp
ConflictFreeScheduler scheduler;
std::vector<Activity> selected = scheduler.greedySchedule(activities);

// Print visual timeline
Visualization::printScheduleTimeline(activities, selected);

// Generate text-based Gantt chart
Visualization::generateGanttChart(selected, "my_schedule.txt");
```

## Error Handling

### Custom Exceptions

```cpp
class SchedulingException : public std::exception {
public:
    explicit SchedulingException(const std::string& message) : message_(message) {}
    const char* what() const noexcept override { return message_.c_str(); }

private:
    std::string message_;
};

class InvalidInputException : public SchedulingException {
public:
    explicit InvalidInputException(const std::string& message) 
        : SchedulingException("Invalid input: " + message) {}
};

class AlgorithmTimeoutException : public SchedulingException {
public:
    explicit AlgorithmTimeoutException(int timeLimit) 
        : SchedulingException("Algorithm exceeded time limit of " + std::to_string(timeLimit) + " seconds") {}
};
```

### Error Handling Example

```cpp
try {
    ConflictFreeScheduler scheduler;
    std::vector<Activity> result = scheduler.dpSchedule(activities);
    std::cout << "Successfully scheduled " << result.size() << " activities" << std::endl;
} 
catch (const InvalidInputException& e) {
    std::cerr << "Input error: " << e.what() << std::endl;
} 
catch (const AlgorithmTimeoutException& e) {
    std::cerr << "Timeout error: " << e.what() << std::endl;
} 
catch (const std::exception& e) {
    std::cerr << "Unexpected error: " << e.what() << std::endl;
}
```

## Configuration

### Compiler Settings

```cpp
// scheduler_config.h
#ifndef SCHEDULER_CONFIG_H
#define SCHEDULER_CONFIG_H

namespace Config {
    constexpr int DEFAULT_TIME_LIMIT = 60;  // seconds
    constexpr size_t MAX_MEMORY_USAGE = 1024 * 1024 * 1024;  // 1GB
    constexpr bool ENABLE_DEBUG_OUTPUT = false;
    constexpr bool ENABLE_PERFORMANCE_PROFILING = true;
}

#endif // SCHEDULER_CONFIG_H
```

### Build Configuration

```cmake
# CMakeLists.txt options
option(ENABLE_TESTING "Build test programs" ON)
option(ENABLE_BENCHMARKING "Build benchmark programs" OFF)
option(ENABLE_VISUALIZATION "Build with visualization support" OFF)
```

---

This API reference provides complete documentation for all public interfaces in the Conflict-Free Scheduling C++ library. For implementation details and algorithm explanations, refer to the source code and algorithm documentation.
