#include "branch_and_bound.h"
#include <queue>
#include <algorithm>
#include <iostream>

// Optimal weighted activity selection using branch and bound
std::vector<Activity> BranchAndBound::optimalWeightedSelection(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Sort activities by weight/duration ratio for better bounds
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  double ratioA = a.weight / (a.end - a.start);
                  double ratioB = b.weight / (b.end - b.start);
                  return ratioA > ratioB;
              });
    
    int n = activities.size();
    std::priority_queue<BBNode> pq;
    
    // Initialize root node
    std::vector<bool> initialTaken(n, false);
    double initialBound = calculateBound(activities, initialTaken, -1);
    pq.push(BBNode(-1, 0.0, initialBound, initialTaken));
    
    double maxProfit = 0.0;
    std::vector<bool> bestSolution(n, false);
    
    while (!pq.empty()) {
        BBNode current = pq.top();
        pq.pop();
        
        // Prune if bound is not better than current best
        if (current.bound <= maxProfit) {
            continue;
        }
        
        int level = current.level + 1;
        
        // If we've processed all activities
        if (level >= n) {
            if (current.profit > maxProfit) {
                maxProfit = current.profit;
                bestSolution = current.taken;
            }
            continue;
        }
        
        // Branch 1: Include current activity
        std::vector<bool> includeTaken = current.taken;
        includeTaken[level] = true;
        
        if (isFeasible(activities, includeTaken)) {
            double includeProfit = current.profit + activities[level].weight;
            double includeBound = calculateBound(activities, includeTaken, level);
            
            if (includeBound > maxProfit) {
                pq.push(BBNode(level, includeProfit, includeBound, includeTaken));
            }
        }
        
        // Branch 2: Exclude current activity
        std::vector<bool> excludeTaken = current.taken;
        excludeTaken[level] = false;
        double excludeProfit = current.profit;
        double excludeBound = calculateBound(activities, excludeTaken, level);
        
        if (excludeBound > maxProfit) {
            pq.push(BBNode(level, excludeProfit, excludeBound, excludeTaken));
        }
    }
    
    // Construct result from best solution
    std::vector<Activity> result;
    for (int i = 0; i < n; i++) {
        if (bestSolution[i]) {
            result.push_back(activities[i]);
        }
    }
    
    return result;
}

// Constrained activity selection
std::vector<Activity> BranchAndBound::constrainedSelection(std::vector<Activity> activities, 
                                                           int maxActivities) {
    if (activities.empty() || maxActivities <= 0) return {};
    
    // Sort by weight in descending order
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.weight > b.weight;
              });
    
    int n = activities.size();
    std::priority_queue<BBNode> pq;
    
    std::vector<bool> initialTaken(n, false);
    double initialBound = calculateBound(activities, initialTaken, -1);
    pq.push(BBNode(-1, 0.0, initialBound, initialTaken));
    
    double maxProfit = 0.0;
    std::vector<bool> bestSolution(n, false);
    
    while (!pq.empty()) {
        BBNode current = pq.top();
        pq.pop();
        
        if (current.bound <= maxProfit) continue;
        
        int level = current.level + 1;
        if (level >= n) {
            if (current.profit > maxProfit) {
                maxProfit = current.profit;
                bestSolution = current.taken;
            }
            continue;
        }
        
        // Count currently selected activities
        int selectedCount = 0;
        for (int i = 0; i <= current.level; i++) {
            if (current.taken[i]) selectedCount++;
        }
        
        // Branch 1: Include current activity (if within limit)
        if (selectedCount < maxActivities) {
            std::vector<bool> includeTaken = current.taken;
            includeTaken[level] = true;
            
            if (isFeasible(activities, includeTaken)) {
                double includeProfit = current.profit + activities[level].weight;
                double includeBound = calculateBound(activities, includeTaken, level);
                
                if (includeBound > maxProfit) {
                    pq.push(BBNode(level, includeProfit, includeBound, includeTaken));
                }
            }
        }
        
        // Branch 2: Exclude current activity
        std::vector<bool> excludeTaken = current.taken;
        excludeTaken[level] = false;
        double excludeProfit = current.profit;
        double excludeBound = calculateBound(activities, excludeTaken, level);
        
        if (excludeBound > maxProfit) {
            pq.push(BBNode(level, excludeProfit, excludeBound, excludeTaken));
        }
    }
    
    // Construct result
    std::vector<Activity> result;
    for (int i = 0; i < n; i++) {
        if (bestSolution[i]) {
            result.push_back(activities[i]);
        }
    }
    
    return result;
}

// Multi-resource scheduling
std::vector<Activity> BranchAndBound::multiResourceSelection(std::vector<Activity> activities, 
                                                             int resources) {
    // For simplicity, this implementation assumes activities can run in parallel
    // if there are enough resources and no time conflicts
    
    if (activities.empty() || resources <= 0) return {};
    
    // Sort by efficiency (weight/duration)
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  double effA = a.weight / (a.end - a.start);
                  double effB = b.weight / (b.end - b.start);
                  return effA > effB;
              });
    
    std::vector<Activity> result;
    std::vector<std::vector<Activity>> resourceSchedules(resources);
    
    for (const auto& activity : activities) {
        // Find a resource that can accommodate this activity
        for (int r = 0; r < resources; r++) {
            bool canSchedule = true;
            
            // Check conflicts with activities on this resource
            for (const auto& scheduled : resourceSchedules[r]) {
                if (hasConflict(activity, scheduled)) {
                    canSchedule = false;
                    break;
                }
            }
            
            if (canSchedule) {
                resourceSchedules[r].push_back(activity);
                result.push_back(activity);
                break;
            }
        }
    }
    
    return result;
}

// Calculate upper bound for branch and bound
double BranchAndBound::calculateBound(const std::vector<Activity>& activities, 
                                      const std::vector<bool>& taken, int level) {
    double bound = 0.0;
    
    // Add profit of already taken activities
    for (int i = 0; i <= level; i++) {
        if (taken[i]) {
            bound += activities[i].weight;
        }
    }
    
    // Add fractional knapsack bound for remaining activities
    // (This is a simplification - more sophisticated bounds could be used)
    for (int i = level + 1; i < (int)activities.size(); i++) {
        bound += activities[i].weight * 0.5; // Assume 50% chance of inclusion
    }
    
    return bound;
}

// Check if current selection is feasible
bool BranchAndBound::isFeasible(const std::vector<Activity>& activities, 
                                 const std::vector<bool>& taken) {
    std::vector<Activity> selected;
    
    for (int i = 0; i < (int)activities.size(); i++) {
        if (taken[i]) {
            selected.push_back(activities[i]);
        }
    }
    
    // Check all pairs for conflicts
    for (size_t i = 0; i < selected.size(); i++) {
        for (size_t j = i + 1; j < selected.size(); j++) {
            if (hasConflict(selected[i], selected[j])) {
                return false;
            }
        }
    }
    
    return true;
}

// Calculate total profit
double BranchAndBound::calculateProfit(const std::vector<Activity>& activities, 
                                       const std::vector<bool>& taken) {
    double profit = 0.0;
    for (int i = 0; i < (int)activities.size(); i++) {
        if (taken[i]) {
            profit += activities[i].weight;
        }
    }
    return profit;
}

// Check if two activities conflict
bool BranchAndBound::hasConflict(const Activity& a, const Activity& b) {
    return !(a.end <= b.start || b.end <= a.start);
}
