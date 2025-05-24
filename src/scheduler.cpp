#include "scheduler.h"
#include "algorithms/graph_coloring.h"
#include "algorithms/dynamic_programming.h"
#include "algorithms/backtracking.h"
#include "algorithms/genetic_algorithm.h"
#include <iostream>
#include <iomanip>
#include <chrono>

// Core Algorithm 1: Graph Coloring
std::vector<Activity> ConflictFreeScheduler::graphColoringSchedule(std::vector<Activity> activities) {
    return GraphColoringScheduler::coloringSchedule(activities);
}

// Core Algorithm 2: Dynamic Programming
std::vector<Activity> ConflictFreeScheduler::dpSchedule(std::vector<Activity> activities) {
    return DynamicProgrammingScheduler::solveWeightedActivitySelection(activities);
}

// Core Algorithm 3: Backtracking
std::vector<Activity> ConflictFreeScheduler::backtrackingSchedule(std::vector<Activity> activities) {
    return BacktrackingScheduler::optimalSchedule(activities);
}

// Core Algorithm 4: Genetic Algorithm
std::vector<Activity> ConflictFreeScheduler::geneticAlgorithmSchedule(std::vector<Activity> activities) {
    GeneticAlgorithmScheduler::GAConfig config(50, 100, 0.8, 0.1, 5); // Small config for quick results
    return GeneticAlgorithmScheduler::evolveSchedule(activities, config);
}

// Utility functions
bool ConflictFreeScheduler::hasConflict(const Activity& a1, const Activity& a2) const {
    return !(a1.end <= a2.start || a2.end <= a1.start);
}

double ConflictFreeScheduler::calculateTotalWeight(const std::vector<Activity>& activities) const {
    double totalWeight = 0.0;
    for (const auto& activity : activities) {
        totalWeight += activity.weight;
    }
    return totalWeight;
}

void ConflictFreeScheduler::printSchedule(const std::vector<Activity>& schedule) const {
    if (schedule.empty()) {
        std::cout << "No activities scheduled." << std::endl;
        return;
    }
    
    std::cout << "\n=== SCHEDULED ACTIVITIES ===" << std::endl;
    std::cout << std::setw(5) << "ID" 
              << std::setw(8) << "Start" 
              << std::setw(8) << "End" 
              << std::setw(10) << "Duration"
              << std::setw(10) << "Weight" << std::endl;
    std::cout << std::string(41, '-') << std::endl;
    
    for (const auto& activity : schedule) {
        int duration = activity.end - activity.start;
        std::cout << std::setw(5) << activity.id
                  << std::setw(8) << activity.start
                  << std::setw(8) << activity.end
                  << std::setw(10) << duration
                  << std::setw(10) << std::fixed << std::setprecision(1) << activity.weight
                  << std::endl;
    }
    
    std::cout << std::string(41, '-') << std::endl;
    std::cout << "Total Activities: " << schedule.size() << std::endl;
    std::cout << "Total Weight: " << std::fixed << std::setprecision(2) 
              << calculateTotalWeight(schedule) << std::endl;
}

// Helper functions
void ConflictFreeScheduler::sortByEndTime(std::vector<Activity>& activities) {
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.end < b.end;
              });
}

void ConflictFreeScheduler::sortByStartTime(std::vector<Activity>& activities) {
    std::sort(activities.begin(), activities.end(),
              [](const Activity& a, const Activity& b) {
                  return a.start < b.start;
              });
}

int ConflictFreeScheduler::findLatestNonConflicting(const std::vector<Activity>& activities, int index) {
    for (int i = index - 1; i >= 0; i--) {
        if (activities[i].end <= activities[index].start) {
            return i;
        }
    }
    return -1;
}