#ifndef DYNAMIC_PROGRAMMING_H
#define DYNAMIC_PROGRAMMING_H

#include "../scheduler.h"
#include <vector>
#include <algorithm>

/**
 * @brief Dynamic Programming algorithms for conflict-free scheduling
 */
class DynamicProgramming {
public:
    /**
     * @brief Dynamic programming solution for weighted activity selection
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities with maximum weight
     * @complexity Time: O(n²), Space: O(n)
     */
    static std::vector<Activity> weightedActivitySelection(std::vector<Activity> activities);
    
    /**
     * @brief Dynamic programming solution for interval scheduling maximization
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities with maximum count
     * @complexity Time: O(n log n), Space: O(n)
     */
    static std::vector<Activity> maxActivitySelection(std::vector<Activity> activities);
    
    /**
     * @brief DP solution for activity selection with minimum gaps
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities minimizing gaps
     * @complexity Time: O(n²), Space: O(n)
     */
    static std::vector<Activity> minGapSelection(std::vector<Activity> activities);

private:
    /**
     * @brief Find the latest activity that doesn't conflict with current activity
     */
    static int findLatestNonConflicting(const std::vector<Activity>& activities, int index);
    
    /**
     * @brief Helper function for weighted activity selection
     */
    static double dpWeightedHelper(const std::vector<Activity>& activities, 
                                   std::vector<double>& memo, int index);
    
    /**
     * @brief Reconstruct solution from DP table
     */
    static std::vector<Activity> reconstructSolution(const std::vector<Activity>& activities,
                                                     const std::vector<double>& memo);
};

#endif // DYNAMIC_PROGRAMMING_H
