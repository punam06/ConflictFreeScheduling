#include "database_manager.h"
#include <iostream>
#include <fstream>
#include <sstream>

DatabaseManager::DatabaseManager(const std::string& database_path) 
    : db(nullptr), db_path(database_path), is_connected(false) {
    // Constructor implementation
}

DatabaseManager::~DatabaseManager() {
    closeConnection();
}

bool DatabaseManager::openConnection() {
    int result = sqlite3_open(db_path.c_str(), &db);
    if (result != SQLITE_OK) {
        last_error = "Cannot open database: " + std::string(sqlite3_errmsg(db));
        return false;
    }
    
    // Enable foreign key constraints
    executeQuery("PRAGMA foreign_keys = ON;");
    
    is_connected = true;
    return true;
}

void DatabaseManager::closeConnection() {
    if (db) {
        sqlite3_close(db);
        db = nullptr;
        is_connected = false;
    }
}

bool DatabaseManager::initialize() {
    if (!openConnection()) {
        return false;
    }
    
    return createTables();
}

bool DatabaseManager::createTables() {
    return executeSQLFile("data/schema.sql");
}

bool DatabaseManager::loadSampleData() {
    return executeSQLFile("data/minimal_sample.sql");
}

bool DatabaseManager::executeQuery(const std::string& query) {
    char* error_message = nullptr;
    int result = sqlite3_exec(db, query.c_str(), nullptr, nullptr, &error_message);
    
    if (result != SQLITE_OK) {
        last_error = "SQL error: " + std::string(error_message);
        sqlite3_free(error_message);
        return false;
    }
    
    return true;
}

bool DatabaseManager::executeSQLFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        last_error = "Cannot open SQL file: " + filename;
        return false;
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string sql_content = buffer.str();
    
    return executeQuery(sql_content);
}

sqlite3_stmt* DatabaseManager::prepareStatement(const std::string& query) {
    sqlite3_stmt* stmt;
    int result = sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr);
    
    if (result != SQLITE_OK) {
        last_error = "Failed to prepare statement: " + std::string(sqlite3_errmsg(db));
        return nullptr;
    }
    
    return stmt;
}

bool DatabaseManager::insertCourse(const Activity& course) {
    const std::string query = R"(
        INSERT INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    )";
    
    sqlite3_stmt* stmt = prepareStatement(query);
    if (!stmt) return false;
    
    std::string course_code = "CSE" + std::to_string(1100 + course.id);
    std::string course_title = "Course " + std::to_string(course.id);
    int duration = course.end - course.start;
    
    sqlite3_bind_text(stmt, 1, course_code.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, course_title.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_double(stmt, 3, 3.0); // Default credit hours
    sqlite3_bind_text(stmt, 4, "THEORY", -1, SQLITE_STATIC); 
    sqlite3_bind_int(stmt, 5, duration * 60); // Convert to minutes
    sqlite3_bind_int(stmt, 6, 3); // Default sessions per week
    sqlite3_bind_int(stmt, 7, 1); // Default batch_id
    sqlite3_bind_int(stmt, 8, 1); // Default teacher_id
    
    int result = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    
    return result == SQLITE_DONE;
}

std::vector<Activity> DatabaseManager::getAllCourses() {
    std::vector<Activity> courses;
    const std::string query = "SELECT course_id, course_title, session_duration, credit_hours FROM courses";
    
    sqlite3_stmt* stmt = prepareStatement(query);
    if (!stmt) return courses;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        int duration_minutes = sqlite3_column_int(stmt, 2);
        double credit_hours = sqlite3_column_double(stmt, 3);
        
        // Convert minutes to hours for start/end times (simplified)
        int duration_hours = duration_minutes / 60;
        if (duration_hours == 0) duration_hours = 1; // Minimum 1 hour
        
        // Create Activity with start=0, end=duration, weight=credit_hours
        Activity activity(id, 0, duration_hours, credit_hours);
        courses.push_back(activity);
    }
    
    sqlite3_finalize(stmt);
    return courses;
}

bool DatabaseManager::resetDatabase() {
    if (!executeQuery("DROP TABLE IF EXISTS schedule_assignments;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS conflicts_log;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS scheduling_preferences;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS courses;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS rooms;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS time_slots;")) return false;
    
    return createTables();
}

DatabaseManager::ScheduleStats DatabaseManager::getScheduleStatistics() {
    ScheduleStats stats = {0, 0, 0, 0, 0, 0, 0, 0};
    
    sqlite3_stmt* stmt = prepareStatement("SELECT COUNT(*) FROM courses");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_courses = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM rooms");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_rooms = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM time_slots");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_time_slots = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM schedule_assignments WHERE status = 'active'");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.scheduled_courses = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stats.unscheduled_courses = stats.total_courses - stats.scheduled_courses;
    
    stmt = prepareStatement("SELECT COUNT(*) FROM conflicts_log WHERE resolved = 0");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.conflicts_detected = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM conflicts_log WHERE resolved = 1");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.conflicts_resolved = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    if (stats.total_time_slots > 0) {
        stats.room_utilization_percentage = (stats.scheduled_courses * 100) / (stats.total_rooms * stats.total_time_slots);
    }
    
    return stats;
}

bool DatabaseManager::beginTransaction() {
    return executeQuery("BEGIN TRANSACTION;");
}

bool DatabaseManager::commitTransaction() {
    return executeQuery("COMMIT;");
}

bool DatabaseManager::rollbackTransaction() {
    return executeQuery("ROLLBACK;");
}
