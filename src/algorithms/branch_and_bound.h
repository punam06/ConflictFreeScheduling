#ifndef BRANCH_AND_BOUND_H
#define BRANCH_AND_BOUND_H

#include "../scheduler.h"
#include <vector>
#include <queue>
#include <algorithm>

/**
 * @brief Branch and Bound algorithms for optimal conflict-free scheduling
 */
class BranchAndBound {
public:
    /**
     * @brief Branch and bound solution for optimal weighted activity selection
     * @param activities Vector of activities to schedule
     * @return Vector of selected activities with optimal weight
     * @complexity Time: O(2^n) worst case, Space: O(n)
     */
    static std::vector<Activity> optimalWeightedSelection(std::vector<Activity> activities);
    
    /**
     * @brief Branch and bound for maximum activities with constraints
     * @param activities Vector of activities to schedule
     * @param maxActivities Maximum number of activities allowed
     * @return Vector of selected activities within constraints
     * @complexity Time: O(2^n) worst case, Space: O(n)
     */
    static std::vector<Activity> constrainedSelection(std::vector<Activity> activities, 
                                                      int maxActivities);
    
    /**
     * @brief Branch and bound for multi-resource scheduling
     * @param activities Vector of activities to schedule
     * @param resources Number of available resources
     * @return Vector of selected activities using available resources
     * @complexity Time: O(2^n) worst case, Space: O(n)
     */
    static std::vector<Activity> multiResourceSelection(std::vector<Activity> activities, 
                                                        int resources);

private:
    /**
     * @brief Node structure for branch and bound tree
     */
    struct BBNode {
        int level;              // Current level in decision tree
        double profit;          // Current profit
        double bound;           // Upper bound of profit
        std::vector<bool> taken; // Which activities are taken
        
        BBNode(int level, double profit, double bound, const std::vector<bool>& taken)
            : level(level), profit(profit), bound(bound), taken(taken) {}
        
        // For priority queue (max heap based on bound)
        bool operator<(const BBNode& other) const {
            return bound < other.bound;
        }
    };
    
    /**
     * @brief Calculate upper bound for branch and bound
     */
    static double calculateBound(const std::vector<Activity>& activities, 
                                 const std::vector<bool>& taken, int level);
    
    /**
     * @brief Check if current selection is feasible (no conflicts)
     */
    static bool isFeasible(const std::vector<Activity>& activities, 
                           const std::vector<bool>& taken);
    
    /**
     * @brief Calculate total weight of selected activities
     */
    static double calculateProfit(const std::vector<Activity>& activities, 
                                  const std::vector<bool>& taken);
    
    /**
     * @brief Check if two activities conflict
     */
    static bool hasConflict(const Activity& a, const Activity& b);
};

#endif // BRANCH_AND_BOUND_H
