#ifndef DATABASE_MANAGER_H
#define DATABASE_MANAGER_H

#include <string>
#include <vector>
#include <memory>
#include <sqlite3.h>
#include "../scheduler.h"

/**
 * @brief Database Manager for Conflict-Free Scheduling System
 * 
 * This class provides a comprehensive interface for database operations
 * including SQLite (default) and PostgreSQL support for production use.
 */
class DatabaseManager {
private:
    sqlite3* db;
    std::string db_path;
    bool is_connected;
    
    // Error handling
    std::string last_error;
    
    // Connection management
    bool openConnection();
    void closeConnection();
    
    // Schema management
    bool createTables();
    bool executeSQLFile(const std::string& filename);
    
    // Query helpers
    bool executeQuery(const std::string& query);
    sqlite3_stmt* prepareStatement(const std::string& query);
    
public:
    /**
     * @brief Constructor - initializes database connection
     * @param database_path Path to SQLite database file
     */
    explicit DatabaseManager(const std::string& database_path = "data/scheduling.db");
    
    /**
     * @brief Destructor - ensures proper cleanup
     */
    ~DatabaseManager();
    
    // Database initialization
    bool initialize();
    bool connect(); // Just open connection without creating tables
    bool loadSampleData();
    bool resetDatabase();
    
    // Course operations
    bool insertCourse(const Activity& course);
    bool updateCourse(const Activity& course);
    bool deleteCourse(int course_id);
    std::vector<Activity> getAllCourses();
    std::pair<std::vector<Activity>, std::vector<std::string>> getAllCoursesWithTitles();
    std::vector<Activity> getCoursesBySemester(int semester);
    Activity getCourseById(int course_id);
    
    // Room operations
    struct Room {
        int room_id;
        std::string room_code;
        std::string room_name;
        int capacity;
        std::string room_type;
        std::string equipment;
        std::string building;
        int floor;
        bool is_available;
    };
    
    bool insertRoom(const Room& room);
    bool updateRoom(const Room& room);
    bool deleteRoom(int room_id);
    std::vector<Room> getAllRooms();
    std::vector<Room> getAvailableRooms();
    std::vector<Room> getRoomsByType(const std::string& room_type);
    Room getRoomById(int room_id);
    
    // Time slot operations
    struct TimeSlot {
        int slot_id;
        int day_of_week;
        std::string start_time;
        std::string end_time;
        std::string slot_type;
        bool is_available;
    };
    
    bool insertTimeSlot(const TimeSlot& slot);
    bool updateTimeSlot(const TimeSlot& slot);
    bool deleteTimeSlot(int slot_id);
    std::vector<TimeSlot> getAllTimeSlots();
    std::vector<TimeSlot> getAvailableTimeSlots();
    std::vector<TimeSlot> getTimeSlotsByDay(int day_of_week);
    TimeSlot getTimeSlotById(int slot_id);
    
    // Schedule assignment operations
    struct ScheduleAssignment {
        int assignment_id;
        int course_id;
        int room_id;
        int slot_id;
        std::string semester;
        std::string academic_year;
        std::string status;
    };
    
    bool insertScheduleAssignment(const ScheduleAssignment& assignment);
    bool updateScheduleAssignment(const ScheduleAssignment& assignment);
    bool deleteScheduleAssignment(int assignment_id);
    std::vector<ScheduleAssignment> getAllAssignments();
    std::vector<ScheduleAssignment> getAssignmentsBySemester(const std::string& semester);
    std::vector<ScheduleAssignment> getAssignmentsByRoom(int room_id);
    bool isSlotAvailable(int room_id, int slot_id, const std::string& semester);
    
    // Conflict management
    struct ConflictLog {
        int conflict_id;
        std::string conflict_type;
        std::string description;
        int course_id_1;
        int course_id_2;
        int room_id;
        int slot_id;
        bool resolved;
        std::string resolution_method;
    };
    
    bool logConflict(const ConflictLog& conflict);
    bool resolveConflict(int conflict_id, const std::string& resolution_method);
    std::vector<ConflictLog> getUnresolvedConflicts();
    std::vector<ConflictLog> getAllConflicts();
    
    // Scheduling preferences
    struct SchedulingPreference {
        int preference_id;
        int course_id;
        int preferred_slot_id;
        int preferred_room_id;
        std::string preference_type;
        int priority;
        std::string notes;
    };
    
    bool insertPreference(const SchedulingPreference& preference);
    bool updatePreference(const SchedulingPreference& preference);
    bool deletePreference(int preference_id);
    std::vector<SchedulingPreference> getPreferencesByCourse(int course_id);
    
    // Analytics and reporting
    struct ScheduleStats {
        int total_courses;
        int total_rooms;
        int total_time_slots;
        int scheduled_courses;
        int unscheduled_courses;
        int room_utilization_percentage;
        int conflicts_detected;
        int conflicts_resolved;
    };
    
    ScheduleStats getScheduleStatistics();
    std::vector<std::pair<std::string, int>> getRoomUtilization();
    std::vector<std::pair<std::string, int>> getTimeSlotUtilization();
    
    // Validation and constraints
    bool validateScheduleAssignment(const ScheduleAssignment& assignment);
    bool checkRoomCapacity(int course_id, int room_id);
    bool checkTimeConflicts(int room_id, int slot_id, const std::string& semester);
    bool checkInstructorConflicts(const std::string& instructor, int slot_id, const std::string& semester);
    
    // Backup and restore
    bool backupDatabase(const std::string& backup_path);
    bool restoreDatabase(const std::string& backup_path);
    
    // Error handling
    std::string getLastError() const { return last_error; }
    bool hasError() const { return !last_error.empty(); }
    void clearError() { last_error.clear(); }
    
    // Connection status
    bool isConnected() const { return is_connected; }
    
    // Transaction management
    bool beginTransaction();
    bool commitTransaction();
    bool rollbackTransaction();
    
    // Academic structures for BUP integration
    struct AcademicBatch {
        int batch_id;
        std::string batch_code;      // e.g., "BCSE23"
        std::string batch_name;      // e.g., "Bachelor of Computer Science Engineering - 2023"
        int year_level;              // 1, 2, 3, 4
        int semester;                // 1, 2, 3, 4, 5, 6, 7, 8
        int total_sections;          // Usually 2 (A and B)
        std::string status;          // ACTIVE, INACTIVE, GRADUATED
    };
    
    struct AcademicTeacher {
        int teacher_id;
        std::string teacher_code;    // e.g., "DR_ASM", "EXT_MSH"
        std::string full_name;       // e.g., "Dr. ASM Shihavuddin"
        std::string designation;     // e.g., "Professor", "Assistant Professor"
        std::string department;      // e.g., "CSE"
        std::string email;
        std::string phone;
        std::string availability_start;  // e.g., "08:30"
        std::string availability_end;    // e.g., "17:30"
        bool external_faculty;       // true for external teachers
        int max_hours_per_week;
        std::string status;
    };
    
    struct AcademicCourse {
        int course_id;
        std::string course_code;     // e.g., "CSE2201"
        std::string course_title;    // e.g., "Data Structures"
        double credit_hours;         // e.g., 3.0, 1.5
        std::string class_type;      // THEORY, LAB
        int session_duration;        // 90 min for theory, 180 min for lab
        int sessions_per_week;       // Usually 2 for theory, 1 for lab
        int batch_id;
        int teacher_id;
        std::string department;
        std::string status;
    };
    
    struct AcademicSection {
        int section_id;
        int course_id;
        std::string section_name;    // A, B
        int max_students;            // Usually 40
        int enrolled_students;
        std::string status;
    };
    
    struct AcademicTimeSlot {
        int slot_id;
        std::string slot_name;       // e.g., "SUN_S1", "MON_L1"
        std::string day_of_week;     // SUN, MON, TUE, WED, THU
        std::string start_time;      // e.g., "08:30"
        std::string end_time;        // e.g., "10:00"
        int duration_minutes;        // 90 or 180
        std::string slot_type;       // THEORY, LAB
        bool is_available;
        int priority;                // Higher priority = preferred slots
    };
    
    struct AcademicSchedule {
        int schedule_id;
        int course_id;
        int section_id;
        int teacher_id;
        int room_id;
        int slot_id;
        int session_number;          // 1, 2 for multiple sessions per week
        std::string academic_year;   // e.g., "2024-25"
        std::string semester;        // SPRING, SUMMER, FALL
        std::string status;
        std::string notes;
    };
    
    // Academic data operations
    std::vector<AcademicBatch> getAllBatches();
    std::vector<AcademicTeacher> getAllTeachers();
    std::vector<AcademicCourse> getAllAcademicCourses();
    std::vector<AcademicSection> getAllSections();
    std::vector<AcademicTimeSlot> getAllAcademicTimeSlots();
    std::vector<AcademicSchedule> getAllAcademicSchedules();
    
    // Filtered queries for academic data
    std::vector<AcademicCourse> getCoursesByBatch(const std::string& batch_code);
    std::vector<AcademicSchedule> getScheduleBySection(const std::string& batch_code, const std::string& section_name);
    std::vector<AcademicSchedule> getScheduleByTeacher(int teacher_id);
    std::vector<AcademicSchedule> getScheduleByRoom(const std::string& room_code);
    std::vector<AcademicSchedule> getScheduleByDay(const std::string& day_of_week);
    
    // Academic schedule generation support
    bool insertAcademicSchedule(const AcademicSchedule& schedule);
    bool updateAcademicSchedule(const AcademicSchedule& schedule);
    bool deleteAcademicSchedule(int schedule_id);
    bool clearAllSchedules(const std::string& academic_year, const std::string& semester);
    
    // Professional schedule validation
    bool validateAcademicSchedule(const AcademicSchedule& schedule);
    bool checkTeacherAvailability(int teacher_id, int slot_id);
    bool checkRoomAvailability(int room_id, int slot_id);
    bool checkSectionConflict(int section_id, int slot_id);
    
    // Academic reporting
    struct AcademicStats {
        int total_batches;
        int total_teachers;
        int total_classrooms;
        int total_courses;
        int total_sections;
        int scheduled_sessions;
        int unscheduled_sessions;
        double schedule_completion_percentage;
        int teacher_conflicts;
        int room_conflicts;
        int section_conflicts;
    };
    
    AcademicStats getAcademicStatistics(const std::string& academic_year, const std::string& semester);
    
    // Professional PDF data export
    struct PDFScheduleData {
        std::string batch_code;
        std::string section_name;
        std::vector<AcademicSchedule> schedules;
        std::vector<AcademicCourse> courses;
        std::vector<AcademicTeacher> teachers;
        std::vector<Room> rooms;
        std::vector<AcademicTimeSlot> time_slots;
    };
    
    PDFScheduleData getPDFScheduleData(const std::string& batch_code, const std::string& section_name, 
                                      const std::string& academic_year, const std::string& semester);
    
    // Bridge between file-based scheduling and database
    bool saveSchedulingResults(
        const std::vector<Activity>& scheduledActivities,
        const std::vector<std::string>& courseNames,
        const std::string& algorithm,
        const std::string& academic_year = "2024-25",
        const std::string& semester = "SPRING"
    );
    
    bool convertActivitiesToAcademicSchedule(
        const std::vector<Activity>& activities,
        const std::vector<std::string>& courseNames,
        const std::string& academic_year,
        const std::string& semester
    );
    
    // Create time slots for file-based activity times
    bool createTimeSlotFromActivity(const Activity& activity);
    
    // Get or create course mapping for file input
    int getOrCreateCourseFromActivity(const Activity& activity, const std::string& courseName);
    
    // Get default assignments for file-based scheduling
    int getDefaultTeacherId();
    int getDefaultRoomId(const std::string& course_type = "THEORY", int required_capacity = 30);
    int getAvailableRoomAtTimeSlot(int slot_id, const std::string& course_type = "THEORY", int required_capacity = 30);
    int getDistributedRoomId(const std::string& course_type = "THEORY", int required_capacity = 30);
    int getDefaultSectionId();
    
    // Get room type counts
    std::pair<int, int> getRoomTypeCounts(); // returns {theory_rooms, lab_rooms}

    // PostgreSQL support (future implementation)
    bool connectToPostgreSQL(const std::string& connection_string);
    bool migrateToPostgreSQL();
};

#endif // DATABASE_MANAGER_H
