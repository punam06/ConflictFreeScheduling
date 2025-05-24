#ifndef GREEDY_H
#define GREEDY_H

#include "../scheduler.h"
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>

/**
 * @brief Graph Coloring Algorithm for Conflict-Free Scheduling
 * 
 * This class implements graph coloring to solve scheduling conflicts.
 * Each activity is a vertex, conflicts are edges, and colors represent time slots.
 */
class GraphColoringScheduler {
public:
    /**
     * @brief Solve scheduling using graph coloring (greedy approach)
     * @param activities Vector of activities to schedule
     * @return Vector of scheduled activities with assigned time slots
     * @complexity Time: O(V²), Space: O(V)
     */
    static std::vector<Activity> coloringSchedule(std::vector<Activity> activities);
    
    /**
     * @brief Welsh-Powell graph coloring algorithm
     * @param activities Vector of activities
     * @return Minimum number of colors (time slots) needed
     */
    static int welshPowellColoring(std::vector<Activity> activities);

private:
    /**
     * @brief Build conflict graph from activities
     * @param activities Vector of activities
     * @return Adjacency list representation of conflict graph
     */
    static std::unordered_map<int, std::vector<int>> buildConflictGraph(const std::vector<Activity>& activities);
    
    /**
     * @brief Check if two activities conflict in time
     */
    static bool hasTimeConflict(const Activity& a1, const Activity& a2);
    
    /**
     * @brief Assign colors using greedy approach
     */
    static std::unordered_map<int, int> assignColors(
        const std::vector<Activity>& activities,
        const std::unordered_map<int, std::vector<int>>& graph
    );
};
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm optimizing for maximum utilization
     * @param activities Vector of activities with different durations
     * @return Vector of activities maximizing time utilization
     */
    static std::vector<Activity> maxUtilizationSelection(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm using earliest start time first
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities with earliest start preference
     * @complexity Time: O(n log n), Space: O(1)
     */
    static std::vector<Activity> earliestStartFirst(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm using shortest duration first
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities prioritizing shorter durations
     * @complexity Time: O(n log n), Space: O(1)
     */
    static std::vector<Activity> shortestDurationFirst(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm using weight per unit time optimization
     * @param activities Vector of weighted activities
     * @return Vector of activities maximizing weight per unit time
     * @complexity Time: O(n log n), Space: O(1)
     */
    static std::vector<Activity> weightPerTimeOptimal(std::vector<Activity> activities);
    
    /**
     * @brief Advanced greedy with look-ahead for better optimization
     * @param activities Vector of activities to schedule
     * @param lookAheadDepth Depth of look-ahead (default: 2)
     * @return Vector of selected activities with local optimization
     * @complexity Time: O(n² * d), Space: O(1) where d is look-ahead depth
     */
    static std::vector<Activity> lookAheadGreedy(std::vector<Activity> activities, int lookAheadDepth = 2);

private:
    /**
     * @brief Comparator for sorting activities by end time
     */
    static bool compareByEndTime(const Activity& a, const Activity& b);
    
    /**
     * @brief Comparator for sorting activities by weight/duration ratio
     */
    static bool compareByWeightRatio(const Activity& a, const Activity& b);
    
    /**
     * @brief Check if two activities conflict
     */
    static bool hasConflict(const Activity& a, const Activity& b);
    
    /**
     * @brief Comparator for sorting activities by start time
     */
    static bool compareByStartTime(const Activity& a, const Activity& b);
    
    /**
     * @brief Comparator for sorting activities by duration (shortest first)
     */
    static bool compareByDuration(const Activity& a, const Activity& b);
    
    /**
     * @brief Find latest non-conflicting activity for given activity
     */
    static int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
    
    /**
     * @brief Calculate weight per unit time for an activity
     */
    static double calculateWeightPerTime(const Activity& a);
};

#endif // GREEDY_H
