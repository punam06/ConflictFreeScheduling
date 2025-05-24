#include "database_manager.h"
#include <iostream>

/**
 * @brief Example demonstrating database integration with Conflict-Free Scheduling
 */
int main() {
    std::cout << "=== Database Integration Example ===" << std::endl;
    
    // Initialize database manager
    DatabaseManager dbManager("data/scheduling.db");
    
    if (!dbManager.initialize()) {
        std::cerr << "Failed to initialize database: " << dbManager.getLastError() << std::endl;
        return 1;
    }
    
    std::cout << "✓ Database initialized successfully" << std::endl;
    
    // Reset and load sample data
    if (!dbManager.resetDatabase() || !dbManager.loadSampleData()) {
        std::cerr << "Failed to load sample data: " << dbManager.getLastError() << std::endl;
        return 1;
    }
    
    std::cout << "✓ Sample data loaded" << std::endl;
    
    // Display database statistics
    auto stats = dbManager.getScheduleStatistics();
    std::cout << "\n=== Database Statistics ===" << std::endl;
    std::cout << "Total Courses: " << stats.total_courses << std::endl;
    std::cout << "Total Rooms: " << stats.total_rooms << std::endl;
    std::cout << "Total Time Slots: " << stats.total_time_slots << std::endl;
    std::cout << "Scheduled Courses: " << stats.scheduled_courses << std::endl;
    std::cout << "Unscheduled Courses: " << stats.unscheduled_courses << std::endl;
    std::cout << "Unresolved Conflicts: " << stats.conflicts_detected << std::endl;
    std::cout << "Resolved Conflicts: " << stats.conflicts_resolved << std::endl;
    std::cout << "Room Utilization: " << stats.room_utilization_percentage << "%" << std::endl;
    
    // Get all courses from database
    auto courses = dbManager.getAllCourses();
    std::cout << "\n=== Course List ===" << std::endl;
    for (const auto& course : courses) {
        std::cout << "Course ID: " << course.id 
                  << ", Name: " << course.name 
                  << ", Duration: " << course.duration 
                  << ", Priority: " << course.priority << std::endl;
    }
    
    // Example: Insert a new course
    Activity newCourse;
    newCourse.name = "CSE500-Advanced Algorithms";
    newCourse.duration = 3;
    newCourse.priority = 1;
    newCourse.start_time = 0;
    newCourse.end_time = 3;
    
    if (dbManager.insertCourse(newCourse)) {
        std::cout << "\n✓ Successfully inserted new course: " << newCourse.name << std::endl;
    } else {
        std::cerr << "\n✗ Failed to insert course: " << dbManager.getLastError() << std::endl;
    }
    
    // Example: Conflict logging
    DatabaseManager::ConflictLog conflict;
    conflict.conflict_type = "ROOM_CAPACITY";
    conflict.description = "Course enrollment exceeds room capacity";
    conflict.course_id_1 = 1;
    conflict.course_id_2 = 0;
    conflict.room_id = 1;
    conflict.slot_id = 1;
    conflict.resolved = false;
    
    if (dbManager.logConflict(conflict)) {
        std::cout << "\n✓ Conflict logged successfully" << std::endl;
    }
    
    // Get unresolved conflicts
    auto conflicts = dbManager.getUnresolvedConflicts();
    std::cout << "\n=== Unresolved Conflicts ===" << std::endl;
    for (const auto& c : conflicts) {
        std::cout << "Conflict ID: " << c.conflict_id 
                  << ", Type: " << c.conflict_type
                  << ", Description: " << c.description << std::endl;
    }
    
    std::cout << "\n=== Database Example Complete ===" << std::endl;
    return 0;
}
