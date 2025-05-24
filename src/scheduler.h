#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <vector>
#include <algorithm>
#include <iostream>

/**
 * @brief Structure representing an activity/task with start and end times
 */
struct Activity {
    int id;
    int start;
    int end;
    double weight = 1.0;  // Default weight for unweighted problems
    
    Activity(int id, int start, int end) : id(id), start(start), end(end) {}
    Activity(int id, int start, int end, double weight) 
        : id(id), start(start), end(end), weight(weight) {}
};

/**
 * @brief Structure representing a task with additional metadata
 */
struct Task {
    int id;
    int start;
    int end;
    std::string name;
    std::string room;
    
    Task(int id, int start, int end) : id(id), start(start), end(end) {}
    Task(int id, int start, int end, const std::string& name, const std::string& room)
        : id(id), start(start), end(end), name(name), room(room) {}
};

/**
 * @brief Main class for conflict-free scheduling algorithms
 * Simplified to focus on 4 core algorithms:
 * 1. Graph Coloring - For conflict resolution using graph theory
 * 2. Dynamic Programming - For optimal weighted activity selection
 * 3. Backtracking - For exhaustive optimal solutions
 * 4. Genetic Algorithm - For evolutionary optimization
 */
class ConflictFreeScheduler {
public:
    ConflictFreeScheduler() = default;
    ~ConflictFreeScheduler() = default;
    
    // Core Algorithm 1: Graph Coloring
    std::vector<Activity> graphColoringSchedule(std::vector<Activity> activities);
    
    // Core Algorithm 2: Dynamic Programming
    std::vector<Activity> dpSchedule(std::vector<Activity> activities);
    
    // Core Algorithm 3: Backtracking
    std::vector<Activity> backtrackingSchedule(std::vector<Activity> activities);
    
    // Core Algorithm 4: Genetic Algorithm
    std::vector<Activity> geneticAlgorithmSchedule(std::vector<Activity> activities);
    
    // Utility functions
    bool hasConflict(const Activity& a1, const Activity& a2) const;
    double calculateTotalWeight(const std::vector<Activity>& activities) const;
    void printSchedule(const std::vector<Activity>& schedule) const;
    
private:
    // Helper functions
    void sortByEndTime(std::vector<Activity>& activities);
    void sortByStartTime(std::vector<Activity>& activities);
    int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
};

#endif // SCHEDULER_H
