#ifndef GREEDY_H
#define GREEDY_H

#include "../scheduler.h"
#include <vector>
#include <algorithm>

/**
 * @brief Greedy algorithms for conflict-free scheduling
 */
class GreedyAlgorithms {
public:
    /**
     * @brief Classical greedy activity selection algorithm
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities that don't conflict
     * @complexity Time: O(n log n), Space: O(1)
     */
    static std::vector<Activity> activitySelection(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm for weighted activity selection
     * @param activities Vector of weighted activities
     * @return Vector of selected activities maximizing total weight
     * @complexity Time: O(n log n), Space: O(1)
     */
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    
    /**
     * @brief Greedy algorithm optimizing for maximum utilization
     * @param activities Vector of activities with different durations
     * @return Vector of activities maximizing time utilization
     */
    static std::vector<Activity> maxUtilizationSelection(std::vector<Activity> activities);

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
};

#endif // GREEDY_H
