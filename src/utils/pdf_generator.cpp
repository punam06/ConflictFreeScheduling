#include "pdf_generator.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstdlib>

bool PDFGenerator::generateSchedulePDF(
    const std::vector<Activity>& schedule,
    const std::vector<std::string>& courseNames,
    const std::string& outputPath,
    const std::string& algorithm) {
    
    // First generate HTML
    std::string htmlPath = outputPath + ".html";
    if (!generateScheduleHTML(schedule, courseNames, htmlPath, algorithm)) {
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
    file << "    </div>\n\n";
    
    // Statistics
    file << "    <div class=\"stats\">\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << schedule.size() << "</span>\n";
    file << "            <span class=\"stat-label\">Courses Scheduled</span>\n";
    file << "        </div>\n";
    file << "        <div class=\"stat-box\">\n";
    file << "            <span class=\"stat-number\">" << static_cast<int>(totalWeight) << "</span>\n";
    file << "            <span class=\"stat-label\">Total Students</span>\n";
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
    file << "                    <th>Start Time</th>\n";
    file << "                    <th>End Time</th>\n";
    file << "                    <th>Duration</th>\n";
    file << "                    <th>Students</th>\n";
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
        file << "                    <td>" << formatTime(activity.start) << "</td>\n";
        file << "                    <td>" << formatTime(activity.end) << "</td>\n";
        file << "                    <td>" << (activity.end - activity.start) << "h</td>\n";
        file << "                    <td>" << static_cast<int>(activity.weight) << "</td>\n";
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
                file << "                        " << static_cast<int>(activity.weight) << " students\n";
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

std::string PDFGenerator::generateCSS() {
    return R"(
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header h2 {
            color: #34495e;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        
        .header h3 {
            color: #e74c3c;
            font-size: 1.3em;
            margin-bottom: 10px;
        }
        
        .algorithm {
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 10px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .stat-box {
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            min-width: 150px;
        }
        
        .stat-number {
            display: block;
            font-size: 2.5em;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .schedule-container {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .schedule-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .schedule-table th {
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9em;
        }
        
        .schedule-table td {
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .schedule-table tr:hover {
            background: #f8f9fa;
        }
        
        .status-scheduled {
            background: #27ae60;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .timeline-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .timeline-container h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .timeline {
            display: grid;
            gap: 10px;
        }
        
        .time-slot {
            display: grid;
            grid-template-columns: 100px 1fr;
            gap: 15px;
            padding: 10px;
            border-radius: 8px;
            background: #f8f9fa;
        }
        
        .time-label {
            font-weight: bold;
            color: #34495e;
            text-align: right;
            padding-top: 5px;
        }
        
        .course-block {
            background: #3498db;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 5px;
        }
        
        .footer {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            color: #7f8c8d;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .header, .schedule-container, .timeline-container, .footer {
                box-shadow: none;
                break-inside: avoid;
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
