#ifndef ENHANCED_ROUTINE_GENERATOR_H
#define ENHANCED_ROUTINE_GENERATOR_H

#include "database_manager.h"
#include <vector>
#include <string>
#include <map>
#include <set>

/**
 * @brief Enhanced Routine Generator for BUP CSE Department
 * 
 * This class generates conflict-free academic schedules based on:
 * - 4 batches: BCSE22, BCSE23, BCSE24, BCSE25
 * - Course distribution per batch as specified
 * - 5 classrooms: CR302, CR303, CR304, CR504, CR1003
 * - Time slots: Sunday-Thursday, 8:30 AM - 5:00 PM with lunch break
 * - Faculty availability and preferences
 */
class EnhancedRoutineGenerator {
public:
    struct CourseScheduleInfo {
        int course_id;
        std::string course_code;
        std::string course_title;
        std::string batch_code;
        std::string section_name;
        double credit_hours;
        std::string class_type;        // THEORY or LAB
        int session_duration;          // 90 min for theory, 180 min for lab
        int sessions_per_week;         // 2 for theory, 1 for lab
        int teacher_id;
        std::string faculty_name;
        bool is_external_faculty;
        
        // Scheduling constraints
        std::vector<std::string> preferred_days;
        std::vector<std::string> preferred_times;
        std::vector<std::string> unavailable_times;
    };
    
    struct TimeSlotInfo {
        int slot_id;
        std::string slot_name;
        std::string day_of_week;
        std::string start_time;
        std::string end_time;
        int duration_minutes;
        std::string slot_type;         // REGULAR, LUNCH, BREAK
        bool is_available;
    };
    
    struct RoomInfo {
        int room_id;
        std::string room_code;
        int capacity;
        std::string room_type;         // THEORY, LAB, BOTH
        std::string building;
        bool is_available;
    };
    
    struct ScheduleAssignment {
        CourseScheduleInfo course;
        TimeSlotInfo time_slot;
        RoomInfo room;
        int session_number;            // 1 or 2 for multiple sessions per week
        bool has_conflict;
        std::vector<std::string> conflict_reasons;
    };
    
    struct ConflictInfo {
        std::string conflict_type;     // TEACHER, ROOM, BATCH, TIME
        std::string description;
        std::vector<int> conflicting_assignments;
        std::string severity;          // LOW, MEDIUM, HIGH, CRITICAL
    };
    
private:
    std::shared_ptr<DatabaseManager> dbManager;
    
    // Cache for optimization
    std::vector<CourseScheduleInfo> allCourses;
    std::vector<TimeSlotInfo> allTimeSlots;
    std::vector<RoomInfo> allRooms;
    std::map<std::string, std::vector<CourseScheduleInfo>> coursesByBatch;
    std::map<int, std::vector<TimeSlotInfo>> teacherAvailability;
    
    // Scheduling state
    std::vector<ScheduleAssignment> currentSchedule;
    std::vector<ConflictInfo> detectedConflicts;
    
    // Algorithm parameters
    bool prioritizeExternalFaculty;
    bool minimizeGaps;
    bool balanceRoomUsage;
    int maxTriesPerCourse;
    
    // Helper functions for gap minimization
    double calculateGapScore(const TimeSlotInfo& candidate_slot, const std::vector<ScheduleAssignment>& existing_classes) const;
    double timeStringToMinutes(const std::string& timeStr) const;
    
public:
    explicit EnhancedRoutineGenerator(std::shared_ptr<DatabaseManager> dbMgr);
    
    // Main scheduling functions
    bool generateCompleteRoutine(const std::string& academic_year = "2024-25", 
                                const std::string& semester = "Spring");
    bool generateBatchRoutine(const std::string& batch_code, 
                             const std::string& academic_year = "2024-25",
                             const std::string& semester = "Spring");
    bool generateFacultyRoutine(const std::string& faculty_code,
                               const std::string& academic_year = "2024-25",
                               const std::string& semester = "Spring");
    
    // Constraint checking
    bool checkTeacherConflict(const ScheduleAssignment& assignment) const;
    bool checkRoomConflict(const ScheduleAssignment& assignment) const;
    bool checkBatchConflict(const ScheduleAssignment& assignment) const;
    bool checkTimeConstraints(const ScheduleAssignment& assignment) const;
    bool checkFacultyAvailability(const ScheduleAssignment& assignment) const;
    
    // Optimization functions
    std::vector<ScheduleAssignment> optimizeSchedule(const std::vector<ScheduleAssignment>& initial_schedule);
    void resolveConflicts();
    void balanceWorkload();
    void minimizeGapsBetweenClasses();
    
    // Output generation
    bool generateDayWiseRoutinePDF(const std::string& output_path);
    bool generateFacultyWiseRoutinePDF(const std::string& output_path);
    bool generateRoomWiseRoutinePDF(const std::string& output_path);
    bool generateBatchWiseRoutinePDF(const std::string& batch_code, const std::string& output_path);
    
    // Utility functions
    void loadCourseData();
    void loadTimeSlotData();
    void loadRoomData();
    void loadFacultyConstraints();
    
    std::vector<TimeSlotInfo> getAvailableSlots(const CourseScheduleInfo& course, 
                                               const std::string& day) const;
    std::vector<RoomInfo> getAvailableRooms(const CourseScheduleInfo& course, 
                                           const TimeSlotInfo& time_slot) const;
    
    // Statistics and reporting
    struct ScheduleStatistics {
        int total_courses;
        int scheduled_courses;
        int total_conflicts;
        int teacher_conflicts;
        int room_conflicts;
        int batch_conflicts;
        double schedule_efficiency;
        double room_utilization;
        std::map<std::string, int> courses_per_batch;
        std::map<std::string, double> faculty_workload;
    };
    
    ScheduleStatistics getScheduleStatistics() const;
    void printConflictReport() const;
    void printScheduleSummary() const;
    
    // Getters
    const std::vector<ScheduleAssignment>& getCurrentSchedule() const { return currentSchedule; }
    const std::vector<ConflictInfo>& getDetectedConflicts() const { return detectedConflicts; }
    
    // Algorithm configuration
    void setPrioritizeExternalFaculty(bool enable) { prioritizeExternalFaculty = enable; }
    void setMinimizeGaps(bool enable) { minimizeGaps = enable; }
    void setBalanceRoomUsage(bool enable) { balanceRoomUsage = enable; }
    void setMaxTriesPerCourse(int tries) { maxTriesPerCourse = tries; }
};

#endif // ENHANCED_ROUTINE_GENERATOR_H
