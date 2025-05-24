#ifndef DYNAMIC_PROGRAMMING_H
#define DYNAMIC_PROGRAMMING_H

#include "../scheduler.h"
#include <vector>
#include <algorithm>

/**
 * @brief Dynamic Programming algorithms for optimal scheduling
 * 
 * This class implements DP solutions for various scheduling optimization problems
 * including weighted activity selection and interval scheduling.
 */
class DynamicProgramming {
public:
    /**
     * @brief Weighted activity selection using dynamic programming
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities with maximum weight
     * @complexity Time: O(n^2), Space: O(n)
     */
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    
    /**
     * @brief Activity selection with limited resources (rooms/teachers)
     * @param activities Vector of activities
     * @param maxResources Maximum number of parallel activities allowed
     * @return Optimal schedule within resource constraints
     * @complexity Time: O(n^2 * k), Space: O(n * k) where k = maxResources
     */
    static std::vector<Activity> resourceConstrainedScheduling(std::vector<Activity> activities, int maxResources);

private:
    /**
     * @brief Find latest non-overlapping activity
     * @param activities Sorted activities
     * @param index Current activity index
     * @return Index of latest non-overlapping activity
     */
    static int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
    
    /**
     * @brief Recursive DP helper with memoization
     */
    static double dpHelper(
        const std::vector<Activity>& activities,
        int index,
        std::vector<double>& memo
    );
    
    /**
     * @brief Build solution from DP table
     */
    static std::vector<Activity> buildSolution(
        const std::vector<Activity>& activities,
        const std::vector<double>& dp
    );
};

#endif // DYNAMIC_PROGRAMMING_H
