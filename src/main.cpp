#include "scheduler.h"
#include "database/database_manager.h"
#include "utils/file_parser.h"
#include "utils/pdf_generator.h"
#include "utils/academic_pdf_generator.h"
#include "algorithms/enhanced_routine_generator.h"
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <chrono>
#include <iomanip>
#include <memory>

/**
 * @brief Main function demonstrating the conflict-free scheduling system
 * Enhanced with academic PDF generation and professional BUP scheduling
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
    bool generatePDF = false;
    bool generateAcademicPDF = false;
    bool generateUniversitySchedule = false;
    bool generateComprehensiveRoutine = false;
    bool useEnhancedGenerator = false;
    std::string batchCode = "";
    std::string sectionName = "";
    std::string facultyCode = "";
    std::string roomCode = "";
    std::string academicYear = "2024-25";
    std::string semester = "Spring";
    
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
        } else if (arg == "--pdf") {
            generatePDF = true;
        } else if (arg == "--academic-pdf") {
            generateAcademicPDF = true;
        } else if (arg == "--university-schedule") {
            generateUniversitySchedule = true;
        } else if (arg == "--comprehensive-routine") {
            generateComprehensiveRoutine = true;
        } else if (arg == "--enhanced-generator") {
            useEnhancedGenerator = true;
        } else if (arg == "--batch" && i + 1 < argc) {
            batchCode = argv[++i];
        } else if (arg == "--section" && i + 1 < argc) {
            sectionName = argv[++i];
        } else if (arg == "--faculty" && i + 1 < argc) {
            facultyCode = argv[++i];
        } else if (arg == "--room" && i + 1 < argc) {
            roomCode = argv[++i];
        } else if (arg == "--year" && i + 1 < argc) {
            academicYear = argv[++i];
        } else if (arg == "--semester" && i + 1 < argc) {
            semester = argv[++i];
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
        std::cout << "  --pdf               Generate PDF output and open in browser" << std::endl;
        std::cout << "  --academic-pdf      Generate professional academic schedule PDF" << std::endl;
        std::cout << "  --university-schedule Generate complete university schedule (all batches)" << std::endl;
        std::cout << "  --comprehensive-routine Generate comprehensive routine (days as rows, rooms as sub-rows)" << std::endl;
        std::cout << "  --enhanced-generator  Use enhanced routine generator with faculty constraints" << std::endl;
        std::cout << "  --batch <code>      Specify batch code (e.g., BCSE23)" << std::endl;
        std::cout << "  --section <name>    Specify section name (A or B)" << std::endl;
        std::cout << "  --faculty <code>    Generate faculty-specific schedule" << std::endl;
        std::cout << "  --room <code>       Generate room utilization schedule" << std::endl;
        std::cout << "  --year <year>       Academic year (default: 2024-25)" << std::endl;
        std::cout << "  --semester <sem>    Semester (Spring/Summer/Fall, default: Spring)" << std::endl;
        std::cout << "  --visualize         Enable visualization output" << std::endl;
        std::cout << "  --no-database       Disable database integration (use file input only)" << std::endl;
        std::cout << "  --init-db           Initialize/reset database with sample data" << std::endl;
        std::cout << "  --help, -h          Show this help message" << std::endl;
        std::cout << "\n🎓 Academic Scheduling Features:" << std::endl;
        std::cout << "  • Professional PDF generation with university branding" << std::endl;
        std::cout << "  • Section-wise schedules (BCSE22-25, Sections A & B)" << std::endl;
        std::cout << "  • Faculty schedules with contact information" << std::endl;
        std::cout << "  • Room utilization reports" << std::endl;
        std::cout << "  • Credit-hour based session durations" << std::endl;
        std::cout << "  • External faculty scheduling support" << std::endl;
        std::cout << "\n4 Core Algorithms:" << std::endl;
        std::cout << "  1. Graph Coloring    - Models conflicts as graph edges, assigns time slots as colors" << std::endl;
        std::cout << "  2. Dynamic Programming - Optimal weighted activity selection with memoization" << std::endl;
        std::cout << "  3. Backtracking      - Exhaustive search with pruning for optimal solutions" << std::endl;
        std::cout << "  4. Genetic Algorithm - Population-based evolutionary optimization" << std::endl;
        std::cout << "\nExamples:" << std::endl;
        std::cout << "  " << argv[0] << " --enhanced-generator --init-db" << std::endl;
        std::cout << "  " << argv[0] << " --enhanced-generator --comprehensive-routine" << std::endl;
        std::cout << "  " << argv[0] << " --run-all --visualize" << std::endl;
        std::cout << "  " << argv[0] << " --algorithm genetic --no-database --input data/sample_courses.txt" << std::endl;
        std::cout << "  " << argv[0] << " --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database" << std::endl;
        std::cout << "\n🎓 Academic Examples:" << std::endl;
        std::cout << "  " << argv[0] << " --academic-pdf --batch BCSE23 --section A" << std::endl;
        std::cout << "  " << argv[0] << " --university-schedule --algorithm graph-coloring" << std::endl;
        std::cout << "  " << argv[0] << " --comprehensive-routine --algorithm genetic" << std::endl;
        std::cout << "  " << argv[0] << " --faculty DR_ASM --year 2024-25 --semester Spring" << std::endl;
        std::cout << "  " << argv[0] << " --room CR302 --academic-pdf" << std::endl;
        std::cout << "\nInput File Format:" << std::endl;
        std::cout << "  Course Name,Start Time,End Time,Students" << std::endl;
        std::cout << "  Data Structures,9,11,50" << std::endl;
        std::cout << "  Algorithms,10,12,45" << std::endl;
        return 0;
    }
    
    // Database initialization
    std::shared_ptr<DatabaseManager> dbManager;
    if (useDatabase) {
        std::cout << "\n=== Database Integration ===" << std::endl;
        dbManager = std::make_shared<DatabaseManager>("data/scheduling.db");
        
        if (!dbManager->connect()) {
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

    // Enhanced Routine Generator Option
    if (useEnhancedGenerator) {
        if (!useDatabase || !dbManager) {
            std::cerr << "❌ Enhanced routine generator requires database integration!" << std::endl;
            std::cerr << "    Please run with database enabled (remove --no-database)" << std::endl;
            return 1;
        }
        
        std::cout << "\n🎓 === Enhanced Routine Generator ===" << std::endl;
        std::cout << "Generating comprehensive conflict-free schedule for BUP CSE Department" << std::endl;
        
        try {
            // Create enhanced routine generator
            auto enhancedGenerator = std::make_unique<EnhancedRoutineGenerator>(dbManager);
            
            // Generate complete routine
            std::cout << "\n🔄 Generating complete university routine..." << std::endl;
            bool success = enhancedGenerator->generateCompleteRoutine(academicYear, semester);
            
            if (success) {
                std::cout << "\n✅ Enhanced routine generation completed!" << std::endl;
                
                // Print statistics
                enhancedGenerator->printScheduleSummary();
                
                // Generate PDFs using enhanced data
                if (generateComprehensiveRoutine || generateUniversitySchedule || generateAcademicPDF) {
                    std::cout << "\n📄 Generating PDF outputs..." << std::endl;
                    auto academicPDFGen = std::make_shared<AcademicPDFGenerator>(dbManager);
                    std::string outputBase = outputFile.empty() ? "output/enhanced_schedule" : outputFile;
                    
                    if (generateComprehensiveRoutine) {
                        if (academicPDFGen->generateComprehensiveUniversityRoutine(outputBase, "Enhanced Algorithm", academicYear, semester)) {
                            std::cout << "✅ Comprehensive routine PDF generated!" << std::endl;
                        }
                    }
                    
                    if (generateUniversitySchedule) {
                        if (academicPDFGen->generateUniversitySchedule(outputBase, "Enhanced Algorithm", academicYear, semester)) {
                            std::cout << "✅ University schedule PDF generated!" << std::endl;
                        }
                    }
                }
                
                return 0; // Exit after enhanced generation
            } else {
                std::cerr << "❌ Enhanced routine generation failed!" << std::endl;
                return 1;
            }
            
        } catch (const std::exception& e) {
            std::cerr << "❌ Error in enhanced routine generator: " << e.what() << std::endl;
            return 1;
        }
    }

    // Create scheduler instance
    ConflictFreeScheduler scheduler;
    
    // Get activities from input file, database, or use default
    std::vector<Activity> activities;
    std::vector<std::string> courseNames;
    
    if (!inputFile.empty()) {
        std::cout << "\n=== Loading Activities from Input File ===" << std::endl;
        FileParser parser;
        try {
            auto result = parser.parseCSVFormat(inputFile);
            activities = result.first;
            courseNames = result.second;
            std::cout << "Loaded " << activities.size() << " activities from file: " << inputFile << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error parsing input file: " << e.what() << std::endl;
            std::cout << "Falling back to built-in sample data..." << std::endl;
            inputFile = ""; // Reset to use default data
        }
    }
    
    if (inputFile.empty()) {
        if (useDatabase && dbManager) {
            std::cout << "\n=== Loading Activities from Database ===" << std::endl;
            auto coursesWithTitles = dbManager->getAllCoursesWithTitles();
            activities = coursesWithTitles.first;
            courseNames = coursesWithTitles.second;
            std::cout << "Loaded " << activities.size() << " activities from database." << std::endl;
        } else {
            std::cout << "\n=== Using Built-in Sample Data ===" << std::endl;
            // Sample activities (CSE Department courses)
            activities = {
                {1, 9, 11, 50},    // Data Structures: 9-11 AM, 50 students
                {2, 10, 12, 45},   // Algorithms: 10-12 PM, 45 students  
                {3, 13, 15, 40},   // Database Systems: 1-3 PM, 40 students
                {4, 14, 16, 35},   // Computer Networks: 2-4 PM, 35 students
                {5, 16, 18, 30},   // Software Engineering: 4-6 PM, 30 students
                {6, 11, 13, 25},   // Operating Systems: 11-1 PM, 25 students
                {7, 15, 17, 20}    // Machine Learning: 3-5 PM, 20 students
            };
            courseNames = {
                "Data Structures", "Algorithms", "Database Systems", 
                "Computer Networks", "Software Engineering", 
                "Operating Systems", "Machine Learning"
            };
            std::cout << "Using " << activities.size() << " built-in sample activities." << std::endl;
        }
    }
    
    std::cout << "\nInput Activities (CSE Courses):" << std::endl;
    std::cout << "ID | Course                | Time    | Students" << std::endl;
    std::cout << "---|----------------------|---------|----------" << std::endl;
    
    for (size_t i = 0; i < activities.size(); i++) {
        const auto& activity = activities[i];
        std::string courseName = (i < courseNames.size()) ? courseNames[i] : "Unknown Course";
        // Truncate long names and pad short ones
        if (courseName.length() > 20) {
            courseName = courseName.substr(0, 17) + "...";
        }
        std::cout << " " << activity.id << " | " 
                  << courseName << std::string(21 - courseName.length(), ' ') 
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
    
    // Save scheduling results to database for academic PDF generation
    if (useDatabase && dbManager && !schedule.empty()) {
        std::cout << "\n=== Saving Results to Database ===" << std::endl;
        if (dbManager->saveSchedulingResults(schedule, courseNames, algorithm, academicYear, semester)) {
            std::cout << "✅ Scheduling results saved successfully!" << std::endl;
            std::cout << "   Academic PDF generation is now available." << std::endl;
        } else {
            std::cerr << "⚠️ Failed to save results to database: " << dbManager->getLastError() << std::endl;
            std::cerr << "   Academic PDF generation may not work properly." << std::endl;
        }
    }
    
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
    
    // Generate PDF if requested
    if (generatePDF) {
        std::cout << "\n=== Generating PDF Output ===" << std::endl;
        PDFGenerator pdfGen;
        try {
            std::string filename = "schedule_" + algorithm + ".html";
            pdfGen.generateSchedulePDF(schedule, courseNames, algorithm, filename);
            std::cout << "PDF generated successfully! Opening in browser..." << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error generating PDF: " << e.what() << std::endl;
        }
    }
    
    // Generate Academic PDF if requested
    if (generateAcademicPDF || generateUniversitySchedule || generateComprehensiveRoutine || !facultyCode.empty() || !roomCode.empty()) {
        if (!useDatabase || !dbManager) {
            std::cerr << "❌ Academic PDF generation requires database integration!" << std::endl;
            std::cerr << "    Please run with database enabled (remove --no-database)" << std::endl;
            return 1;
        }
        
        std::cout << "\n🎓 === Academic Schedule Generation ===" << std::endl;
        
        // Create academic PDF generator with database integration
        auto academicPDFGen = std::make_shared<AcademicPDFGenerator>(dbManager);
        
        // Determine output base path
        std::string outputBase = outputFile.empty() ? "output/academic_schedule" : outputFile;
        
        try {
            if (generateUniversitySchedule) {
                // Generate complete university schedule
                std::cout << "🏛️ Generating complete university schedule..." << std::endl;
                if (academicPDFGen->generateUniversitySchedule(outputBase, algorithm, academicYear, semester)) {
                    std::cout << "✅ University schedule generation completed!" << std::endl;
                } else {
                    std::cerr << "❌ Failed to generate university schedule" << std::endl;
                }
                
            } else if (generateComprehensiveRoutine) {
                // Generate comprehensive university routine with proper format
                std::cout << "🏛️ Generating comprehensive university routine..." << std::endl;
                if (academicPDFGen->generateComprehensiveUniversityRoutine(outputBase, algorithm, academicYear, semester)) {
                    std::cout << "✅ Comprehensive university routine generated successfully!" << std::endl;
                } else {
                    std::cerr << "❌ Failed to generate comprehensive routine" << std::endl;
                }
                
            } else if (!facultyCode.empty()) {
                // Generate faculty-specific schedule
                std::cout << "👨‍🏫 Generating faculty schedule for: " << facultyCode << std::endl;
                std::string facultyOutput = outputBase + "_faculty_" + facultyCode;
                if (academicPDFGen->generateFacultyScheduleFromDB(facultyCode, facultyOutput, algorithm, academicYear, semester)) {
                    std::cout << "✅ Faculty schedule generated successfully!" << std::endl;
                } else {
                    std::cerr << "❌ Failed to generate faculty schedule" << std::endl;
                }
                
            } else if (!roomCode.empty()) {
                // Generate room utilization schedule
                std::cout << "🏢 Generating room schedule for: " << roomCode << std::endl;
                std::string roomOutput = outputBase + "_room_" + roomCode;
                if (academicPDFGen->generateRoomUtilizationFromDB(roomCode, roomOutput, algorithm, academicYear, semester)) {
                    std::cout << "✅ Room schedule generated successfully!" << std::endl;
                } else {
                    std::cerr << "❌ Failed to generate room schedule" << std::endl;
                }
                
            } else if (!batchCode.empty() && !sectionName.empty()) {
                // Generate section-specific schedule
                std::cout << "📚 Generating schedule for: " << batchCode << " Section " << sectionName << std::endl;
                std::string sectionOutput = outputBase + "_" + batchCode + "_" + sectionName;
                if (academicPDFGen->generateScheduleFromDatabase(batchCode, sectionName, sectionOutput, algorithm, academicYear, semester)) {
                    std::cout << "✅ Section schedule generated successfully!" << std::endl;
                } else {
                    std::cerr << "❌ Failed to generate section schedule" << std::endl;
                }
                
            } else {
                // Default: Generate for all active batches
                std::cout << "📋 Generating schedules for all active batches..." << std::endl;
                auto batches = dbManager->getAllBatches();
                
                if (batches.empty()) {
                    std::cerr << "❌ No active batches found in database" << std::endl;
                    std::cerr << "    Try running with --init-db to load sample data" << std::endl;
                } else {
                    bool anySuccess = false;
                    for (const auto& batch : batches) {
                        // Generate for both sections A and B
                        for (const std::string& section : {"A", "B"}) {
                            std::string batchOutput = outputBase + "_" + batch.batch_code + "_" + section;
                            std::cout << "  📄 Generating: " << batch.batch_code << " Section " << section << std::endl;
                            
                            if (academicPDFGen->generateScheduleFromDatabase(
                                batch.batch_code, section, batchOutput, algorithm, academicYear, semester)) {
                                anySuccess = true;
                            } else {
                                std::cerr << "    ⚠️ Failed: " << batch.batch_code << " Section " << section << std::endl;
                            }
                        }
                    }
                    
                    if (anySuccess) {
                        std::cout << "✅ Academic schedule generation completed!" << std::endl;
                    } else {
                        std::cerr << "❌ No schedules were generated successfully" << std::endl;
                    }
                }
            }
            
        } catch (const std::exception& e) {
            std::cerr << "❌ Error during academic PDF generation: " << e.what() << std::endl;
        }
        
        // Display academic statistics
        std::cout << "\n📊 Academic Statistics:" << std::endl;
        auto academicStats = dbManager->getAcademicStatistics(academicYear, semester);
        std::cout << "  • Total Batches: " << academicStats.total_batches << std::endl;
        std::cout << "  • Internal Faculty: " << academicStats.total_teachers << std::endl;
        std::cout << "  • Available Classrooms: " << academicStats.total_classrooms << std::endl;
        std::cout << "  • Total Courses: " << academicStats.total_courses << std::endl;
        std::cout << "  • Total Sections: " << academicStats.total_sections << " (4 batches × 2 sections each)" << std::endl;
        std::cout << "  • Scheduled Sessions: " << academicStats.scheduled_sessions << std::endl;
        std::cout << "  • Schedule Completion: " << std::fixed << std::setprecision(1) 
                  << academicStats.schedule_completion_percentage << "%" << std::endl;
        
        if (academicStats.teacher_conflicts > 0 || academicStats.room_conflicts > 0 || academicStats.section_conflicts > 0) {
            std::cout << "\n⚠️ Conflicts Detected:" << std::endl;
            if (academicStats.teacher_conflicts > 0) {
                std::cout << "  • Teacher conflicts: " << academicStats.teacher_conflicts << std::endl;
            }
            if (academicStats.room_conflicts > 0) {
                std::cout << "  • Room conflicts: " << academicStats.room_conflicts << std::endl;
            }
            if (academicStats.section_conflicts > 0) {
                std::cout << "  • Section conflicts: " << academicStats.section_conflicts << std::endl;
            }
        }
    }
    
    std::cout << "\n=== Scheduling Complete ===" << std::endl;
    return 0;
}
