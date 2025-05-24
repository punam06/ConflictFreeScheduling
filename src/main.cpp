#include "scheduler.h"
#include "database/database_manager.h"
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <chrono>
#include <iomanip>

/**
 * @brief Main function demonstrating the conflict-free scheduling system
 */
int main(int argc, char* argv[]) {
    std::cout << "=== Conflict-Free Class Scheduling System ===" << std::endl;
    std::cout << "CSE Department Academic Scheduling Solution" << std::endl;
    std::cout << "=============================================" << std::endl;
    
    // Parse command line arguments
    std::string algorithm = "graph-coloring";
    std::string inputFile = "";
    std::string outputFile = "";
    bool visualize = false;
    bool showHelp = false;
    bool useDatabase = true;
    bool initDatabase = false;
    bool runAll = false;
    
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--algorithm" && i + 1 < argc) {
            algorithm = argv[++i];
        } else if (arg == "--input" && i + 1 < argc) {
            inputFile = argv[++i];
        } else if (arg == "--output" && i + 1 < argc) {
            outputFile = argv[++i];
        } else if (arg == "--visualize") {
            visualize = true;
        } else if (arg == "--no-database") {
            useDatabase = false;
        } else if (arg == "--init-db") {
            initDatabase = true;
        } else if (arg == "--run-all") {
            runAll = true;
        } else if (arg == "--help" || arg == "-h") {
            showHelp = true;
        }
    }
    
    if (showHelp) {
        std::cout << "\nUsage: " << argv[0] << " [options]" << std::endl;
        std::cout << "\nOptions:" << std::endl;
        std::cout << "  --algorithm <type>  Algorithm to use:" << std::endl;
        std::cout << "                        graph-coloring  : Graph coloring for conflict resolution" << std::endl;
        std::cout << "                        dynamic-prog    : Dynamic programming for optimal selection" << std::endl;
        std::cout << "                        backtracking    : Backtracking for exhaustive solutions" << std::endl;
        std::cout << "                        genetic         : Genetic algorithm for evolution-based optimization" << std::endl;
        std::cout << "  --run-all           Run all 4 core algorithms and compare results" << std::endl;
        std::cout << "  --input <file>      Input file with activities data" << std::endl;
        std::cout << "  --output <file>     Output file for results" << std::endl;
        std::cout << "  --visualize         Enable visualization output" << std::endl;
        std::cout << "  --no-database       Disable database integration (use file input only)" << std::endl;
        std::cout << "  --init-db           Initialize/reset database with sample data" << std::endl;
        std::cout << "  --help, -h          Show this help message" << std::endl;
        std::cout << "\n4 Core Algorithms:" << std::endl;
        std::cout << "  1. Graph Coloring    - Models conflicts as graph edges, assigns time slots as colors" << std::endl;
        std::cout << "  2. Dynamic Programming - Optimal weighted activity selection with memoization" << std::endl;
        std::cout << "  3. Backtracking      - Exhaustive search with pruning for optimal solutions" << std::endl;
        std::cout << "  4. Genetic Algorithm - Population-based evolutionary optimization" << std::endl;
        std::cout << "\nExamples:" << std::endl;
        std::cout << "  " << argv[0] << " --algorithm graph-coloring --init-db" << std::endl;
        std::cout << "  " << argv[0] << " --run-all --visualize" << std::endl;
        std::cout << "  " << argv[0] << " --algorithm genetic --no-database --input data/courses.txt" << std::endl;
        return 0;
    }
    
    // Database initialization
    std::unique_ptr<DatabaseManager> dbManager;
    if (useDatabase) {
        std::cout << "\n=== Database Integration ===" << std::endl;
        dbManager = std::make_unique<DatabaseManager>("../data/scheduling.db");
        
        if (!dbManager->initialize()) {
            std::cerr << "Error: Failed to initialize database: " << dbManager->getLastError() << std::endl;
            return 1;
        }
        
        if (initDatabase) {
            std::cout << "Resetting database and loading sample data..." << std::endl;
            if (!dbManager->resetDatabase() || !dbManager->loadSampleData()) {
                std::cerr << "Error: Failed to initialize database with sample data: " << dbManager->getLastError() << std::endl;
                return 1;
            }
            std::cout << "Database initialized successfully!" << std::endl;
        }
        
        // Display database statistics
        auto stats = dbManager->getScheduleStatistics();
        std::cout << "Database Status:" << std::endl;
        std::cout << "  - Total Courses: " << stats.total_courses << std::endl;
        std::cout << "  - Total Rooms: " << stats.total_rooms << std::endl;
        std::cout << "  - Total Time Slots: " << stats.total_time_slots << std::endl;
        std::cout << "  - Scheduled Courses: " << stats.scheduled_courses << std::endl;
        std::cout << "  - Unresolved Conflicts: " << stats.conflicts_detected << std::endl;
    }

    // Create scheduler instance
    ConflictFreeScheduler scheduler;
    
    // Sample activities (CSE Department courses)
    std::vector<Activity> activities = {
        {1, 9, 11, 50},    // Data Structures: 9-11 AM, 50 students
        {2, 10, 12, 45},   // Algorithms: 10-12 PM, 45 students  
        {3, 13, 15, 40},   // Database Systems: 1-3 PM, 40 students
        {4, 14, 16, 35},   // Computer Networks: 2-4 PM, 35 students
        {5, 16, 18, 30},   // Software Engineering: 4-6 PM, 30 students
        {6, 11, 13, 25},   // Operating Systems: 11-1 PM, 25 students
        {7, 15, 17, 20}    // Machine Learning: 3-5 PM, 20 students
    };
    
    std::cout << "\nInput Activities (CSE Courses):" << std::endl;
    std::cout << "ID | Course                | Time    | Students" << std::endl;
    std::cout << "---|----------------------|---------|----------" << std::endl;
    std::vector<std::string> courseNames = {
        "Data Structures", "Algorithms", "Database Systems", 
        "Computer Networks", "Software Engineering", 
        "Operating Systems", "Machine Learning"
    };
    
    for (size_t i = 0; i < activities.size(); i++) {
        const auto& activity = activities[i];
        std::cout << " " << activity.id << " | " 
                  << courseNames[i] << std::string(21 - courseNames[i].length(), ' ') 
                  << " | " << activity.start << "-" << activity.end 
                  << "     | " << static_cast<int>(activity.weight) << std::endl;
    }
    
    // Run selected algorithm or all algorithms
    std::vector<Activity> schedule;
    
    if (runAll) {
        std::cout << "\n=== Running All 4 Core Algorithms ===" << std::endl;
        
        // 1. Graph Coloring
        std::cout << "\n1. Graph Coloring Algorithm:" << std::endl;
        auto start = std::chrono::high_resolution_clock::now();
        auto graphSchedule = scheduler.graphColoringSchedule(activities);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "   Scheduled: " << graphSchedule.size() << "/" << activities.size() 
                  << " activities (Weight: " << static_cast<int>(scheduler.calculateTotalWeight(graphSchedule)) << ")" << std::endl;
        std::cout << "   Execution time: " << std::fixed << std::setprecision(2) 
                  << duration.count() / 1000.0 << " ms" << std::endl;
        
        // 2. Dynamic Programming
        std::cout << "\n2. Dynamic Programming Algorithm:" << std::endl;
        start = std::chrono::high_resolution_clock::now();
        auto dpSchedule = scheduler.dpSchedule(activities);
        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "   Scheduled: " << dpSchedule.size() << "/" << activities.size() 
                  << " activities (Weight: " << static_cast<int>(scheduler.calculateTotalWeight(dpSchedule)) << ")" << std::endl;
        std::cout << "   Execution time: " << std::fixed << std::setprecision(2) 
                  << duration.count() / 1000.0 << " ms" << std::endl;
        
        // 3. Backtracking
        std::cout << "\n3. Backtracking Algorithm:" << std::endl;
        start = std::chrono::high_resolution_clock::now();
        auto backtrackSchedule = scheduler.backtrackingSchedule(activities);
        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "   Scheduled: " << backtrackSchedule.size() << "/" << activities.size() 
                  << " activities (Weight: " << static_cast<int>(scheduler.calculateTotalWeight(backtrackSchedule)) << ")" << std::endl;
        std::cout << "   Execution time: " << std::fixed << std::setprecision(2) 
                  << duration.count() / 1000.0 << " ms" << std::endl;
        
        // 4. Genetic Algorithm
        std::cout << "\n4. Genetic Algorithm:" << std::endl;
        start = std::chrono::high_resolution_clock::now();
        auto geneticSchedule = scheduler.geneticAlgorithmSchedule(activities);
        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "   Scheduled: " << geneticSchedule.size() << "/" << activities.size() 
                  << " activities (Weight: " << static_cast<int>(scheduler.calculateTotalWeight(geneticSchedule)) << ")" << std::endl;
        std::cout << "   Execution time: " << std::fixed << std::setprecision(2) 
                  << duration.count() / 1000.0 << " ms" << std::endl;
        
        // Use the best result for detailed output
        schedule = dpSchedule; // DP usually gives optimal results
        std::cout << "\nUsing Dynamic Programming result for detailed analysis:" << std::endl;
        
    } else {
        std::cout << "\nRunning " << algorithm << " algorithm..." << std::endl;
        
        auto start = std::chrono::high_resolution_clock::now();
        if (algorithm == "graph-coloring") {
            schedule = scheduler.graphColoringSchedule(activities);
        } else if (algorithm == "dynamic-prog" || algorithm == "dp") {
            schedule = scheduler.dpSchedule(activities);
        } else if (algorithm == "backtracking") {
            schedule = scheduler.backtrackingSchedule(activities);
        } else if (algorithm == "genetic") {
            schedule = scheduler.geneticAlgorithmSchedule(activities);
        } else {
            std::cerr << "Unknown algorithm: " << algorithm << std::endl;
            std::cerr << "Valid options: graph-coloring, dynamic-prog, backtracking, genetic" << std::endl;
            return 1;
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Execution time: " << std::fixed << std::setprecision(2) 
                  << duration.count() / 1000.0 << " ms" << std::endl;
    }
    
    // Display results
    std::cout << "\nOptimal Schedule:" << std::endl;
    std::cout << "=================" << std::endl;
    scheduler.printSchedule(schedule);
    
    std::cout << "\nScheduling Statistics:" << std::endl;
    std::cout << "- Total courses scheduled: " << schedule.size() << "/" << activities.size() << std::endl;
    std::cout << "- Total students served: " << static_cast<int>(scheduler.calculateTotalWeight(schedule)) << std::endl;
    std::cout << "- Utilization: " << (schedule.size() * 100.0 / activities.size()) << "%" << std::endl;
    
    // Save to output file if specified
    if (!outputFile.empty()) {
        std::ofstream out(outputFile);
        out << "Conflict-Free Scheduling Results" << std::endl;
        out << "Algorithm: " << algorithm << std::endl;
        out << "Scheduled Activities: " << schedule.size() << std::endl;
        for (const auto& activity : schedule) {
            out << "ID: " << activity.id << ", Time: " << activity.start 
                << "-" << activity.end << ", Weight: " << activity.weight << std::endl;
        }
        out.close();
        std::cout << "\nResults saved to: " << outputFile << std::endl;
    }
    
    if (visualize) {
        std::cout << "\nVisualization:" << std::endl;
        std::cout << "Time:  9 10 11 12 13 14 15 16 17 18" << std::endl;
        std::cout << "      =============================" << std::endl;
        
        for (const auto& activity : schedule) {
            std::cout << "C" << activity.id << ":   ";
            for (int hour = 9; hour <= 18; hour++) {
                if (hour >= activity.start && hour < activity.end) {
                    std::cout << "██ ";
                } else {
                    std::cout << "   ";
                }
            }
            std::cout << std::endl;
        }
    }
    
    std::cout << "\n=== Scheduling Complete ===" << std::endl;
    return 0;
}
