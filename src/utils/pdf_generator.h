#ifndef PDF_GENERATOR_H
#define PDF_GENERATOR_H

#include "../scheduler.h"
#include "../database/database_manager.h"
#include <vector>
#include <string>

/**
 * @brief Department statistics for PDF generation
 */
struct DepartmentStats {
    int total_batches;
    int total_teachers;
    int total_sections;
    int total_classrooms;
    int theory_rooms;
    int lab_rooms;
};

/**
 * @brief PDF schedule generator
 */
class PDFGenerator {
public:
    /**
     * @brief Generate a PDF schedule from activities
     * @param schedule Vector of scheduled activities
     * @param courseNames Vector of course names (optional)
     * @param outputPath Path for the output PDF
     * @param algorithm Algorithm name used
     * @return true if successful, false otherwise
     */
    static bool generateSchedulePDF(
        const std::vector<Activity>& schedule,
        const std::vector<std::string>& courseNames,
        const std::vector<std::string>& teacherNames,
        const std::string& outputPath,
        const std::string& algorithm = "Dynamic Programming"
    );
    
    /**
     * @brief Generate a PDF schedule from activities with department statistics
     * @param schedule Vector of scheduled activities
     * @param courseNames Vector of course names (optional)
     * @param outputPath Path for the output PDF
     * @param deptStats Department statistics
     * @param algorithm Algorithm name used
     * @return true if successful, false otherwise
     */
    static bool generateSchedulePDF(
        const std::vector<Activity>& schedule,
        const std::vector<std::string>& courseNames,
        const std::vector<std::string>& teacherNames,
        const std::string& outputPath,
        const DepartmentStats& deptStats,
        const std::string& algorithm = "Dynamic Programming"
    );
     /**
     * @brief Generate HTML version of the schedule
     * @param schedule Vector of scheduled activities
     * @param courseNames Vector of course names (optional)
     * @param teacherNames Vector of teacher names (optional)
     * @param htmlPath Path for the output HTML
     * @param algorithm Algorithm name used
     * @return true if successful, false otherwise
     */
    static bool generateScheduleHTML(
        const std::vector<Activity>& schedule,
        const std::vector<std::string>& courseNames,
        const std::vector<std::string>& teacherNames,
        const std::string& htmlPath,
        const std::string& algorithm = "Dynamic Programming"
    );
    
    /**
     * @brief Generate HTML version of the schedule with department statistics
     * @param schedule Vector of scheduled activities  
     * @param courseNames Vector of course names (optional)
     * @param teacherNames Vector of teacher names (optional)
     * @param htmlPath Path for the output HTML
     * @param deptStats Department statistics
     * @param algorithm Algorithm name used
     * @return true if successful, false otherwise
     */
    static bool generateScheduleHTML(
        const std::vector<Activity>& schedule,
        const std::vector<std::string>& courseNames,
        const std::vector<std::string>& teacherNames,
        const std::string& htmlPath,
        const DepartmentStats& deptStats,
        const std::string& algorithm = "Dynamic Programming"
    );
    
    /**
     * @brief Open PDF in default browser/viewer
     * @param pdfPath Path to the PDF file
     * @return true if successful, false otherwise
     */
    static bool openInBrowser(const std::string& pdfPath);

    /**
     * @brief Convert HTML file to PDF using headless Chrome
     * @param htmlPath Path to the HTML file
     * @param pdfPath Path for the output PDF file
     * @return true if successful, false otherwise
     */
    static bool convertHTMLtoPDF(const std::string& htmlPath, const std::string& pdfPath);

    /**
     * @brief Convert AcademicStats to DepartmentStats for PDF generation
     * @param academicStats Academic statistics from database
     * @param dbManager Database manager for additional room type counts
     * @return DepartmentStats structure for PDF generation
     */
    static DepartmentStats convertAcademicStatsToDepartmentStats(
        const DatabaseManager::AcademicStats& academicStats,
        DatabaseManager* dbManager
    );

private:
    /**
     * @brief Convert time integer to readable format
     */
    static std::string formatTime(int hour);
    
    /**
     * @brief Generate CSS for the schedule table
     */
    static std::string generateCSS();
    
    /**
     * @brief Get course name by ID or generate default
     */
    static std::string getCourseName(int id, const std::vector<std::string>& courseNames);
    
    /**
     * @brief Get teacher name by ID or generate default
     */
    static std::string getTeacherName(int id, const std::vector<std::string>& teacherNames);
};

#endif // PDF_GENERATOR_H
