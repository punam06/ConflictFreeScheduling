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
 */
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
    
private:
    // Helper functions
    void sortByEndTime(std::vector<Activity>& activities);
    void sortByStartTime(std::vector<Activity>& activities);
    int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
};

#endif // SCHEDULER_H
