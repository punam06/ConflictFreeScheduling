#include <iostream>
#include <vector>
#include <cassert>
#include <string>

// Include test files
#include "test_algorithms/algorithm_tests.cpp"
#include "test_utils/utility_tests.cpp"
#include "../src/scheduler.h"

/**
 * @brief Simple testing framework for C++ algorithms
 */
class TestRunner {
private:
    int totalTests = 0;
    int passedTests = 0;
    
public:
    void runTest(const std::string& testName, bool result) {
        totalTests++;
        if (result) {
            passedTests++;
            std::cout << "[PASS] " << testName << std::endl;
        } else {
            std::cout << "[FAIL] " << testName << std::endl;
        }
    }
    
    void summary() {
        std::cout << "\n=== Test Summary ===" << std::endl;
        std::cout << "Total tests: " << totalTests << std::endl;
        std::cout << "Passed: " << passedTests << std::endl;
        std::cout << "Failed: " << (totalTests - passedTests) << std::endl;
        std::cout << "Success rate: " << (passedTests * 100.0 / totalTests) << "%" << std::endl;
    }
};

/**
 * @brief Test cases for the scheduling algorithms
 */
class SchedulingTests {
private:
    TestRunner& runner;
    ConflictFreeScheduler scheduler;
    
public:
    SchedulingTests(TestRunner& r) : runner(r) {}
    
    void testEmptyInput() {
        std::vector<Activity> activities;
        auto result = scheduler.dpSchedule(activities);
        runner.runTest("Empty input test", result.empty());
    }
    
    void testSingleActivity() {
        std::vector<Activity> activities = {{1, 1, 3}};
        auto result = scheduler.dpSchedule(activities);
        runner.runTest("Single activity test", result.size() == 1);
    }
    
    void testNonOverlappingActivities() {
        std::vector<Activity> activities = {
            {1, 1, 2},
            {2, 3, 4},
            {3, 5, 6}
        };
        auto result = scheduler.graphColoringSchedule(activities);
        runner.runTest("Non-overlapping activities", result.size() == 3);
    }
    
    void testOverlappingActivities() {
        std::vector<Activity> activities = {
            {1, 1, 4},
            {2, 3, 5},
            {3, 0, 6}
        };
        auto result = scheduler.geneticAlgorithmSchedule(activities);
        runner.runTest("Overlapping activities", result.size() >= 1);
    }
    
    void testClassicExample() {
        std::vector<Activity> activities = {
            {1, 1, 4},
            {2, 3, 5},
            {3, 0, 6},
            {4, 5, 7},
            {5, 8, 9}
        };
        auto result = scheduler.dpSchedule(activities);
        runner.runTest("Classic textbook example", result.size() == 3);
    }
    
    void runAllTests() {
        std::cout << "Running Scheduling Algorithm Tests..." << std::endl;
        std::cout << "====================================" << std::endl;
        
        testEmptyInput();
        testSingleActivity();
        testNonOverlappingActivities();
        testOverlappingActivities();
        testClassicExample();
    }
};

/**
 * @brief Main test runner
 */
int main() {
    std::cout << "Conflict-Free Scheduling Test Suite" << std::endl;
    std::cout << "===================================" << std::endl;
    
    // Run basic scheduling tests
    TestRunner runner;
    SchedulingTests tests(runner);
    tests.runAllTests();
    
    std::cout << "\n";
    
    // Run algorithm-specific tests
    AlgorithmTests algorithmTests(true);
    algorithmTests.runAllTests();
    
    std::cout << "\n";
    
    // Run utility tests
    UtilityTests utilityTests(true);
    utilityTests.runAllTests();
    
    std::cout << "\n";
    runner.summary();
    
    return 0;
}
