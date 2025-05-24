#ifndef DYNAMIC_PROGRAMMING_H
#define DYNAMIC_PROGRAMMING_H

#include "../scheduler.h"
#include <vector>
#include <algorithm>

/**
 * @brief Dynamic Programming for Weighted Activity Selection
 * 
 * This class implements the classic weighted activity selection problem
 * using dynamic programming to find the optimal schedule with maximum weight.
 */
class DynamicProgrammingScheduler {
public:
    /**
     * @brief Solve weighted activity selection problem
     * @param activities Vector of activities with weights
     * @return Optimal schedule with maximum total weight
     * @complexity Time: O(n log n), Space: O(n)
     */
    static std::vector<Activity> solveWeightedActivitySelection(std::vector<Activity> activities);

private:
    /**
     * @brief Find latest non-conflicting activity
     * @param activities Sorted activities by end time
     * @param index Current activity index
     * @return Index of latest non-conflicting activity, -1 if none
     */
    static int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
    
    /**
     * @brief Check if two activities overlap in time
     */
    static bool hasConflict(const Activity& a1, const Activity& a2);
};

#endif // DYNAMIC_PROGRAMMING_H