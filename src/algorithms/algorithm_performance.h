#ifndef ALGORITHM_PERFORMANCE_H
#define ALGORITHM_PERFORMANCE_H

#include "../scheduler.h"
#include <vector>
#include <chrono>
#include <string>
#include <map>

/**
 * @brief Performance analysis and benchmarking for scheduling algorithms
 */
class AlgorithmPerformance {
public:
    /**
     * @brief Performance metrics for an algorithm run
     */
    struct PerformanceMetrics {
        double executionTime;        // Time in milliseconds
        int activitiesSelected;      // Number of activities selected
        double totalWeight;          // Total weight of selected activities
        double utilization;          // Time utilization percentage
        int algorithmsCompared;      // Number of algorithms in comparison
        double averageGap;          // Average gap between activities
        double efficiencyRatio;     // Weight per unit time efficiency
        
        PerformanceMetrics() : executionTime(0), activitiesSelected(0), 
                              totalWeight(0), utilization(0), 
                              algorithmsCompared(0), averageGap(0), 
                              efficiencyRatio(0) {}
    };
    
    /**
     * @brief Comparison result between algorithms
     */
    struct AlgorithmComparison {
        std::string algorithmName;
        PerformanceMetrics metrics;
        int rank;                   // Ranking (1 = best)
        double scoreMultiObjective; // Combined score
    };
    
    /**
     * @brief Comprehensive performance test of all algorithms
     * @param activities Test dataset
     * @return Map of algorithm names to performance metrics
     */
    static std::map<std::string, PerformanceMetrics> runComprehensiveTest(
        const std::vector<Activity>& activities);
    
    /**
     * @brief Benchmark algorithms with different dataset sizes
     * @param baseSizes Vector of dataset sizes to test
     * @return Performance scaling analysis
     */
    static std::map<std::string, std::vector<PerformanceMetrics>> benchmarkScaling(
        const std::vector<int>& baseSizes);
    
    /**
     * @brief Compare algorithm quality vs speed trade-offs
     * @param activities Test dataset
     * @return Sorted comparison results
     */
    static std::vector<AlgorithmComparison> compareAlgorithmTradeoffs(
        const std::vector<Activity>& activities);
    
    /**
     * @brief Generate synthetic test datasets
     * @param size Number of activities
     * @param timeRange Maximum time range
     * @param conflictRate Probability of conflicts (0.0-1.0)
     * @return Generated activity dataset
     */
    static std::vector<Activity> generateTestDataset(int size, int timeRange, 
                                                     double conflictRate = 0.3);
    
    /**
     * @brief Test algorithm robustness with edge cases
     * @return Map of test names to success/failure
     */
    static std::map<std::string, bool> testEdgeCases();
    
    /**
     * @brief Print detailed performance report
     * @param results Performance test results
     * @param title Report title
     */
    static void printPerformanceReport(
        const std::map<std::string, PerformanceMetrics>& results,
        const std::string& title = "Algorithm Performance Report");
    
    /**
     * @brief Print algorithm comparison report
     * @param comparisons Algorithm comparison results
     */
    static void printComparisonReport(
        const std::vector<AlgorithmComparison>& comparisons);

private:
    /**
     * @brief Measure execution time of a function
     */
    template<typename Func>
    static double measureExecutionTime(Func&& func);
    
    /**
     * @brief Calculate utilization percentage
     */
    static double calculateUtilization(const std::vector<Activity>& activities);
    
    /**
     * @brief Calculate average gap between consecutive activities
     */
    static double calculateAverageGap(const std::vector<Activity>& activities);
    
    /**
     * @brief Calculate multi-objective score
     */
    static double calculateMultiObjectiveScore(const PerformanceMetrics& metrics,
                                               double weightTime = 0.3,
                                               double weightQuality = 0.4,
                                               double weightEfficiency = 0.3);
    
    /**
     * @brief Sort activities by start time for analysis
     */
    static std::vector<Activity> sortByStartTime(std::vector<Activity> activities);
};

#endif // ALGORITHM_PERFORMANCE_H
