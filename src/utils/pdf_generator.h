#ifndef PDF_GENERATOR_H
#define PDF_GENERATOR_H

#include "../scheduler.h"
#include <vector>
#include <string>

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
        const std::string& outputPath,
        const std::string& algorithm = "Dynamic Programming"
    );
    
    /**
     * @brief Generate HTML version of the schedule
     * @param schedule Vector of scheduled activities  
     * @param courseNames Vector of course names (optional)
     * @param htmlPath Path for the output HTML
     * @param algorithm Algorithm name used
     * @return true if successful, false otherwise
     */
    static bool generateScheduleHTML(
        const std::vector<Activity>& schedule,
        const std::vector<std::string>& courseNames,
        const std::string& htmlPath,
        const std::string& algorithm = "Dynamic Programming"
    );
    
    /**
     * @brief Open PDF in default browser/viewer
     * @param pdfPath Path to the PDF file
     * @return true if successful, false otherwise
     */
    static bool openInBrowser(const std::string& pdfPath);

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
};

#endif // PDF_GENERATOR_H
