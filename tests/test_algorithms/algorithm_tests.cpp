#include <vector>
#include <string>
#include <iostream>
#include <cassert>
#include "../../src/algorithms/graph_coloring.h"
#include "../../src/algorithms/dynamic_programming.h"
#include "../../src/algorithms/backtracking.h"
#include "../../src/algorithms/genetic_algorithm.h"
#include "../../src/scheduler.h"

/**
 * @brief Test class for algorithm-specific unit tests
 */
class AlgorithmTests {
private:
    bool verbose;
    
public:
    AlgorithmTests(bool verbose = false) : verbose(verbose) {}
    
    void testGraphColoring() {
        if (verbose) std::cout << "Testing Graph Coloring algorithm..." << std::endl;
        
        std::vector<Activity> activities = {
            {1, 9, 11},   // Class 1: 9-11 AM
            {2, 10, 12},  // Class 2: 10-12 AM (conflicts with 1)
            {3, 11, 13},  // Class 3: 11-1 PM (conflicts with 2)
            {4, 13, 15},  // Class 4: 1-3 PM
            {5, 14, 16}   // Class 5: 2-4 PM (conflicts with 4)
        };
        
        ConflictFreeScheduler scheduler;
        auto result = scheduler.graphColoringSchedule(activities);
        
        // Should be able to schedule at least 2 non-conflicting activities
        assert(result.size() >= 2);
        
        // Verify no conflicts in the result
        for (size_t i = 0; i < result.size(); i++) {
            for (size_t j = i + 1; j < result.size(); j++) {
                assert(!scheduler.hasConflict(result[i], result[j]));
            }
        }
        
        if (verbose) std::cout << "Graph Coloring test passed!" << std::endl;
    }
    
    void testDynamicProgramming() {
        if (verbose) std::cout << "Testing Dynamic Programming algorithm..." << std::endl;
        
        std::vector<Activity> activities = {
            {1, 1, 3, 5},   // Activity 1: weight 5
            {2, 2, 5, 10},  // Activity 2: weight 10
            {3, 4, 7, 7},   // Activity 3: weight 7
            {4, 6, 9, 8}    // Activity 4: weight 8
        };
        
        ConflictFreeScheduler scheduler;
        auto result = scheduler.dpSchedule(activities);
        
        // Should return a valid solution
        assert(!result.empty());
        
        // Verify no conflicts in the result
        for (size_t i = 0; i < result.size(); i++) {
            for (size_t j = i + 1; j < result.size(); j++) {
                assert(!scheduler.hasConflict(result[i], result[j]));
            }
        }
        
        // Calculate total weight
        double totalWeight = scheduler.calculateTotalWeight(result);
        assert(totalWeight > 0); // Should have some positive weight
        
        if (verbose) std::cout << "Dynamic Programming test passed!" << std::endl;
    }
    
    void testBacktracking() {
        if (verbose) std::cout << "Testing Backtracking algorithm..." << std::endl;
        
        std::vector<Activity> activities = {
            {1, 1, 3},
            {2, 2, 4},
            {3, 3, 5},
            {4, 5, 7}
        };
        
        ConflictFreeScheduler scheduler;
        auto result = scheduler.backtrackingSchedule(activities);
        
        // Should return a valid solution
        assert(!result.empty());
        
        // Verify no conflicts in the result
        for (size_t i = 0; i < result.size(); i++) {
            for (size_t j = i + 1; j < result.size(); j++) {
                assert(!scheduler.hasConflict(result[i], result[j]));
            }
        }
        
        if (verbose) std::cout << "Backtracking test passed!" << std::endl;
    }
    
    void testGeneticAlgorithm() {
        if (verbose) std::cout << "Testing Genetic Algorithm..." << std::endl;
        
        std::vector<Activity> activities = {
            {1, 1, 3, 5},
            {2, 2, 4, 3},
            {3, 3, 6, 7},
            {4, 5, 8, 4},
            {5, 7, 9, 6}
        };
        
        ConflictFreeScheduler scheduler;
        auto result = scheduler.geneticAlgorithmSchedule(activities);
        
        // Should return a non-empty schedule with no conflicts
        assert(!result.empty());
        
        // Verify no conflicts
        for (size_t i = 0; i < result.size(); i++) {
            for (size_t j = i + 1; j < result.size(); j++) {
                assert(!scheduler.hasConflict(result[i], result[j]));
            }
        }
        
        if (verbose) std::cout << "Genetic Algorithm test passed!" << std::endl;
    }
    
    void runAllTests() {
        testGraphColoring();
        testDynamicProgramming();
        testBacktracking();
        testGeneticAlgorithm();
        
        std::cout << "All algorithm tests passed successfully!" << std::endl;
    }
};

#ifdef RUN_ALGORITHM_TESTS
int main() {
    AlgorithmTests tests(true);
    tests.runAllTests();
    return 0;
}
#endif
