#include "scheduler.h"
#include "algorithms/graph_coloring.h"
#include "algorithms/dynamic_programming.h"
#include "algorithms/backtracking.h"
#include "algorithms/genetic_algorithm.h"
#include <algorithm>
#include <iostream>

// Core Algorithm 1: Graph Coloring
std::vector<Activity> ConflictFreeScheduler::graphColoringSchedule(std::vector<Activity> activities) {
    return GraphColoringScheduler::coloringSchedule(activities);
}

// Core Algorithm 2: Dynamic Programming
std::vector<Activity> ConflictFreeScheduler::dpSchedule(std::vector<Activity> activities) {
    return DynamicProgramming::weightedActivitySelection(activities);
}

// Core Algorithm 3: Backtracking
std::vector<Activity> ConflictFreeScheduler::backtrackingSchedule(std::vector<Activity> activities) {
    return BacktrackingScheduler::optimalSchedule(activities);
}

// Core Algorithm 4: Genetic Algorithm
std::vector<Activity> ConflictFreeScheduler::geneticAlgorithmSchedule(std::vector<Activity> activities) {
    GeneticAlgorithmScheduler::GAConfig config(50, 200, 0.8, 0.1, 5); // Simplified config
    return GeneticAlgorithmScheduler::evolveSchedule(activities, config);
}

// Utility functions
bool ConflictFreeScheduler::hasConflict(const Activity& a1, const Activity& a2) const {
    return !(a1.end <= a2.start || a2.end <= a1.start);
}

double ConflictFreeScheduler::calculateTotalWeight(const std::vector<Activity>& activities) const {
    double total = 0.0;
    for (const auto& activity : activities) {
        total += activity.weight;
    }
    return total;
}

void ConflictFreeScheduler::printSchedule(const std::vector<Activity>& schedule) const {
    std::cout << "\nScheduled Activities:\n";
    std::cout << "ID\tStart\tEnd\tWeight\n";
    std::cout << "------------------------\n";
    for (const auto& activity : schedule) {
        std::cout << activity.id << "\t" << activity.start << "\t" 
                  << activity.end << "\t" << activity.weight << "\n";
    }
    std::cout << "Total Weight: " << calculateTotalWeight(schedule) << "\n";
    std::cout << "Total Activities: " << schedule.size() << "\n\n";
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
