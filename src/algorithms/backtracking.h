#ifndef BACKTRACKING_H
#define BACKTRACKING_H

#include "../scheduler.h"
#include <vector>
#include <unordered_set>

/**
 * @brief Backtracking Algorithm for Optimal Scheduling
 * 
 * This class implements backtracking to find optimal scheduling solutions
 * by exploring all possible combinations and backtracking when conflicts arise.
 */
class BacktrackingScheduler {
public:
    /**
     * @brief Find optimal schedule using backtracking
     * @param activities Vector of activities to schedule
     * @return Vector of activities with maximum weight (optimal solution)
     * @complexity Time: O(2^n), Space: O(n)
     */
    static std::vector<Activity> optimalSchedule(std::vector<Activity> activities);
    
    /**
     * @brief Find all possible valid schedules
     * @param activities Vector of activities to schedule
     * @return Vector of all valid scheduling combinations
     */
    static std::vector<std::vector<Activity>> allValidSchedules(std::vector<Activity> activities);

private:
    /**
     * @brief Recursive backtracking function
     * @param activities All activities
     * @param current Current partial solution
     * @param index Current activity index
     * @param best Best solution found so far
     */
    static void backtrack(
        const std::vector<Activity>& activities,
        std::vector<Activity>& current,
        size_t index,
        std::vector<Activity>& best
    );
    
    /**
     * @brief Check if adding an activity creates conflicts
     * @param current Current schedule
     * @param newActivity Activity to add
     * @return true if no conflicts, false otherwise
     */
    static bool isValidAddition(const std::vector<Activity>& current, const Activity& newActivity);
    
    /**
     * @brief Calculate total weight of activities
     */
    static double calculateWeight(const std::vector<Activity>& activities);
    
    /**
     * @brief Recursive function to find all valid schedules
     */
    static void findAllSchedules(
        const std::vector<Activity>& activities,
        std::vector<Activity>& current,
        size_t index,
        std::vector<std::vector<Activity>>& allSchedules
    );
};

#endif // BACKTRACKING_H
