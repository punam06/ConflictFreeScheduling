#include "greedy.h"
#include <algorithm>
#include <iostream>

// Classical greedy activity selection algorithm
std::vector<Activity> GreedyAlgorithms::activitySelection(std::vector<Activity> activities) {
    // Sort activities by end time
    std::sort(activities.begin(), activities.end(), compareByEndTime);
    
    std::vector<Activity> selected;
    if (activities.empty()) return selected;
    
    // Always select the first activity (earliest end time)
    selected.push_back(activities[0]);
    int lastSelected = 0;
    
    // Greedily select activities that don't conflict with previously selected
    for (size_t i = 1; i < activities.size(); i++) {
        if (activities[i].start >= activities[lastSelected].end) {
            selected.push_back(activities[i]);
            lastSelected = i;
        }
    }
    
    return selected;
}

// Greedy algorithm for weighted activity selection
std::vector<Activity> GreedyAlgorithms::weightedActivitySelection(std::vector<Activity> activities) {
    // Sort activities by weight/duration ratio (efficiency)
    std::sort(activities.begin(), activities.end(), compareByWeightRatio);
    
    std::vector<Activity> selected;
    
    for (const auto& activity : activities) {
        bool canAdd = true;
        
        // Check if this activity conflicts with any selected activity
        for (const auto& selectedActivity : selected) {
            if (hasConflict(activity, selectedActivity)) {
                canAdd = false;
                break;
            }
        }
        
        if (canAdd) {
            selected.push_back(activity);
        }
    }
    
    return selected;
}

// Greedy algorithm optimizing for maximum utilization
std::vector<Activity> GreedyAlgorithms::maxUtilizationSelection(std::vector<Activity> activities) {
    // Sort by duration in descending order (longest first)
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return (a.end - a.start) > (b.end - b.start);
              });
    
    std::vector<Activity> selected;
    
    for (const auto& activity : activities) {
        bool canAdd = true;
        
        // Check conflicts with selected activities
        for (const auto& selectedActivity : selected) {
            if (hasConflict(activity, selectedActivity)) {
                canAdd = false;
                break;
            }
        }
        
        if (canAdd) {
            selected.push_back(activity);
        }
    }
    
    return selected;
}

// Comparator for sorting activities by end time
bool GreedyAlgorithms::compareByEndTime(const Activity& a, const Activity& b) {
    return a.end_time < b.end_time;
}

// Comparator for sorting activities by weight/duration ratio
bool GreedyAlgorithms::compareByWeightRatio(const Activity& a, const Activity& b) {
    double ratioA = static_cast<double>(a.priority) / (a.end_time - a.start_time);
    double ratioB = static_cast<double>(b.priority) / (b.end_time - b.start_time);
    return ratioA > ratioB;
}

// Check if two activities conflict
bool GreedyAlgorithms::hasConflict(const Activity& a, const Activity& b) {
    // Activities conflict if they overlap in time
    return !(a.end_time <= b.start_time || b.end_time <= a.start_time);
}
