#include "dynamic_programming.h"
#include <algorithm>
#include <vector>
#include <iostream>

/**
 * @brief Solve weighted activity selection using dynamic programming
 * 
 * This implements the classic weighted activity selection problem using
 * dynamic programming. Activities are first sorted by end time, then
 * we compute the optimal weight for each prefix.
 * 
 * @param activities Vector of activities with weights
 * @return Optimal schedule with maximum total weight
 * @complexity Time: O(n log n), Space: O(n)
 */
std::vector<Activity> DynamicProgrammingScheduler::solveWeightedActivitySelection(std::vector<Activity> activities) {
    if (activities.empty()) {
        return {};
    }
    
    int n = activities.size();
    
    // Sort activities by end time
    std::sort(activities.begin(), activities.end(), 
              [](const Activity& a, const Activity& b) {
                  return a.end < b.end;
              });
    
    // dp[i] = maximum weight achievable using activities 0..i
    std::vector<double> dp(n);
    std::vector<int> parent(n, -1); // To reconstruct solution
    
    // Base case
    dp[0] = activities[0].weight;
    
    // Fill DP table
    for (int i = 1; i < n; i++) {
        // Option 1: Don't include current activity
        double withoutCurrent = dp[i - 1];
        
        // Option 2: Include current activity
        double withCurrent = activities[i].weight;
        int latest = findLatestNonConflicting(activities, i);
        
        if (latest != -1) {
            withCurrent += dp[latest];
        }
        
        // Choose the better option
        if (withCurrent > withoutCurrent) {
            dp[i] = withCurrent;
            parent[i] = latest;
        } else {
            dp[i] = withoutCurrent;
            parent[i] = i - 1; // Mark as "don't include"
        }
    }
    
    // Reconstruct the optimal solution
    std::vector<Activity> result;
    int current = n - 1;
    
    while (current >= 0) {
        if (current == 0 || dp[current] != dp[current - 1]) {
            // This activity is included in the optimal solution
            result.push_back(activities[current]);
            current = parent[current];
        } else {
            // This activity is not included
            current--;
        }
    }
    
    // Reverse to get correct order
    std::reverse(result.begin(), result.end());
    
    return result;
}

/**
 * @brief Find the latest non-conflicting activity
 * 
 * Uses binary search to find the latest activity that ends before
 * the current activity starts.
 * 
 * @param activities Sorted activities by end time
 * @param index Current activity index
 * @return Index of latest non-conflicting activity, -1 if none
 */
int DynamicProgrammingScheduler::findLatestNonConflicting(const std::vector<Activity>& activities, int index) {
    int start = activities[index].start;
    
    // Binary search for the latest activity that ends before current starts
    int left = 0, right = index - 1;
    int result = -1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (activities[mid].end <= start) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return result;
}

/**
 * @brief Check if two activities have a time conflict
 * 
 * @param a1 First activity
 * @param a2 Second activity
 * @return true if activities overlap in time, false otherwise
 */
bool DynamicProgrammingScheduler::hasConflict(const Activity& a1, const Activity& a2) {
    return !(a1.end <= a2.start || a2.end <= a1.start);
}