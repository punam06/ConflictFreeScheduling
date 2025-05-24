#include "backtracking.h"
#include <algorithm>
#include <iostream>

std::vector<Activity> BacktrackingScheduler::optimalSchedule(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Sort activities by weight (descending) for better pruning
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.weight > b.weight;
              });
    
    std::vector<Activity> current;
    std::vector<Activity> best;
    
    backtrack(activities, current, 0, best);
    
    return best;
}

std::vector<std::vector<Activity>> BacktrackingScheduler::allValidSchedules(std::vector<Activity> activities) {
    std::vector<std::vector<Activity>> allSchedules;
    std::vector<Activity> current;
    
    findAllSchedules(activities, current, 0, allSchedules);
    
    return allSchedules;
}

void BacktrackingScheduler::backtrack(
    const std::vector<Activity>& activities,
    std::vector<Activity>& current,
    size_t index,
    std::vector<Activity>& best) {
    
    // Base case: processed all activities
    if (index == activities.size()) {
        if (calculateWeight(current) > calculateWeight(best)) {
            best = current;
        }
        return;
    }
    
    // Pruning: if even adding all remaining activities can't beat current best
    double currentWeight = calculateWeight(current);
    double maxPossibleWeight = currentWeight;
    for (size_t i = index; i < activities.size(); i++) {
        maxPossibleWeight += activities[i].weight;
    }
    
    if (maxPossibleWeight <= calculateWeight(best)) {
        return; // Prune this branch
    }
    
    // Try including the current activity
    if (isValidAddition(current, activities[index])) {
        current.push_back(activities[index]);
        backtrack(activities, current, index + 1, best);
        current.pop_back(); // Backtrack
    }
    
    // Try excluding the current activity
    backtrack(activities, current, index + 1, best);
}

bool BacktrackingScheduler::isValidAddition(const std::vector<Activity>& current, const Activity& newActivity) {
    for (const auto& activity : current) {
        // Check for time conflicts
        if (!(activity.end <= newActivity.start || newActivity.end <= activity.start)) {
            return false;
        }
    }
    return true;
}

double BacktrackingScheduler::calculateWeight(const std::vector<Activity>& activities) {
    double total = 0.0;
    for (const auto& activity : activities) {
        total += activity.weight;
    }
    return total;
}

void BacktrackingScheduler::findAllSchedules(
    const std::vector<Activity>& activities,
    std::vector<Activity>& current,
    size_t index,
    std::vector<std::vector<Activity>>& allSchedules) {
    
    // Base case: processed all activities
    if (index == activities.size()) {
        if (!current.empty()) {
            allSchedules.push_back(current);
        }
        return;
    }
    
    // Try including the current activity
    if (isValidAddition(current, activities[index])) {
        current.push_back(activities[index]);
        findAllSchedules(activities, current, index + 1, allSchedules);
        current.pop_back(); // Backtrack
    }
    
    // Try excluding the current activity
    findAllSchedules(activities, current, index + 1, allSchedules);
}
