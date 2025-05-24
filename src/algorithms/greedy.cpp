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

// Greedy algorithm using earliest start time first
std::vector<Activity> GreedyAlgorithms::earliestStartFirst(std::vector<Activity> activities) {
    // Sort activities by start time
    std::sort(activities.begin(), activities.end(), compareByStartTime);
    
    std::vector<Activity> selected;
    if (activities.empty()) return selected;
    
    selected.push_back(activities[0]);
    
    for (size_t i = 1; i < activities.size(); i++) {
        bool canAdd = true;
        
        // Check conflicts with all selected activities
        for (const auto& selectedActivity : selected) {
            if (hasConflict(activities[i], selectedActivity)) {
                canAdd = false;
                break;
            }
        }
        
        if (canAdd) {
            selected.push_back(activities[i]);
        }
    }
    
    return selected;
}

// Greedy algorithm using shortest duration first
std::vector<Activity> GreedyAlgorithms::shortestDurationFirst(std::vector<Activity> activities) {
    // Sort activities by duration (shortest first)
    std::sort(activities.begin(), activities.end(), compareByDuration);
    
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

// Greedy algorithm using weight per unit time optimization
std::vector<Activity> GreedyAlgorithms::weightPerTimeOptimal(std::vector<Activity> activities) {
    // Sort by weight per unit time (highest efficiency first)
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  double efficiencyA = calculateWeightPerTime(a);
                  double efficiencyB = calculateWeightPerTime(b);
                  return efficiencyA > efficiencyB;
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

// Advanced greedy with look-ahead for better optimization
std::vector<Activity> GreedyAlgorithms::lookAheadGreedy(std::vector<Activity> activities, int lookAheadDepth) {
    if (activities.empty() || lookAheadDepth <= 0) {
        return activitySelection(activities); // Fall back to classical greedy
    }
    
    // Sort activities by end time for baseline
    std::sort(activities.begin(), activities.end(), compareByEndTime);
    
    std::vector<Activity> selected;
    std::vector<bool> used(activities.size(), false);
    
    for (size_t i = 0; i < activities.size(); i++) {
        if (used[i]) continue;
        
        double bestValue = 0;
        int bestChoice = -1;
        
        // Look ahead at next few activities
        for (size_t j = i; j < std::min(i + lookAheadDepth, activities.size()); j++) {
            if (used[j]) continue;
            
            // Check if this activity conflicts with selected ones
            bool conflicts = false;
            for (const auto& selectedActivity : selected) {
                if (hasConflict(activities[j], selectedActivity)) {
                    conflicts = true;
                    break;
                }
            }
            
            if (!conflicts) {
                double value = activities[j].weight;
                // Add potential future value (simplified heuristic)
                double futureValue = 0;
                for (size_t k = j + 1; k < activities.size(); k++) {
                    if (!used[k] && activities[k].start >= activities[j].end) {
                        futureValue += activities[k].weight * 0.5; // Discounted future value
                        break; // Only consider immediate next opportunity
                    }
                }
                
                double totalValue = value + futureValue;
                if (totalValue > bestValue) {
                    bestValue = totalValue;
                    bestChoice = j;
                }
            }
        }
        
        if (bestChoice != -1) {
            selected.push_back(activities[bestChoice]);
            used[bestChoice] = true;
        }
    }
    
    return selected;
}

// Comparator for sorting activities by end time
bool GreedyAlgorithms::compareByEndTime(const Activity& a, const Activity& b) {
    return a.end < b.end;
}

// Comparator for sorting activities by weight/duration ratio
bool GreedyAlgorithms::compareByWeightRatio(const Activity& a, const Activity& b) {
    double ratioA = static_cast<double>(a.weight) / (a.end - a.start);
    double ratioB = static_cast<double>(b.weight) / (b.end - b.start);
    return ratioA > ratioB;
}

// Check if two activities conflict
bool GreedyAlgorithms::hasConflict(const Activity& a, const Activity& b) {
    // Activities conflict if they overlap in time
    return !(a.end <= b.start || b.end <= a.start);
}

// Comparator for sorting activities by start time
bool GreedyAlgorithms::compareByStartTime(const Activity& a, const Activity& b) {
    return a.start < b.start;
}

// Comparator for sorting activities by duration (shortest first)
bool GreedyAlgorithms::compareByDuration(const Activity& a, const Activity& b) {
    int durationA = a.end - a.start;
    int durationB = b.end - b.start;
    return durationA < durationB;
}

// Find latest non-conflicting activity for given activity
int GreedyAlgorithms::findLatestNonConflicting(const std::vector<Activity>& activities, int index) {
    for (int i = index - 1; i >= 0; i--) {
        if (activities[i].end <= activities[index].start) {
            return i;
        }
    }
    return -1;
}

// Calculate weight per unit time for an activity
double GreedyAlgorithms::calculateWeightPerTime(const Activity& a) {
    int duration = a.end - a.start;
    return duration > 0 ? a.weight / static_cast<double>(duration) : 0.0;
}
