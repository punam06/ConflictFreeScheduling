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
    return executeSQLFile("data/sample_data_fixed.sql");
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

std::pair<std::vector<Activity>, std::vector<std::string>> DatabaseManager::getAllCoursesWithTitles() {
    std::vector<Activity> courses;
    std::vector<std::string> courseTitles;
    const std::string query = "SELECT course_id, course_title, session_duration, credit_hours FROM courses";
    
    sqlite3_stmt* stmt = prepareStatement(query);
    if (!stmt) return std::make_pair(courses, courseTitles);
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        const char* title = (const char*)sqlite3_column_text(stmt, 1);
        int duration_minutes = sqlite3_column_int(stmt, 2);
        double credit_hours = sqlite3_column_double(stmt, 3);
        
        // Convert minutes to hours for start/end times (simplified)
        int duration_hours = duration_minutes / 60;
        if (duration_hours == 0) duration_hours = 1; // Minimum 1 hour
        
        // Create Activity with start=0, end=duration, weight=credit_hours
        Activity activity(id, 0, duration_hours, credit_hours);
        courses.push_back(activity);
        
        // Store the actual course title from database
        courseTitles.push_back(title ? std::string(title) : "Unknown Course");
    }
    
    sqlite3_finalize(stmt);
    return std::make_pair(courses, courseTitles);
}

bool DatabaseManager::resetDatabase() {
    // Drop all tables in correct order (respecting foreign key constraints)
    if (!executeQuery("DROP TABLE IF EXISTS schedule;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS schedule_conflicts;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS teacher_constraints;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS room_constraints;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS routine_generation_log;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS system_settings;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS course_sections;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS courses;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS time_slots;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS classrooms;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS teachers;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS batches;")) return false;
    
    // Legacy table cleanup (in case they exist from old versions)
    if (!executeQuery("DROP TABLE IF EXISTS schedule_assignments;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS conflicts_log;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS scheduling_preferences;")) return false;
    if (!executeQuery("DROP TABLE IF EXISTS rooms;")) return false;
    
    return createTables();
}

DatabaseManager::ScheduleStats DatabaseManager::getScheduleStatistics() {
    ScheduleStats stats = {0, 0, 0, 0, 0, 0, 0, 0};
    
    sqlite3_stmt* stmt = prepareStatement("SELECT COUNT(*) FROM courses");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_courses = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM classrooms WHERE status = 'AVAILABLE'");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_rooms = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM time_slots");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.total_time_slots = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM schedule WHERE status = 'SCHEDULED'");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.scheduled_courses = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stats.unscheduled_courses = stats.total_courses - stats.scheduled_courses;
    
    stmt = prepareStatement("SELECT COUNT(*) FROM schedule_conflicts WHERE is_resolved = 0");
    if (stmt && sqlite3_step(stmt) == SQLITE_ROW) {
        stats.conflicts_detected = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    stmt = prepareStatement("SELECT COUNT(*) FROM schedule_conflicts WHERE is_resolved = 1");
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

// Academic Data Operations Implementation

std::vector<DatabaseManager::AcademicBatch> DatabaseManager::getAllBatches() {
    std::vector<AcademicBatch> batches;
    
    const char* sql = R"(
        SELECT batch_id, batch_code, batch_name, year_level, semester, 
               total_sections, status 
        FROM batches 
        WHERE status = 'ACTIVE' 
        ORDER BY year_level DESC, semester DESC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return batches;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicBatch batch;
        batch.batch_id = sqlite3_column_int(stmt, 0);
        batch.batch_code = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        batch.batch_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        batch.year_level = sqlite3_column_int(stmt, 3);
        batch.semester = sqlite3_column_int(stmt, 4);
        batch.total_sections = sqlite3_column_int(stmt, 5);
        batch.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        batches.push_back(batch);
    }
    
    sqlite3_finalize(stmt);
    return batches;
}

std::vector<DatabaseManager::AcademicTeacher> DatabaseManager::getAllTeachers() {
    std::vector<AcademicTeacher> teachers;
    
    const char* sql = R"(
        SELECT teacher_id, teacher_code, full_name, designation, department,
               email, phone, availability_start, availability_end, 
               external_faculty, max_hours_per_week, status
        FROM teachers 
        WHERE status = 'ACTIVE'
        ORDER BY external_faculty ASC, designation ASC, full_name ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return teachers;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicTeacher teacher;
        teacher.teacher_id = sqlite3_column_int(stmt, 0);
        teacher.teacher_code = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        teacher.full_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        teacher.designation = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        teacher.department = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        teacher.email = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
        teacher.phone = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        teacher.availability_start = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
        teacher.availability_end = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
        teacher.external_faculty = sqlite3_column_int(stmt, 9) == 1;
        teacher.max_hours_per_week = sqlite3_column_int(stmt, 10);
        teacher.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 11));
        teachers.push_back(teacher);
    }
    
    sqlite3_finalize(stmt);
    return teachers;
}

std::vector<DatabaseManager::Room> DatabaseManager::getAllRooms() {
    std::vector<Room> rooms;
    
    const char* sql = R"(
        SELECT room_id, room_code, room_code, capacity, 
               room_type, facilities, building, floor_number, 
               CASE WHEN status='AVAILABLE' THEN 1 ELSE 0 END
        FROM classrooms 
        WHERE status = 'AVAILABLE'
        ORDER BY building ASC, room_code ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return rooms;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        Room room;
        room.room_id = sqlite3_column_int(stmt, 0);
        room.room_code = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        room.room_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)); // Use room_code as name
        room.capacity = sqlite3_column_int(stmt, 3);
        room.room_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        room.equipment = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
        room.building = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        room.floor = sqlite3_column_int(stmt, 7);
        room.is_available = sqlite3_column_int(stmt, 8) != 0;
        
        rooms.push_back(room);
    }
    
    sqlite3_finalize(stmt);
    return rooms;
}

std::vector<DatabaseManager::AcademicCourse> DatabaseManager::getAllAcademicCourses() {
    std::vector<AcademicCourse> courses;
    
    const char* sql = R"(
        SELECT c.course_id, c.course_code, c.course_title, c.credit_hours,
               c.class_type, c.session_duration, c.sessions_per_week,
               c.batch_id, c.teacher_id, c.department, c.status
        FROM courses c
        WHERE c.status = 'ACTIVE'
        ORDER BY c.course_code ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return courses;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicCourse course;
        course.course_id = sqlite3_column_int(stmt, 0);
        course.course_code = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        course.course_title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        course.credit_hours = sqlite3_column_double(stmt, 3);
        course.class_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        course.session_duration = sqlite3_column_int(stmt, 5);
        course.sessions_per_week = sqlite3_column_int(stmt, 6);
        course.batch_id = sqlite3_column_int(stmt, 7);
        course.teacher_id = sqlite3_column_int(stmt, 8);
        course.department = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
        course.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
        courses.push_back(course);
    }
    
    sqlite3_finalize(stmt);
    return courses;
}

std::vector<DatabaseManager::AcademicSection> DatabaseManager::getAllSections() {
    std::vector<AcademicSection> sections;
    
    const char* sql = R"(
        SELECT section_id, course_id, section_name, max_students, 
               enrolled_students, status
        FROM course_sections
        WHERE status = 'ACTIVE'
        ORDER BY course_id ASC, section_name ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return sections;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicSection section;
        section.section_id = sqlite3_column_int(stmt, 0);
        section.course_id = sqlite3_column_int(stmt, 1);
        section.section_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        section.max_students = sqlite3_column_int(stmt, 3);
        section.enrolled_students = sqlite3_column_int(stmt, 4);
        section.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
        sections.push_back(section);
    }
    
    sqlite3_finalize(stmt);
    return sections;
}

std::vector<DatabaseManager::AcademicTimeSlot> DatabaseManager::getAllAcademicTimeSlots() {
    std::vector<AcademicTimeSlot> slots;
    
    const char* sql = R"(
        SELECT slot_id, slot_name, day_of_week, start_time, end_time,
               duration_minutes, slot_type, is_available, priority
        FROM time_slots
        WHERE is_available = 1
        ORDER BY day_of_week ASC, start_time ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return slots;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicTimeSlot slot;
        slot.slot_id = sqlite3_column_int(stmt, 0);
        slot.slot_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        slot.day_of_week = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        slot.start_time = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        slot.end_time = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        slot.duration_minutes = sqlite3_column_int(stmt, 5);
        slot.slot_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        slot.is_available = sqlite3_column_int(stmt, 7) == 1;
        slot.priority = sqlite3_column_int(stmt, 8);
        slots.push_back(slot);
    }
    
    sqlite3_finalize(stmt);
    return slots;
}

std::vector<DatabaseManager::AcademicSchedule> DatabaseManager::getAllAcademicSchedules() {
    std::vector<AcademicSchedule> schedules;
    
    const char* sql = R"(
        SELECT schedule_id, course_id, section_id, teacher_id, room_id,
               slot_id, session_number, academic_year, semester, status, notes
        FROM schedule
        WHERE status = 'SCHEDULED'
        ORDER BY course_id ASC, section_id ASC, session_number ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return schedules;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicSchedule schedule;
        schedule.schedule_id = sqlite3_column_int(stmt, 0);
        schedule.course_id = sqlite3_column_int(stmt, 1);
        schedule.section_id = sqlite3_column_int(stmt, 2);
        schedule.teacher_id = sqlite3_column_int(stmt, 3);
        schedule.room_id = sqlite3_column_int(stmt, 4);
        schedule.slot_id = sqlite3_column_int(stmt, 5);
        schedule.session_number = sqlite3_column_int(stmt, 6);
        schedule.academic_year = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
        schedule.semester = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
        schedule.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
        schedule.notes = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
        schedules.push_back(schedule);
    }
    
    sqlite3_finalize(stmt);
    return schedules;
}

// Filtered queries for academic data
std::vector<DatabaseManager::AcademicCourse> DatabaseManager::getCoursesByBatch(const std::string& batch_code) {
    std::vector<AcademicCourse> courses;
    
    const char* sql = R"(
        SELECT c.course_id, c.course_code, c.course_title, c.credit_hours,
               c.class_type, c.session_duration, c.sessions_per_week,
               c.batch_id, c.teacher_id, c.department, c.status
        FROM courses c
        JOIN batches b ON c.batch_id = b.batch_id
        WHERE b.batch_code = ? AND c.status = 'ACTIVE'
        ORDER BY c.course_code ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return courses;
    
    sqlite3_bind_text(stmt, 1, batch_code.c_str(), -1, SQLITE_STATIC);
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        AcademicCourse course;
        course.course_id = sqlite3_column_int(stmt, 0);
        course.course_code = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        course.course_title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        course.credit_hours = sqlite3_column_double(stmt, 3);
        course.class_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        course.session_duration = sqlite3_column_int(stmt, 5);
        course.sessions_per_week = sqlite3_column_int(stmt, 6);
        course.batch_id = sqlite3_column_int(stmt, 7);
        course.teacher_id = sqlite3_column_int(stmt, 8);
        course.department = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
        course.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
        courses.push_back(course);
    }
    
    sqlite3_finalize(stmt);
    return courses;
}

DatabaseManager::PDFScheduleData DatabaseManager::getPDFScheduleData(
    const std::string& batch_code, const std::string& section_name,
    const std::string& academic_year, const std::string& semester) {
    
    PDFScheduleData data;
    data.batch_code = batch_code;
    data.section_name = section_name;
    
    // Get schedules for the specific batch and section
    const char* sql = R"(
        SELECT s.schedule_id, s.course_id, s.section_id, s.teacher_id, s.room_id,
               s.slot_id, s.session_number, s.academic_year, s.semester, s.status, s.notes
        FROM schedule s
        JOIN course_sections cs ON s.section_id = cs.section_id
        JOIN courses c ON cs.course_id = c.course_id
        JOIN batches b ON c.batch_id = b.batch_id
        WHERE b.batch_code = ? AND cs.section_name = ? 
              AND s.academic_year = ? AND s.semester = ?
              AND s.status = 'SCHEDULED'
        ORDER BY s.slot_id ASC, s.session_number ASC
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (stmt) {
        sqlite3_bind_text(stmt, 1, batch_code.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, section_name.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 3, academic_year.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 4, semester.c_str(), -1, SQLITE_STATIC);
        
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            AcademicSchedule schedule;
            schedule.schedule_id = sqlite3_column_int(stmt, 0);
            schedule.course_id = sqlite3_column_int(stmt, 1);
            schedule.section_id = sqlite3_column_int(stmt, 2);
            schedule.teacher_id = sqlite3_column_int(stmt, 3);
            schedule.room_id = sqlite3_column_int(stmt, 4);
            schedule.slot_id = sqlite3_column_int(stmt, 5);
            schedule.session_number = sqlite3_column_int(stmt, 6);
            schedule.academic_year = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
            schedule.semester = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
            schedule.status = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
            schedule.notes = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
            data.schedules.push_back(schedule);
        }
        sqlite3_finalize(stmt);
    }
    
    // Get related courses WITH TITLES, teachers, rooms, and time slots
    // Using getAllAcademicCourses() instead of getCoursesByBatch() to ensure we get ALL courses with their titles
    data.courses = getAllAcademicCourses();
    data.teachers = getAllTeachers();
    data.rooms = getAllRooms();
    data.time_slots = getAllAcademicTimeSlots();
    
    return data;
}

// Academic statistics calculation
DatabaseManager::AcademicStats DatabaseManager::getAcademicStatistics(
    const std::string& academic_year, const std::string& semester) {
    
    AcademicStats stats = {};
    
    // Count total batches
    const char* batchSql = "SELECT COUNT(*) FROM batches WHERE status = 'ACTIVE'";
    sqlite3_stmt* stmt = prepareStatement(batchSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.total_batches = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count total teachers (internal faculty only for academic overview)
    const char* teacherSql = "SELECT COUNT(*) FROM teachers WHERE status = 'ACTIVE' AND external_faculty = 0";
    stmt = prepareStatement(teacherSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.total_teachers = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count total available classrooms
    const char* roomSql = "SELECT COUNT(*) FROM classrooms WHERE status = 'AVAILABLE'";
    stmt = prepareStatement(roomSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.total_classrooms = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count total courses
    const char* courseSql = "SELECT COUNT(*) FROM courses WHERE status = 'ACTIVE'";
    stmt = prepareStatement(courseSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.total_courses = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count total sections
    const char* sectionSql = "SELECT COUNT(*) FROM course_sections WHERE status = 'ACTIVE'";
    stmt = prepareStatement(sectionSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.total_sections = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count scheduled sessions
    const char* scheduledSql = R"(
        SELECT COUNT(*) FROM schedule 
        WHERE academic_year = ? AND semester = ? AND status = 'SCHEDULED'
    )";
    stmt = prepareStatement(scheduledSql);
    if (stmt) {
        sqlite3_bind_text(stmt, 1, academic_year.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, semester.c_str(), -1, SQLITE_STATIC);
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.scheduled_sessions = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Count total expected sessions (courses * sections * sessions_per_week)
    const char* expectedSql = R"(
        SELECT SUM(c.sessions_per_week) as total_expected
        FROM courses c
        JOIN course_sections cs ON c.course_id = cs.course_id
        WHERE c.status = 'ACTIVE' AND cs.status = 'ACTIVE'
    )";
    stmt = prepareStatement(expectedSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.unscheduled_sessions = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
    }
    
    // Calculate completion percentage
    if (stats.unscheduled_sessions > 0) {
        stats.schedule_completion_percentage = 
            (double)stats.scheduled_sessions / stats.unscheduled_sessions * 100.0;
    }
    
    // Count conflicts
    const char* conflictSql = R"(
        SELECT 
            SUM(CASE WHEN conflict_type = 'TEACHER_OVERLAP' THEN 1 ELSE 0 END) as teacher_conflicts,
            SUM(CASE WHEN conflict_type = 'ROOM_OVERLAP' THEN 1 ELSE 0 END) as room_conflicts,
            SUM(CASE WHEN conflict_type = 'BATCH_OVERLAP' THEN 1 ELSE 0 END) as section_conflicts
        FROM schedule_conflicts 
        WHERE is_resolved = 0
    )";
    stmt = prepareStatement(conflictSql);
    if (stmt) {
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            stats.teacher_conflicts = sqlite3_column_int(stmt, 0);
            stats.room_conflicts = sqlite3_column_int(stmt, 1);
            stats.section_conflicts = sqlite3_column_int(stmt, 2);
        }
        sqlite3_finalize(stmt);
    }
    
    return stats;
}

// Bridge between file-based scheduling and database implementation
bool DatabaseManager::saveSchedulingResults(
    const std::vector<Activity>& scheduledActivities,
    const std::vector<std::string>& courseNames,
    const std::string& algorithm,
    const std::string& academic_year,
    const std::string& semester) {
    
    if (!is_connected) {
        last_error = "Database not connected";
        return false;
    }
    
    std::cout << "🔄 Saving scheduling results to database..." << std::endl;
    
    // Start transaction
    if (!beginTransaction()) {
        last_error = "Failed to begin transaction";
        return false;
    }
    
    try {
        // Clear existing schedules for this year/semester
        clearAllSchedules(academic_year, semester);
        
        // Convert activities to academic schedule entries
        bool success = convertActivitiesToAcademicSchedule(scheduledActivities, courseNames, academic_year, semester);
        
        if (success) {
            commitTransaction();
            std::cout << "✅ Successfully saved " << scheduledActivities.size() << " scheduled activities to database" << std::endl;
            return true;
        } else {
            rollbackTransaction();
            std::cerr << "❌ Failed to convert activities to academic schedule" << std::endl;
            return false;
        }
        
    } catch (const std::exception& e) {
        rollbackTransaction();
        last_error = "Error saving scheduling results: " + std::string(e.what());
        return false;
    }
}

bool DatabaseManager::convertActivitiesToAcademicSchedule(
    const std::vector<Activity>& activities,
    const std::vector<std::string>& courseNames,
    const std::string& academic_year,
    const std::string& semester) {
    
    for (size_t i = 0; i < activities.size(); i++) {
        const Activity& activity = activities[i];
        std::string courseName = (i < courseNames.size()) ? courseNames[i] : "Unknown Course";
        
        // Create a time slot for this activity
        if (!createTimeSlotFromActivity(activity)) {
            last_error = "Failed to create time slot for activity " + std::to_string(activity.id);
            return false;
        }
        
        // Retrieve the time slot ID we just created
        int slot_id = -1;
        sqlite3_stmt* stmt = prepareStatement(
            "SELECT slot_id FROM time_slots WHERE start_time = ? AND end_time = ? LIMIT 1");
        if (!stmt) return false;
        
        char start_time[9], end_time[9];
        snprintf(start_time, sizeof(start_time), "%02d:%02d:00", activity.start / 60, activity.start % 60);
        snprintf(end_time, sizeof(end_time), "%02d:%02d:00", activity.end / 60, activity.end % 60);
        
        sqlite3_bind_text(stmt, 1, start_time, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, end_time, -1, SQLITE_STATIC);
        
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            slot_id = sqlite3_column_int(stmt, 0);
        }
        sqlite3_finalize(stmt);
        
        if (slot_id == -1) {
            last_error = "Could not find created time slot for activity " + std::to_string(activity.id);
            return false;
        }
        
        // Get or create course ID
        int course_id = getOrCreateCourseFromActivity(activity, courseName);
        if (course_id == -1) {
            last_error = "Failed to get/create course for activity " + std::to_string(activity.id);
            return false;
        }
        
        // Determine course type and capacity from activity duration 
        std::string course_type = (activity.end - activity.start) > 120 ? "LAB" : "THEORY";
        int required_capacity = 30; // Default capacity since Activity doesn't have student count
        
        // Create academic schedule entry
        AcademicSchedule schedule;
        schedule.schedule_id = 0; // Auto-increment
        schedule.course_id = course_id;
        schedule.section_id = getDefaultSectionId();
        schedule.teacher_id = getDefaultTeacherId();
        schedule.room_id = getDefaultRoomId(course_type, required_capacity);
        schedule.slot_id = slot_id;
        schedule.session_number = 1;
        schedule.academic_year = academic_year;
        schedule.semester = semester;
        schedule.status = "SCHEDULED";
        schedule.notes = "Auto-scheduled from file input";
        
        if (!insertAcademicSchedule(schedule)) {
            last_error = "Failed to insert academic schedule for activity " + std::to_string(activity.id);
            return false;
        }
    }
    
    return true;
}

bool DatabaseManager::createTimeSlotFromActivity(const Activity& activity) {
    const char* sql = R"(
        INSERT OR IGNORE INTO time_slots (slot_name, day_of_week, start_time, end_time, 
                                         duration_minutes, slot_type, is_available, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return false;
    
    // Generate slot name
    std::string slot_name = "SLOT_" + std::to_string(activity.start) + "_" + std::to_string(activity.end);
    
    // For simplicity, assign to Monday (could be enhanced to distribute across days)
    std::string day_of_week = "MON";
    std::string start_time = std::to_string(activity.start) + ":00:00";
    std::string end_time = std::to_string(activity.end) + ":00:00";
    int duration_minutes = (activity.end - activity.start) * 60;
    std::string slot_type = "THEORY"; // Default to theory class
    
    sqlite3_bind_text(stmt, 1, slot_name.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, day_of_week.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, start_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, end_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 5, duration_minutes);
    sqlite3_bind_text(stmt, 6, slot_type.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 7, 1); // is_available = true
    sqlite3_bind_int(stmt, 8, 5); // priority = 5 (medium)
    
    bool success = (sqlite3_step(stmt) == SQLITE_DONE);
    sqlite3_finalize(stmt);
    
    return success;
}

int DatabaseManager::getOrCreateCourseFromActivity(const Activity& activity, const std::string& courseName) {
    // First try to find existing course by title
    const char* findSql = R"(
        SELECT course_id FROM courses WHERE course_title = ? LIMIT 1
    )";
    
    sqlite3_stmt* stmt = prepareStatement(findSql);
    if (!stmt) return -1;
    
    sqlite3_bind_text(stmt, 1, courseName.c_str(), -1, SQLITE_STATIC);
    
    int course_id = -1;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        course_id = sqlite3_column_int(stmt, 0);
        sqlite3_finalize(stmt);
        return course_id;
    }
    sqlite3_finalize(stmt);
    
    // Course doesn't exist, create new one
    const char* insertSql = R"(
        INSERT INTO courses (course_code, course_title, credit_hours, class_type, 
                           session_duration, sessions_per_week, batch_id, teacher_id, 
                           department, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    )";
    
    stmt = prepareStatement(insertSql);
    if (!stmt) return -1;
    
    std::string course_code = "CS" + std::to_string(activity.id);
    double credit_hours = 3.0; // Default credit hours
    std::string class_type = "THEORY";
    int session_duration = (activity.end - activity.start) * 60; // in minutes
    int sessions_per_week = 2; // Default
    int batch_id = 1; // Default to first batch
    int teacher_id = getDefaultTeacherId();
    std::string department = "CSE";
    std::string status = "ACTIVE";
    
    sqlite3_bind_text(stmt, 1, course_code.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, courseName.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_double(stmt, 3, credit_hours);
    sqlite3_bind_text(stmt, 4, class_type.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 5, session_duration);
    sqlite3_bind_int(stmt, 6, sessions_per_week);
    sqlite3_bind_int(stmt, 7, batch_id);
    sqlite3_bind_int(stmt, 8, teacher_id);
    sqlite3_bind_text(stmt, 9, department.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 10, status.c_str(), -1, SQLITE_STATIC);
    
    if (sqlite3_step(stmt) == SQLITE_DONE) {
        course_id = sqlite3_last_insert_rowid(db);
    }
    sqlite3_finalize(stmt);
    
    return course_id;
}

int DatabaseManager::getDefaultTeacherId() {
    const char* sql = "SELECT teacher_id FROM teachers WHERE status = 'ACTIVE' ORDER BY teacher_id LIMIT 1";
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return 1; // Fallback to ID 1
    
    int teacher_id = 1;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        teacher_id = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    return teacher_id;
}

int DatabaseManager::getDefaultSectionId() {
    const char* sql = "SELECT section_id FROM course_sections WHERE status = 'ACTIVE' ORDER BY section_id LIMIT 1";
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return 1; // Fallback to ID 1
    
    int section_id = 1;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        section_id = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    return section_id;
}

bool DatabaseManager::clearAllSchedules(const std::string& academic_year, const std::string& semester) {
    const char* sql = R"(
        DELETE FROM schedule 
        WHERE academic_year = ? AND semester = ?
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return false;
    
    sqlite3_bind_text(stmt, 1, academic_year.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, semester.c_str(), -1, SQLITE_STATIC);
    
    bool success = (sqlite3_step(stmt) == SQLITE_DONE);
    sqlite3_finalize(stmt);
    
    if (success) {
        std::cout << "🗑️ Cleared existing schedules for " << academic_year << " " << semester << std::endl;
    }
    
    return success;
}

bool DatabaseManager::insertAcademicSchedule(const AcademicSchedule& schedule) {
    const char* sql = R"(
        INSERT INTO schedule (course_id, section_id, teacher_id, room_id, slot_id, 
                            session_number, academic_year, semester, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return false;
    
    sqlite3_bind_int(stmt, 1, schedule.course_id);
    sqlite3_bind_int(stmt, 2, schedule.section_id);
    sqlite3_bind_int(stmt, 3, schedule.teacher_id);
    sqlite3_bind_int(stmt, 4, schedule.room_id);
    sqlite3_bind_int(stmt, 5, schedule.slot_id);
    sqlite3_bind_int(stmt, 6, schedule.session_number);
    sqlite3_bind_text(stmt, 7, schedule.academic_year.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 8, schedule.semester.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 9, schedule.status.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 10, schedule.notes.c_str(), -1, SQLITE_STATIC);
    
    bool success = (sqlite3_step(stmt) == SQLITE_DONE);
    sqlite3_finalize(stmt);
    
    return success;
}

int DatabaseManager::getDefaultRoomId(const std::string& course_type, int required_capacity) {
    // Build query to find appropriate room based on type and capacity
    const char* sql = R"(
        SELECT room_id 
        FROM classrooms 
        WHERE status = 'AVAILABLE' 
        AND room_type = ? 
        AND capacity >= ?
        ORDER BY ABS(capacity - ?) ASC, room_id ASC 
        LIMIT 1
    )";
    
    sqlite3_stmt* stmt = prepareStatement(sql);
    if (!stmt) return 1; // Fallback to ID 1
    
    // Bind parameters
    sqlite3_bind_text(stmt, 1, course_type.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 2, required_capacity);
    sqlite3_bind_int(stmt, 3, required_capacity); // For optimal capacity fit
    
    int room_id = 1;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        room_id = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    return room_id;
}

std::pair<int, int> DatabaseManager::getRoomTypeCounts() {
    int theory_rooms = 0;
    int lab_rooms = 0;
    
    const char* sql = R"(
        SELECT room_type, COUNT(*) as count
        FROM classrooms 
        WHERE status = 'AVAILABLE'
        GROUP BY room_type
    )";
    
    sqlite3_stmt* stmt;
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        return {0, 0};
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::string room_type = (char*)sqlite3_column_text(stmt, 0);
        int count = sqlite3_column_int(stmt, 1);
        
        if (room_type == "THEORY") {
            theory_rooms = count;
        } else if (room_type == "LAB") {
            lab_rooms = count;
        }
    }
    
    sqlite3_finalize(stmt);
    return {theory_rooms, lab_rooms};
}
