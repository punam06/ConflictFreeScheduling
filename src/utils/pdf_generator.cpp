#include "pdf_generator.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstdlib>

bool PDFGenerator::generateSchedulePDF(
    const std::vector<Activity>& schedule,
    const std::vector<std::string>& courseNames,
    const std::vector<std::string>& teacherNames,
    const std::string& outputPath,
    const std::string& algorithm) {
    
    // First generate HTML
    std::string htmlPath = outputPath + ".html";
    std::vector<std::string> emptyTeacherNames; // Empty teacher names for backward compatibility
    if (!generateScheduleHTML(schedule, courseNames, teacherNames, htmlPath, algorithm)) {
        return false;
    }
    
    std::cout << "Generated HTML schedule: " << htmlPath << std::endl;
    
    // Try automatic PDF conversion first
    std::string pdfPath = outputPath + ".pdf";
    if (convertHTMLtoPDF(htmlPath, pdfPath)) {
        // Automatic conversion succeeded, open PDF
        return openInBrowser(pdfPath);
    } else {
        // Fallback to browser-based conversion
        std::cout << "Opening HTML in browser for manual PDF conversion..." << std::endl;
        std::cout << "💡 In browser: Press Cmd+P → Save as PDF" << std::endl;
        return openInBrowser(htmlPath);
    }
}

bool PDFGenerator::generateSchedulePDF(
    const std::vector<Activity>& schedule,
    const std::vector<std::string>& courseNames,
    const std::vector<std::string>& teacherNames,
    const std::string& outputPath,
    const DepartmentStats& deptStats,
    const std::string& algorithm) {
    
    // First generate HTML with department statistics
    std::string htmlPath = outputPath + ".html";
    std::vector<std::string> emptyTeacherNames; // Empty teacher names for backward compatibility
    if (!generateScheduleHTML(schedule, courseNames, teacherNames, htmlPath, deptStats, algorithm)) {
        return false;
    }
    
    std::cout << "Generated HTML schedule: " << htmlPath << std::endl;
    
    // Try automatic PDF conversion first
    std::string pdfPath = outputPath + ".pdf";
    if (convertHTMLtoPDF(htmlPath, pdfPath)) {
        // Automatic conversion succeeded, open PDF
        return openInBrowser(pdfPath);
    } else {
        // Fallback to browser-based conversion
        std::cout << "Opening HTML in browser for manual PDF conversion..." << std::endl;
        std::cout << "💡 In browser: Press Cmd+P → Save as PDF" << std::endl;
        return openInBrowser(htmlPath);
    }
}

bool PDFGenerator::generateScheduleHTML(
    const std::vector<Activity>& schedule,
    const std::vector<std::string>& courseNames,
    const std::vector<std::string>& teacherNames,
    const std::string& htmlPath,
    const std::string& algorithm) {
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot create HTML file " << htmlPath << std::endl;
        return false;
    }
    
    // Calculate statistics
    double totalWeight = 0;
    for (const auto& activity : schedule) {
        totalWeight += activity.weight;
    }
    
    // Generate HTML content
    file << "<!DOCTYPE html>\n";
    file << "<html lang=\"en\">\n";
    file << "<head>\n";
    file << "    <meta charset=\"UTF-8\">\n";
    file << "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
    file << "    <title>Conflict-Free Class Schedule - " << algorithm << "</title>\n";
    file << "    <style>\n" << generateCSS() << "</style>\n";
    file << "</head>\n";
    file << "<body>\n";
    
    // Header
    file << "    <div class=\"header\">\n";
    file << "        <h1>🎓 Bangladesh University of Professionals</h1>\n";
    file << "        <h2>Computer Science & Engineering Department</h2>\n";
    file << "        <h3>Conflict-Free Class Schedule</h3>\n";
    file << "        <p class=\"algorithm\">Generated using: <strong>" << algorithm << " Algorithm</strong></p>\n";
    file << "        <div class=\"department-info\">\n";
    file << "            <p><strong>Department Overview:</strong></p>\n";
    file << "            <p>• Batches: BCSE22-25 (4 batches)</p>\n";
    file << "            <p>• Internal Faculty: 6 members</p>\n";
    file << "            <p>• Sections: 8 (2 per batch)</p>\n";
    file << "            <p>• Rooms: 5 (3 theory + 2 lab)</p>\n";
    file << "        </div>\n";
    file << "    </div>\n\n";
    
    // Statistics
    file << "    <div class=\"stats\">\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << schedule.size() << "</span>\n";
    file << "            <span class=\"stat-label\">Courses Scheduled</span>\n";
    file << "        </div>\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << teacherNames.size() << "</span>\n";
    file << "            <span class=\"stat-label\">Total Teachers</span>\n";
    file << "        </div>\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">0</span>\n";
    file << "            <span class=\"stat-label\">Conflicts</span>\n";
    file << "        </div>\n";
    file << "    </div>\n\n";
    
    // Schedule table
    file << "    <div class=\"schedule-container\">\n";
    file << "        <table class=\"schedule-table\">\n";
    file << "            <thead>\n";
    file << "                <tr>\n";
    file << "                    <th>Course ID</th>\n";
    file << "                    <th>Course Name</th>\n";
    file << "                    <th>Teacher</th>\n";
    file << "                    <th>Start Time</th>\n";
    file << "                    <th>End Time</th>\n";
    file << "                    <th>Duration</th>\n";
    file << "                    <th>Status</th>\n";
    file << "                </tr>\n";
    file << "            </thead>\n";
    file << "            <tbody>\n";
    
    // Sort schedule by start time for better display
    std::vector<Activity> sortedSchedule = schedule;
    std::sort(sortedSchedule.begin(), sortedSchedule.end(),
              [](const Activity& a, const Activity& b) {
                  return a.start < b.start;
              });
    
    for (const auto& activity : sortedSchedule) {
        file << "                <tr>\n";
        file << "                    <td>" << activity.id << "</td>\n";
        file << "                    <td>" << getCourseName(activity.id, courseNames) << "</td>\n";
        file << "                    <td>" << getTeacherName(activity.id, teacherNames) << "</td>\n";
        file << "                    <td>" << formatTime(activity.start) << "</td>\n";
        file << "                    <td>" << formatTime(activity.end) << "</td>\n";
        file << "                    <td>" << (activity.end - activity.start) << "h</td>\n";
        file << "                    <td><span class=\"status-scheduled\">✓ Scheduled</span></td>\n";
        file << "                </tr>\n";
    }
    
    file << "            </tbody>\n";
    file << "        </table>\n";
    file << "    </div>\n\n";
    
    // Timeline visualization
    file << "    <div class=\"timeline-container\">\n";
    file << "        <h3>📅 Daily Timeline</h3>\n";
    file << "        <div class=\"timeline\">\n";
    
    // Generate timeline for 8 AM to 8 PM
    for (int hour = 8; hour <= 20; hour++) {
        file << "            <div class=\"time-slot\">\n";
        file << "                <div class=\"time-label\">" << formatTime(hour) << "</div>\n";
        file << "                <div class=\"time-content\">\n";
        
        // Check if any course is scheduled at this time
        for (const auto& activity : sortedSchedule) {
            if (hour >= activity.start && hour < activity.end) {
                file << "                    <div class=\"course-block\">\n";
                file << "                        <strong>" << getCourseName(activity.id, courseNames) << "</strong><br>\n";
                file << "                        " << getTeacherName(activity.id, teacherNames) << "\n";
                file << "                    </div>\n";
            }
        }
        
        file << "                </div>\n";
        file << "            </div>\n";
    }
    
    file << "        </div>\n";
    file << "    </div>\n\n";
    
    // Footer
    file << "    <div class=\"footer\">\n";
    file << "        <p>Generated on: " << __DATE__ << " at " << __TIME__ << "</p>\n";
    file << "        <p>Conflict-Free Scheduling System v1.0</p>\n";
    file << "        <p><em>Print this page as PDF using your browser (Ctrl+P → Save as PDF)</em></p>\n";
    file << "    </div>\n";
    
    file << "</body>\n";
    file << "</html>\n";
    
    file.close();
    return true;
}

bool PDFGenerator::generateScheduleHTML(
    const std::vector<Activity>& schedule,
    const std::vector<std::string>& courseNames,
    const std::vector<std::string>& teacherNames,
    const std::string& htmlPath,
    const DepartmentStats& deptStats,
    const std::string& algorithm) {
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot create HTML file " << htmlPath << std::endl;
        return false;
    }
    
    // Calculate total weight (students)
    double totalWeight = 0;
    for (const auto& activity : schedule) {
        totalWeight += activity.weight;
    }
    
    // Generate HTML content
    file << "<!DOCTYPE html>\n";
    file << "<html lang=\"en\">\n";
    file << "<head>\n";
    file << "    <meta charset=\"UTF-8\">\n";
    file << "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
    file << "    <title>Conflict-Free Class Schedule - " << algorithm << "</title>\n";
    file << "    <style>\n" << generateCSS() << "</style>\n";
    file << "</head>\n";
    file << "<body>\n";
    
    // Header with dynamic department information
    file << "    <div class=\"header\">\n";
    file << "        <h1>🎓 Bangladesh University of Professionals</h1>\n";
    file << "        <h2>Computer Science & Engineering Department</h2>\n";
    file << "        <h3>Conflict-Free Class Schedule</h3>\n";
    file << "        <p class=\"algorithm\">Generated using: <strong>" << algorithm << " Algorithm</strong></p>\n";
    file << "        <div class=\"department-info\">\n";
    file << "            <p><strong>Department Overview:</strong></p>\n";
    file << "            <p>• Batches: BCSE22-25 (" << deptStats.total_batches << " batches)</p>\n";
    file << "            <p>• Internal Faculty: " << deptStats.total_teachers << " members</p>\n";
    file << "            <p>• Sections: " << deptStats.total_sections << " (" << (deptStats.total_sections / deptStats.total_batches) << " per batch)</p>\n";
    file << "            <p>• Rooms: " << deptStats.total_classrooms << " (" << deptStats.theory_rooms << " theory + " << deptStats.lab_rooms << " lab)</p>\n";
    file << "        </div>\n";
    file << "    </div>\n\n";
    
    // Statistics
    file << "    <div class=\"stats\">\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << schedule.size() << "</span>\n";
    file << "            <span class=\"stat-label\">Courses Scheduled</span>\n";
    file << "        </div>\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << teacherNames.size() << "</span>\n";
    file << "            <span class=\"stat-label\">Total Teachers</span>\n";
    file << "        </div>\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">0</span>\n";
    file << "            <span class=\"stat-label\">Conflicts</span>\n";
    file << "        </div>\n";
    file << "    </div>\n\n";
    
    // Schedule table
    file << "    <div class=\"schedule-container\">\n";
    file << "        <table class=\"schedule-table\">\n";
    file << "            <thead>\n";
    file << "                <tr>\n";
    file << "                    <th>Course ID</th>\n";
    file << "                    <th>Course Name</th>\n";
    file << "                    <th>Teacher</th>\n";
    file << "                    <th>Start Time</th>\n";
    file << "                    <th>End Time</th>\n";
    file << "                    <th>Duration</th>\n";
    file << "                    <th>Status</th>\n";
    file << "                </tr>\n";
    file << "            </thead>\n";
    file << "            <tbody>\n";
    
    // Sort schedule by start time for better display
    std::vector<Activity> sortedSchedule = schedule;
    std::sort(sortedSchedule.begin(), sortedSchedule.end(),
              [](const Activity& a, const Activity& b) {
                  return a.start < b.start;
              });
    
    for (const auto& activity : sortedSchedule) {
        file << "                <tr>\n";
        file << "                    <td>" << activity.id << "</td>\n";
        file << "                    <td>" << getCourseName(activity.id, courseNames) << "</td>\n";
        file << "                    <td>" << getTeacherName(activity.id, teacherNames) << "</td>\n";
        file << "                    <td>" << formatTime(activity.start) << "</td>\n";
        file << "                    <td>" << formatTime(activity.end) << "</td>\n";
        file << "                    <td>" << (activity.end - activity.start) << "h</td>\n";
        file << "                    <td><span class=\"status-scheduled\">✓ Scheduled</span></td>\n";
        file << "                </tr>\n";
    }
    
    file << "            </tbody>\n";
    file << "        </table>\n";
    file << "    </div>\n\n";
    
    // Footer
    file << "    <div class=\"footer\">\n";
    file << "        <p>Generated on " << __DATE__ << " at " << __TIME__ << "</p>\n";
    file << "        <p><em>Print this page as PDF using your browser (Ctrl+P → Save as PDF)</em></p>\n";
    file << "    </div>\n";
    
    file << "</body>\n";
    file << "</html>\n";
    
    file.close();
    return true;
}

bool PDFGenerator::openInBrowser(const std::string& filePath) {
    std::string command;
    
#ifdef __APPLE__
    command = "open \"" + filePath + "\"";
#elif defined(_WIN32)
    command = "start \"\" \"" + filePath + "\"";
#else
    command = "xdg-open \"" + filePath + "\"";
#endif
    
    int result = std::system(command.c_str());
    return result == 0;
}

std::string PDFGenerator::formatTime(int hour) {
    if (hour == 0) return "12:00 AM";
    if (hour < 12) return std::to_string(hour) + ":00 AM";
    if (hour == 12) return "12:00 PM";
    return std::to_string(hour - 12) + ":00 PM";
}

std::string PDFGenerator::getCourseName(int id, const std::vector<std::string>& courseNames) {
    if (id > 0 && id <= static_cast<int>(courseNames.size())) {
        return courseNames[id - 1];
    }
    
    // Default course names
    std::vector<std::string> defaultNames = {
        "Data Structures", "Algorithms", "Database Systems", 
        "Computer Networks", "Software Engineering", 
        "Operating Systems", "Machine Learning", "Computer Graphics",
        "Web Programming", "Mobile App Development"
    };
    
    if (id > 0 && id <= static_cast<int>(defaultNames.size())) {
        return defaultNames[id - 1];
    }
    
    return "Course " + std::to_string(id);
}

std::string PDFGenerator::getTeacherName(int id, const std::vector<std::string>& teacherNames) {
    if (id > 0 && id <= static_cast<int>(teacherNames.size())) {
        return teacherNames[id - 1];
    }
    
    // Default teacher names
    std::vector<std::string> defaultNames = {
        "Dr. Ahmed Rahman", "Prof. Sarah Khan", "Dr. Mohammad Ali",
        "Ms. Fatima Sheikh", "Dr. Hassan Ahmed", "Prof. Nadia Alam",
        "Dr. Tariq Mahmud", "Prof. Ayesha Siddiqui", "Dr. Omar Farooq",
        "Ms. Zara Ahmed"
    };
    
    if (id > 0 && id <= static_cast<int>(defaultNames.size())) {
        return defaultNames[id - 1];
    }
    
    return "Teacher " + std::to_string(id);
}

std::string PDFGenerator::generateCSS() {
    return R"(
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header h2 {
            font-size: 1.5rem;
            color: #4a5568;
            margin-bottom: 4px;
        }

        .header h3 {
            font-size: 1.25rem;
            color: #718096;
            margin-bottom: 16px;
        }

        .department-info {
            margin-top: 24px;
            padding: 16px 24px;
            background: rgba(247, 250, 252, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(226, 232, 240, 0.6);
            display: inline-block;
            text-align: left;
        }

        .department-info p {
            color: #4a5568;
            font-size: 0.95rem;
            line-height: 1.8;
        }

        .department-info p strong {
            color: #2d3748;
            font-weight: 600;
        }
        
        .algorithm {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            display: inline-block;
            font-weight: 600;
            box-shadow: 0 8px 20px rgba(66, 153, 225, 0.3);
            transform: translateY(0);
            transition: all 0.3s ease;
        }

        .algorithm:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(66, 153, 225, 0.4);
        }
        
        /* Enhanced Statistics Dashboard */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
            padding: 0 10px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            padding: 30px 25px;
            border-radius: 18px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.06), 0 5px 15px rgba(0,0,0,0.03);
            border: 1px solid rgba(255,255,255,0.9);
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .stat-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .stat-box:hover::before {
            transform: scaleX(1);
        }

        .stat-box:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 60px rgba(0,0,0,0.12), 0 10px 25px rgba(0,0,0,0.06);
        }
        
        .stat-number {
            display: block;
            font-size: 3.2em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            line-height: 1;
        }
        
        .stat-label {
            color: #4a5568;
            font-size: 1.1em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Premium Schedule Table */
        .schedule-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.08), 0 5px 20px rgba(0,0,0,0.04);
            border: 1px solid rgba(255,255,255,0.8);
            margin-bottom: 40px;
            overflow: hidden;
        }
        
        .schedule-table {
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
        
        .schedule-table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .schedule-table th {
            padding: 20px 15px;
            text-align: left;
            font-weight: 600;
            color: white;
            font-size: 1em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: none;
        }
        
        .schedule-table td {
            padding: 18px 15px;
            border-bottom: 1px solid #e2e8f0;
            color: #2d3748;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .schedule-table tbody tr {
            transition: all 0.3s ease;
        }
        
        .schedule-table tbody tr:hover {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            transform: scale(1.01);
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .schedule-table tbody tr:last-child td {
            border-bottom: none;
        }
        
        .schedule-table tbody tr:nth-child(even) {
            background: #f8fafc;
        }
        
        /* Enhanced Status Badges */
        .status-scheduled {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
            display: inline-block;
        }
        
        /* Modern Timeline */
        .timeline-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.08), 0 5px 20px rgba(0,0,0,0.04);
            border: 1px solid rgba(255,255,255,0.8);
            margin-bottom: 40px;
        }
        
        .timeline-container h3 {
            color: #2d3748;
            margin-bottom: 30px;
            text-align: center;
            font-size: 1.8em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .timeline {
            display: grid;
            gap: 15px;
        }
        
        .time-slot {
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 20px;
            padding: 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }

        .time-slot:hover {
            transform: translateX(5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }
        
        .time-label {
            font-weight: 700;
            color: #4a5568;
            text-align: right;
            padding-top: 8px;
            font-size: 1em;
        }
        
        .course-block {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
            padding: 12px 18px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
            transition: all 0.2s ease;
        }

        .course-block:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(66, 153, 225, 0.4);
        }
        
        /* Enhanced Footer */
        .footer {
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.06), 0 5px 15px rgba(0,0,0,0.03);
            border: 1px solid rgba(255,255,255,0.9);
            color: #718096;
            font-weight: 500;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header {
                padding: 24px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .header h2 {
                font-size: 1.25rem;
            }
            
            .department-info {
                padding: 12px 16px;
                font-size: 0.9rem;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 1.75rem;
            }
            
            .department-info {
                padding: 10px 14px;
                font-size: 0.85rem;
            }
        }
        
        /* Print Optimization */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .header {
                background: white !important;
                box-shadow: none !important;
                border: none !important;
                break-inside: avoid;
            }
            
            .department-info {
                background: white !important;
                border: 1px solid #edf2f7 !important;
                break-inside: avoid;
            }
            
            .department-info p {
                color: #000 !important;
            }
        }
    )";
}

bool PDFGenerator::convertHTMLtoPDF(const std::string& htmlPath, const std::string& pdfPath) {
    // Check if HTML file exists
    std::ifstream htmlFile(htmlPath);
    if (!htmlFile.good()) {
        std::cerr << "Error: HTML file not found: " << htmlPath << std::endl;
        return false;
    }
    htmlFile.close();

    // Try different Chrome/Chromium paths
    std::vector<std::string> chromePaths = {
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", // macOS
        "google-chrome",                                                // Linux
        "chromium",                                                     // Linux alternative
        "chrome",                                                       // Windows
        "/usr/bin/google-chrome",                                      // Linux system install
        "/usr/bin/chromium"                                            // Linux system install
    };

    for (const auto& chromePath : chromePaths) {
        // Check if Chrome/Chromium is available
        std::string checkCmd = "command -v \"" + chromePath + "\" >/dev/null 2>&1";
        if (system(checkCmd.c_str()) == 0) {
            // Convert relative path to absolute path
            char* realHtmlPath = realpath(htmlPath.c_str(), nullptr);
            if (!realHtmlPath) {
                std::cerr << "Error: Cannot resolve absolute path for: " << htmlPath << std::endl;
                continue;
            }

            // Build Chrome command
            std::string cmd = "\"" + chromePath + "\" --headless --disable-gpu --print-to-pdf=\"" + 
                            pdfPath + "\" \"file://" + std::string(realHtmlPath) + "\" 2>/dev/null";

            std::cout << "Converting HTML to PDF using: " << chromePath << std::endl;
            
            int result = system(cmd.c_str());
            free(realHtmlPath);

            if (result == 0) {
                // Check if PDF was actually created
                std::ifstream pdfFile(pdfPath);
                if (pdfFile.good()) {
                    pdfFile.close();
                    std::cout << "✅ PDF generated successfully: " << pdfPath << std::endl;
                    
                    // Get file size
                    std::ifstream::pos_type size = std::ifstream(pdfPath, std::ios::ate | std::ios::binary).tellg();
                    std::cout << "📊 File size: " << (size / 1024) << " KB" << std::endl;
                    
                    return true;
                } else {
                    std::cerr << "❌ PDF file was not created" << std::endl;
                }
            } else {
                std::cerr << "❌ Chrome command failed with exit code: " << result << std::endl;
            }
        }
    }

    std::cerr << "❌ Chrome/Chromium not found!" << std::endl;
    std::cerr << "💡 Alternative: Open " << htmlPath << " in browser and print to PDF (Cmd+P)" << std::endl;
    return false;
}

DepartmentStats PDFGenerator::convertAcademicStatsToDepartmentStats(
    const DatabaseManager::AcademicStats& academicStats,
    DatabaseManager* dbManager) {
    
    DepartmentStats deptStats;
    
    // Direct mapping from AcademicStats
    deptStats.total_batches = academicStats.total_batches;
    deptStats.total_teachers = academicStats.total_teachers;
    deptStats.total_sections = academicStats.total_sections;
    deptStats.total_classrooms = academicStats.total_classrooms;
    
    // Get room type counts from database
    if (dbManager) {
        auto roomCounts = dbManager->getRoomTypeCounts();
        deptStats.theory_rooms = roomCounts.first;
        deptStats.lab_rooms = roomCounts.second;
    } else {
        // Fallback values if database manager is not available
        deptStats.theory_rooms = 3;
        deptStats.lab_rooms = 2;
    }
    
    return deptStats;
}
