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
    bool loadSampleData();
    bool resetDatabase();
    
    // Course operations
    bool insertCourse(const Activity& course);
    bool updateCourse(const Activity& course);
    bool deleteCourse(int course_id);
    std::vector<Activity> getAllCourses();
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
    
    // PostgreSQL support (future implementation)
    bool connectToPostgreSQL(const std::string& connection_string);
    bool migrateToPostgreSQL();
};

#endif // DATABASE_MANAGER_H
