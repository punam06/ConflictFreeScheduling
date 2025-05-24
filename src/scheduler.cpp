#include "scheduler.h"
#include "algorithms/greedy.h"
#include "algorithms/dynamic_programming.h"
#include "algorithms/branch_and_bound.h"
#include <algorithm>
#include <iostream>

// Greedy algorithms
std::vector<Activity> ConflictFreeScheduler::greedySchedule(std::vector<Activity> activities) {
    return GreedyAlgorithms::activitySelection(activities);
}

std::vector<int> ConflictFreeScheduler::greedyActivitySelection(std::vector<Activity> activities) {
    auto selected = GreedyAlgorithms::activitySelection(activities);
    std::vector<int> result;
    for (const auto& activity : selected) {
        result.push_back(activity.id);
    }
    return result;
}

std::vector<Activity> ConflictFreeScheduler::greedyWeightedSchedule(std::vector<Activity> activities) {
    return GreedyAlgorithms::weightedActivitySelection(activities);
}

// Dynamic Programming algorithms
std::vector<Activity> ConflictFreeScheduler::dpSchedule(std::vector<Activity> activities) {
    return DynamicProgramming::weightedActivitySelection(activities);
}

std::vector<Activity> ConflictFreeScheduler::dpWeightedSchedule(std::vector<Activity> activities) {
    return DynamicProgramming::weightedActivitySelection(activities);
}

// Branch and Bound algorithms
std::vector<Activity> ConflictFreeScheduler::branchAndBoundSchedule(std::vector<Activity> activities) {
    return BranchAndBound::optimalWeightedSelection(activities);
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
