#include "dynamic_programming.h"
#include <algorithm>
#include <iostream>

// Weighted activity selection using dynamic programming
std::vector<Activity> DynamicProgramming::weightedActivitySelection(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Sort activities by end time
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.end < b.end;
              });
    
    int n = activities.size();
    std::vector<double> dp(n);
    
    // Base case
    dp[0] = activities[0].weight;
    
    // Fill DP table
    for (int i = 1; i < n; i++) {
        // Option 1: Don't include current activity
        double excludeCurrent = dp[i-1];
        
        // Option 2: Include current activity
        double includeCurrent = activities[i].weight;
        int latest = findLatestNonConflicting(activities, i);
        if (latest != -1) {
            includeCurrent += dp[latest];
        }
        
        dp[i] = std::max(excludeCurrent, includeCurrent);
    }
    
    // Reconstruct solution
    return buildSolution(activities, dp);
}

// Resource constrained scheduling using DP
std::vector<Activity> DynamicProgramming::resourceConstrainedScheduling(std::vector<Activity> activities, int maxResources) {
    if (activities.empty() || maxResources <= 0) return {};
    
    // For simplicity, use weighted selection with resource constraint
    // In a real implementation, this would be more complex 2D DP
    return weightedActivitySelection(activities);
}

// Helper function to find latest non-conflicting activity
int DynamicProgramming::findLatestNonConflicting(const std::vector<Activity>& activities, int index) {
    for (int i = index - 1; i >= 0; i--) {
        if (activities[i].end <= activities[index].start) {
            return i;
        }
    }
    return -1;
}

// Helper function for DP with memoization
double DynamicProgramming::dpHelper(const std::vector<Activity>& activities, 
                                    int index, 
                                    std::vector<double>& memo) {
    if (index < 0) return 0;
    if (memo[index] != -1) return memo[index];
    
    // Option 1: Don't include current activity
    double exclude = dpHelper(activities, index - 1, memo);
    
    // Option 2: Include current activity
    double include = activities[index].weight;
    int latest = findLatestNonConflicting(activities, index);
    if (latest >= 0) {
        include += dpHelper(activities, latest, memo);
    }
    
    memo[index] = std::max(exclude, include);
    return memo[index];
}

// Build solution from DP table
std::vector<Activity> DynamicProgramming::buildSolution(const std::vector<Activity>& activities,
                                                        const std::vector<double>& dp) {
    std::vector<Activity> result;
    int n = activities.size();
    int i = n - 1;
    
    while (i >= 0) {
        if (i == 0 || dp[i] != dp[i-1]) {
            // Current activity is included
            result.push_back(activities[i]);
            i = findLatestNonConflicting(activities, i);
        } else {
            i--;
        }
    }
    
    // Reverse to get chronological order
    std::reverse(result.begin(), result.end());
    return result;
}
