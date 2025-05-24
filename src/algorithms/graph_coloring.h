#ifndef GRAPH_COLORING_H
#define GRAPH_COLORING_H

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

#endif // GRAPH_COLORING_H
