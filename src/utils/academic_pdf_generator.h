#ifndef ACADEMIC_PDF_GENERATOR_H
#define ACADEMIC_PDF_GENERATOR_H

#include <vector>
#include <string>
#include <map>
#include <memory>
#include "../database/database_manager.h"
#include "pdf_generator.h"

// Academic Course Information Structure
struct AcademicCourse {
    std::string courseCode;        // e.g., "CSE2201"
    std::string courseTitle;       // e.g., "Data Structures"
    std::string facultyName;       // e.g., "Dr. Abdul Hamid"
    std::string facultyDesignation; // e.g., "Professor"
    std::string roomCode;          // e.g., "CR302"
    std::string sectionName;       // e.g., "A" or "B"
    std::string batchName;         // e.g., "BCSE23"
    double creditHours;            // e.g., 3.0 or 1.5
    std::string classType;         // "THEORY" or "LAB"
    int sessionDuration;           // in minutes (90 for theory, 180 for lab)
    std::string timeSlot;          // e.g., "SUN_S1"
    std::string dayOfWeek;         // e.g., "SUN"
    std::string startTime;         // e.g., "08:30"
    std::string endTime;           // e.g., "10:00"
    int sessionNumber;             // 1, 2 for multiple sessions per week
    int enrolledStudents;          // Number of enrolled students
    bool isExternal;               // External faculty flag
};

// Professional Schedule Statistics
struct ScheduleStatistics {
    int totalCourses;
    int totalSections;
    int totalFaculty;
    int totalRooms;
    int theoryClasses;
    int labClasses;
    int totalCreditHours;
    double scheduleCompleteness;
    int conflictsResolved;
    std::string algorithmUsed;
    std::string generationTime;
};

// Time Slot Information Structure
struct TimeSlotInfo {
    std::string slotCode;     // e.g., "S1"
    std::string startTime;    // e.g., "08:30"
    std::string endTime;      // e.g., "10:00"
    std::string displayName;  // e.g., "8:30 AM - 10:00 AM"
    std::string slotName;     // e.g., "S1"
    std::string slotType;     // e.g., "THEORY" or "LAB"
};

class AcademicPDFGenerator {
private:
    std::shared_ptr<DatabaseManager> dbManager;
    
public:
    // Constructor with database integration
    explicit AcademicPDFGenerator(std::shared_ptr<DatabaseManager> db = nullptr);
    
    // Database-integrated schedule generation
    bool generateScheduleFromDatabase(
        const std::string& batchCode,
        const std::string& sectionName,
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    // Generate complete university schedule (all batches and sections)
    bool generateUniversitySchedule(
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    // Generate comprehensive university routine (proper format with days as rows, rooms as sub-rows, time slots as columns)
    bool generateComprehensiveUniversityRoutine(
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    // Generate faculty-wise schedule from database
    bool generateFacultyScheduleFromDB(
        const std::string& facultyCode,
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    // Generate room utilization report from database
    bool generateRoomUtilizationFromDB(
        const std::string& roomCode,
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    // Generate comparative schedule (before/after optimization)
    bool generateComparativeSchedule(
        const std::vector<AcademicCourse>& beforeOptimization,
        const std::vector<AcademicCourse>& afterOptimization,
        const std::string& outputPath,
        const std::string& algorithm
    );
    
    // CSV to Academic Course conversion for enhanced weekly routine generation
    std::vector<AcademicCourse> convertActivitiesToAcademicCourses(
        const std::vector<Activity>& activities,
        const std::vector<std::string>& courseNames,
        const std::vector<std::string>& teacherNames
    );
    
    // Generate weekly routine from CSV input
    bool generateWeeklyRoutineFromCSV(
        const std::vector<Activity>& activities,
        const std::vector<std::string>& courseNames, 
        const std::vector<std::string>& teacherNames,
        const std::string& outputPath,
        const std::string& algorithm = "Dynamic Programming"
    );

private:
    // Helper methods for HTML generation
    bool generateFacultyScheduleHTML(
        const std::vector<AcademicCourse>& courses,
        const std::string& facultyName,
        const std::string& htmlPath,
        const std::string& algorithm
    );
    
    bool generateRoomScheduleHTML(
        const std::vector<AcademicCourse>& courses,
        const std::string& roomCode,
        const std::string& htmlPath,
        const std::string& algorithm
    );
    
    // Original methods from the existing implementation
    bool generateAcademicSchedulePDF(
        const std::vector<AcademicCourse>& courses,
        const std::string& outputPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    bool generateAcademicScheduleHTML(
        const std::vector<AcademicCourse>& courses,
        const std::string& htmlPath,
        const std::string& algorithm,
        const std::string& academicYear = "2024-25",
        const std::string& semester = "Spring"
    );
    
    bool generateSectionSchedule(
        const std::vector<AcademicCourse>& courses,
        const std::string& sectionName,
        const std::string& batchName,
        const std::string& outputPath,
        const std::string& algorithm
    );
    
    bool generateFacultySchedule(
        const std::vector<AcademicCourse>& courses,
        const std::string& facultyName,
        const std::string& outputPath,
        const std::string& algorithm
    );
    
    bool generateRoomSchedule(
        const std::vector<AcademicCourse>& courses,
        const std::string& roomCode,
        const std::string& outputPath,
        const std::string& algorithm
    );

private:
    // Database conversion helpers
    std::vector<AcademicCourse> convertDBDataToAcademicCourses(
        const DatabaseManager::PDFScheduleData& pdfData
    );
    
    std::vector<AcademicCourse> convertSchedulesToCourses(
        const std::vector<DatabaseManager::AcademicSchedule>& schedules,
        const std::vector<DatabaseManager::AcademicCourse>& allCourses,
        const std::vector<DatabaseManager::AcademicTeacher>& allTeachers,
        const std::vector<DatabaseManager::Room>& allRooms,
        const std::vector<DatabaseManager::AcademicTimeSlot>& allTimeSlots
    );
    
    // Schedule statistics calculation
    ScheduleStatistics calculateStatistics(
        const std::vector<AcademicCourse>& courses,
        const std::string& algorithm
    );
    
    // Enhanced HTML generation with professional academic styling
    std::string generateProfessionalHeader(
        const std::string& title,
        const std::string& batchCode,
        const std::string& sectionName,
        const std::string& academicYear,
        const std::string& semester
    );
    
    std::string generateUniversityBranding();
    
    // New comprehensive routine layout generators
    std::string generateComprehensiveRoutineGrid(const std::vector<AcademicCourse>& allCourses);
    std::string generateDayBasedScheduleTable(const std::vector<AcademicCourse>& allCourses);
    std::string generateAllBatchesStatistics(const std::vector<AcademicCourse>& allCourses);
    
    // Comprehensive routine HTML generation
    bool generateComprehensiveRoutineHTML(
        const std::vector<AcademicCourse>& courses,
        const std::string& htmlPath,
        const std::string& algorithm,
        const std::string& academicYear,
        const std::string& semester
    );
    std::string generateProfessionalStatistics(const ScheduleStatistics& stats);
    std::string generateWeeklyScheduleGrid(const std::vector<AcademicCourse>& courses);
    std::string generateCourseDetailsList(const std::vector<AcademicCourse>& courses);
    std::string generateFacultyContactInfo(const std::vector<AcademicCourse>& courses);
    std::string generateRoomInformation(const std::vector<AcademicCourse>& courses);
    
    // Academic formatting utilities
    std::string formatAcademicTime(const std::string& time);
    std::string getAcademicDayName(const std::string& dayCode);
    std::string getBatchDisplayName(const std::string& batchCode);
    std::string getCourseTypeIcon(const std::string& classType);
    std::string getFacultyTypeIcon(bool isExternal);
    
    // Missing method declarations for compatibility
    std::string generateAcademicCSS();
    std::string generateTimeSlotGrid(const std::vector<AcademicCourse>& courses);
    std::string generateStatistics(const std::vector<AcademicCourse>& courses);
    std::string generateCourseDetails(const std::vector<AcademicCourse>& courses);
    std::string formatCreditHours(double credits);
    std::string getDayName(const std::string& dayCode);
    std::string formatTimeRange(const std::string& startTime, const std::string& endTime);
    std::string getCourseTypeClass(const std::string& classType);
    
    // Helper methods for time slot grid
    std::vector<std::string> getWeekDays();
    std::vector<TimeSlotInfo> getTimeSlots();
    std::vector<AcademicCourse> getCoursesByTimeSlot(
        const std::vector<AcademicCourse>& courses,
        const std::string& day,
        const std::string& timeSlot
    );
    
    // Professional CSS generation
    std::string generateUniversityCSS();
    std::string generateResponsiveCSS();
    std::string generatePrintCSS();
    
    // Utility helpers
    std::string getCurrentTimestamp();
    std::string formatDuration(const std::string& startTime, const std::string& endTime);
    std::string getClassTypeColor(const std::string& classType);
    std::string getBatchColor(const std::string& batchCode);
    std::string extractSlotPattern(const std::string& slotName);
};

#endif // ACADEMIC_PDF_GENERATOR_H
