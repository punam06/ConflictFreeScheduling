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
    
    /**
     * @brief Enhanced branch and bound with intelligent pruning
     * @param activities Vector of activities to schedule
     * @param pruningFactor Aggressiveness of pruning (0.0-1.0)
     * @return Vector of optimally selected activities
     * @complexity Time: Improved O(2^n), Space: O(n)
     */
    static std::vector<Activity> enhancedOptimalSelection(std::vector<Activity> activities,
                                                          double pruningFactor = 0.8);
    
    /**
     * @brief Branch and bound with time complexity bounds
     * @param activities Vector of activities to schedule
     * @param maxIterations Maximum iterations allowed
     * @return Vector of best found activities within time limit
     * @complexity Time: O(maxIterations), Space: O(n)
     */
    static std::vector<Activity> boundedTimeSelection(std::vector<Activity> activities,
                                                      int maxIterations = 100000);
    
    /**
     * @brief Parallel branch and bound (simulated)
     * @param activities Vector of activities to schedule
     * @param numThreads Number of simulated parallel threads
     * @return Vector of optimally selected activities
     * @complexity Time: O(2^n / threads), Space: O(n * threads)
     */
    static std::vector<Activity> parallelOptimalSelection(std::vector<Activity> activities,
                                                          int numThreads = 4);
    
    /**
     * @brief Branch and bound with heuristic ordering
     * @param activities Vector of activities to schedule
     * @return Vector of optimally selected activities with smart ordering
     * @complexity Time: Improved average case, Space: O(n)
     */
    static std::vector<Activity> heuristicOptimalSelection(std::vector<Activity> activities);

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
    
    /**
     * @brief Enhanced bound calculation with better heuristics
     */
    static double calculateEnhancedBound(const std::vector<Activity>& activities,
                                         const std::vector<bool>& taken, int level,
                                         double pruningFactor);
    
    /**
     * @brief Smart activity ordering for better pruning
     */
    static std::vector<Activity> orderActivitiesHeuristically(std::vector<Activity> activities);
    
    /**
     * @brief Calculate fractional knapsack bound for activities
     */
    static double fractionalBound(const std::vector<Activity>& activities,
                                  const std::vector<bool>& taken, int level);
    
    /**
     * @brief Simulate parallel processing by dividing search space
     */
    static std::vector<Activity> processSearchSpace(const std::vector<Activity>& activities,
                                                    int startLevel, int endLevel);
    
    /**
     * @brief Priority-based node expansion
     */
    static double calculateNodePriority(const BBNode& node, 
                                        const std::vector<Activity>& activities);
};

#endif // BRANCH_AND_BOUND_H
