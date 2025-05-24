#include "dynamic_programming.h"
#include <algorithm>
#include <iostream>
#include <climits>

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
    return reconstructSolution(activities, dp);
}

// Maximum activity selection using DP
std::vector<Activity> DynamicProgramming::maxActivitySelection(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Sort by end time
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.end < b.end;
              });
    
    int n = activities.size();
    std::vector<int> dp(n, 1);  // dp[i] = max activities ending at or before i
    std::vector<int> parent(n, -1);  // For reconstruction
    
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (activities[j].end <= activities[i].start) {
                if (dp[j] + 1 > dp[i]) {
                    dp[i] = dp[j] + 1;
                    parent[i] = j;
                }
            }
        }
    }
    
    // Find the index with maximum activities
    int maxIndex = 0;
    for (int i = 1; i < n; i++) {
        if (dp[i] > dp[maxIndex]) {
            maxIndex = i;
        }
    }
    
    // Reconstruct solution
    std::vector<Activity> result;
    int current = maxIndex;
    while (current != -1) {
        result.push_back(activities[current]);
        current = parent[current];
    }
    
    std::reverse(result.begin(), result.end());
    return result;
}

// Activity selection minimizing gaps
std::vector<Activity> DynamicProgramming::minGapSelection(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Sort by start time
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.start < b.start;
              });
    
    int n = activities.size();
    std::vector<int> dp(n, INT_MAX);  // dp[i] = minimum total gap ending with activity i
    std::vector<int> parent(n, -1);
    
    dp[0] = 0;  // No gap for first activity
    
    for (int i = 1; i < n; i++) {
        // Option 1: Start fresh with current activity
        dp[i] = 0;
        
        // Option 2: Extend from previous activities
        for (int j = 0; j < i; j++) {
            if (activities[j].end <= activities[i].start) {
                int gap = activities[i].start - activities[j].end;
                if (dp[j] + gap < dp[i]) {
                    dp[i] = dp[j] + gap;
                    parent[i] = j;
                }
            }
        }
    }
    
    // Find minimum gap solution
    int minIndex = 0;
    for (int i = 1; i < n; i++) {
        if (dp[i] < dp[minIndex]) {
            minIndex = i;
        }
    }
    
    // Reconstruct solution
    std::vector<Activity> result;
    int current = minIndex;
    while (current != -1) {
        result.push_back(activities[current]);
        current = parent[current];
    }
    
    std::reverse(result.begin(), result.end());
    return result;
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

// Reconstruct solution from DP table
std::vector<Activity> DynamicProgramming::reconstructSolution(const std::vector<Activity>& activities,
                                                              const std::vector<double>& dp) {
    std::vector<Activity> result;
    int n = activities.size();
    int i = n - 1;
    
    while (i >= 0) {
        // Check if current activity was included
        double includeCurrent = activities[i].weight;
        int latest = findLatestNonConflicting(activities, i);
        if (latest != -1) {
            includeCurrent += dp[latest];
        }
        
        double excludeCurrent = (i > 0) ? dp[i-1] : 0;
        
        if (includeCurrent >= excludeCurrent) {
            // Current activity was included
            result.push_back(activities[i]);
            i = latest;
        } else {
            // Current activity was excluded
            i--;
        }
    }
    
    std::reverse(result.begin(), result.end());
    return result;
}
