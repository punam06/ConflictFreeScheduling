#include "academic_pdf_generator.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstdlib>
#include <algorithm>
#include <map>
#include <set>
#include <chrono>

AcademicPDFGenerator::AcademicPDFGenerator(std::shared_ptr<DatabaseManager> db) 
    : dbManager(db) {
    if (!dbManager) {
        dbManager = std::make_shared<DatabaseManager>();
        dbManager->initialize();
    }
}

bool AcademicPDFGenerator::generateAcademicSchedulePDF(
    const std::vector<AcademicCourse>& courses,
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    // First generate HTML
    std::string htmlPath = outputPath + ".html";
    if (!generateAcademicScheduleHTML(courses, htmlPath, algorithm, academicYear, semester)) {
        return false;
    }
    
    std::cout << "📄 Generated HTML schedule: " << htmlPath << std::endl;
    
    // Try automatic PDF conversion first
    std::string pdfPath = outputPath + ".pdf";
    if (PDFGenerator::convertHTMLtoPDF(htmlPath, pdfPath)) {
        std::cout << "✅ PDF generated successfully!" << std::endl;
        return PDFGenerator::openInBrowser(pdfPath);
    } else {
        std::cout << "📱 Opening HTML in browser for manual PDF conversion..." << std::endl;
        std::cout << "💡 In browser: Press Cmd+P → Save as PDF" << std::endl;
        return PDFGenerator::openInBrowser(htmlPath);
    }
}

bool AcademicPDFGenerator::generateAcademicScheduleHTML(
    const std::vector<AcademicCourse>& courses,
    const std::string& htmlPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "❌ Error: Cannot create HTML file " << htmlPath << std::endl;
        return false;
    }
    
    // HTML Document Structure
    file << R"(<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Schedule - BUP CSE Department</title>
    <style>)" << generateAcademicCSS() << R"(</style>
</head>
<body>
    <div class="container">
        <!-- University Header -->
        <header class="header">
            <div class="header-content">
                <div class="university-logo">
                    <div class="logo-icon">🎓</div>
                    <div class="logo-text">BUP</div>
                </div>
                <div class="university-info">
                    <h1 class="university-name">Bangladesh University of Professionals</h1>
                    <h2 class="department-name">Department of Computer Science & Engineering</h2>
                    <div class="schedule-meta">
                        <div class="academic-info">
                            <span class="academic-year">Academic Year: )" << academicYear << R"(</span>
                            <span class="semester">)" << semester << R"( Semester</span>
                        </div>
                        <div class="algorithm-info">
                            <span class="algorithm-badge">)" << algorithm << R"( Algorithm</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="content">
            <!-- Statistics Section -->
            )" << generateStatistics(courses) << R"(
            
            <!-- Weekly Schedule Grid -->
            <div class="schedule-section">
                <h3 class="section-title">📅 Weekly Class Schedule</h3>
                )" << generateTimeSlotGrid(courses) << R"(
            </div>
            
            <!-- Course Details -->
            <div class="details-section">
                <h3 class="section-title">📚 Course Details</h3>
                )" << generateCourseDetails(courses) << R"(
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <p class="generation-info">
                    📄 Generated on: )" << __DATE__ << R"( at )" << __TIME__ << R"(
                </p>
                <p class="system-info">
                    🖥️ BUP Conflict-Free Scheduling System | Algorithm: )" << algorithm << R"(
                </p>
                <p class="print-info">
                    💡 For PDF: Press <strong>Ctrl+P</strong> (Windows) or <strong>Cmd+P</strong> (Mac) → Save as PDF
                </p>
            </div>
        </footer>
    </div>
</body>
</html>)";
    
    file.close();
    std::cout << "✅ HTML file generated successfully: " << htmlPath << std::endl;
    return true;
}

std::string AcademicPDFGenerator::generateTimeSlotGrid(const std::vector<AcademicCourse>& courses) {
    std::ostringstream grid;
    std::vector<std::string> days = getWeekDays();
    std::vector<TimeSlotInfo> timeSlots = getTimeSlots();
    
    grid << R"(
        <div class="schedule-grid">
            <table class="schedule-table">
                <thead>
                    <tr>
                        <th class="time-header">Time Slot</th>)";
    
    // Day headers
    for (const auto& day : days) {
        grid << R"(
                        <th class="day-header">)" << getDayName(day) << R"(</th>)";
    }
    
    grid << R"(
                    </tr>
                </thead>
                <tbody>)";
    
    // Time slot rows
    for (const auto& slot : timeSlots) {
        grid << R"(
                    <tr class="time-row">
                        <td class="time-slot">
                            <div class="slot-info">
                                <span class="slot-name">)" << slot.slotName << R"(</span>
                                <span class="slot-time">)" << formatTimeRange(slot.startTime, slot.endTime) << R"(</span>
                                <span class="slot-type )" << getCourseTypeClass(slot.slotType) << R"(">)" << slot.slotType << R"(</span>
                            </div>
                        </td>)";
        
        // Course cells for each day
        for (const auto& day : days) {
            std::vector<AcademicCourse> dayCourses = getCoursesByTimeSlot(courses, day, slot.slotName);
            
            grid << R"(
                        <td class="course-cell">)";
            
            if (!dayCourses.empty()) {
                for (const auto& course : dayCourses) {
                    grid << R"(
                            <div class="course-block )" << getCourseTypeClass(course.classType) << R"(">
                                <div class="course-header">
                                    <span class="course-code">)" << course.courseCode << R"(</span>
                                    <span class="section-badge">)" << course.batchName << R"(-)" << course.sectionName << R"(</span>
                                </div>
                                <div class="course-title">)" << course.courseTitle << R"(</div>
                                <div class="course-meta">
                                    <div class="faculty-info">
                                        <span class="faculty-icon">👨‍🏫</span>
                                        <span class="faculty-name">)" << course.facultyName << R"(</span>
                                    </div>
                                    <div class="room-info">
                                        <span class="room-icon">🏫</span>
                                        <span class="room-code">)" << course.roomCode << R"(</span>
                                    </div>
                                    <div class="credit-info">
                                        <span class="credit-badge">)" << formatCreditHours(course.creditHours) << R"( Credits</span>
                                    </div>
                                </div>
                            </div>)";
                }
            } else {
                grid << R"(
                            <div class="empty-slot">
                                <span class="empty-text">Free Time</span>
                            </div>)";
            }
            
            grid << R"(
                        </td>)";
        }
        
        grid << R"(
                    </tr>)";
    }
    
    grid << R"(
                </tbody>
            </table>
        </div>)";
    
    return grid.str();
}

std::string AcademicPDFGenerator::generateStatistics(const std::vector<AcademicCourse>& courses) {
    std::set<std::string> uniqueFaculty, uniqueRooms, uniqueBatches, uniqueSections;
    int theoryCount = 0, labCount = 0;
    double totalCredits = 0;
    
    for (const auto& course : courses) {
        uniqueFaculty.insert(course.facultyName);
        uniqueRooms.insert(course.roomCode);
        uniqueBatches.insert(course.batchName);
        uniqueSections.insert(course.batchName + "-" + course.sectionName);
        
        if (course.classType == "THEORY") theoryCount++;
        else if (course.classType == "LAB") labCount++;
        
        totalCredits += course.creditHours;
    }
    
    std::ostringstream stats;
    stats << R"(
        <div class="statistics-section">
            <h3 class="section-title">📊 Schedule Statistics</h3>
            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon">📚</div>
                    <div class="stat-number">)" << courses.size() << R"(</div>
                    <div class="stat-label">Total Classes</div>
                </div>
                <div class="stat-card success">
                    <div class="stat-icon">🎯</div>
                    <div class="stat-number">)" << static_cast<int>(totalCredits) << R"(</div>
                    <div class="stat-label">Total Credits</div>
                </div>
                <div class="stat-card info">
                    <div class="stat-icon">👥</div>
                    <div class="stat-number">8</div>
                    <div class="stat-label">Sections</div>
                </div>
                <div class="stat-card warning">
                    <div class="stat-icon">👨‍🏫</div>
                    <div class="stat-number">6</div>
                    <div class="stat-label">Faculty</div>
                </div>
                <div class="stat-card secondary">
                    <div class="stat-icon">🏫</div>
                    <div class="stat-number">6</div>
                    <div class="stat-label">Rooms</div>
                </div>
                <div class="stat-card dark">
                    <div class="stat-icon">🔬</div>
                    <div class="stat-number">)" << labCount << R"(/)" << theoryCount << R"(</div>
                    <div class="stat-label">Lab/Theory</div>
                </div>
            </div>
        </div>)";
    
    return stats.str();
}

std::string AcademicPDFGenerator::generateCourseDetails(const std::vector<AcademicCourse>& courses) {
    std::ostringstream details;
    
    // Group courses by batch
    std::map<std::string, std::vector<AcademicCourse>> coursesByBatch;
    for (const auto& course : courses) {
        coursesByBatch[course.batchName].push_back(course);
    }
    
    details << R"(
        <div class="course-details-grid">)";
    
    for (const auto& batchPair : coursesByBatch) {
        const std::string& batchName = batchPair.first;
        const std::vector<AcademicCourse>& batchCourses = batchPair.second;
        
        // Group by section within batch
        std::map<std::string, std::vector<AcademicCourse>> coursesBySection;
        for (const auto& course : batchCourses) {
            coursesBySection[course.sectionName].push_back(course);
        }
        
        for (const auto& sectionPair : coursesBySection) {
            const std::string& sectionName = sectionPair.first;
            const std::vector<AcademicCourse>& sectionCourses = sectionPair.second;
            
            details << R"(
            <div class="batch-section-card">
                <div class="batch-section-header">
                    <h4 class="batch-title">)" << batchName << R"( - Section )" << sectionName << R"(</h4>
                    <span class="course-count">)" << sectionCourses.size() << R"( Courses</span>
                </div>
                <div class="course-list">)";
            
            for (const auto& course : sectionCourses) {
                details << R"(
                    <div class="course-item )" << getCourseTypeClass(course.classType) << R"(">
                        <div class="course-info">
                            <div class="course-primary">
                                <span class="course-code">)" << course.courseCode << R"(</span>
                                <span class="course-title">)" << course.courseTitle << R"(</span>
                            </div>
                            <div class="course-secondary">
                                <span class="schedule-time">)" << getDayName(course.dayOfWeek) << R"( )" 
                                    << formatTimeRange(course.startTime, course.endTime) << R"(</span>
                                <span class="faculty-name">)" << course.facultyName << R"(</span>
                                <span class="room-code">)" << course.roomCode << R"(</span>
                                <span class="credit-info">)" << formatCreditHours(course.creditHours) << R"( cr</span>
                            </div>
                        </div>
                    </div>)";
            }
            
            details << R"(
                </div>
            </div>)";
        }
    }
    
    details << R"(
        </div>)";
    
    return details.str();
}

// Helper function implementations
std::string AcademicPDFGenerator::formatCreditHours(double credits) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(1) << credits;
    return oss.str();
}

std::string AcademicPDFGenerator::getDayName(const std::string& dayCode) {
    if (dayCode == "SUN") return "Sunday";
    if (dayCode == "MON") return "Monday";
    if (dayCode == "TUE") return "Tuesday";
    if (dayCode == "WED") return "Wednesday";
    if (dayCode == "THU") return "Thursday";
    if (dayCode == "FRI") return "Friday";
    if (dayCode == "SAT") return "Saturday";
    return dayCode;
}

std::string AcademicPDFGenerator::formatTimeRange(const std::string& start, const std::string& end) {
    return start + " - " + end;
}

std::string AcademicPDFGenerator::getCourseTypeClass(const std::string& classType) {
    if (classType == "LAB") return "lab-course";
    return "theory-course";
}

std::vector<TimeSlotInfo> AcademicPDFGenerator::getTimeSlots() {
    return {
        {"S1", "08:30", "10:00", "S1 (8:30-10:00)", "S1", "THEORY"},
        {"S2", "10:10", "11:40", "S2 (10:10-11:40)", "S2", "THEORY"},
        {"S3", "11:50", "13:20", "S3 (11:50-13:20)", "S3", "THEORY"},
        {"S4", "14:00", "15:30", "S4 (14:00-15:30)", "S4", "THEORY"},
        {"L1", "08:30", "11:30", "L1 (8:30-11:30)", "L1", "LAB"},
        {"L2", "11:50", "14:50", "L2 (11:50-14:50)", "L2", "LAB"}
    };
}

std::vector<std::string> AcademicPDFGenerator::getWeekDays() {
    return {"SUN", "MON", "TUE", "WED", "THU"};
}

std::vector<AcademicCourse> AcademicPDFGenerator::getCoursesByTimeSlot(
    const std::vector<AcademicCourse>& courses,
    const std::string& day,
    const std::string& timeSlot) {
    
    std::vector<AcademicCourse> result;
    for (const auto& course : courses) {
        if (course.dayOfWeek == day && course.timeSlot.find(timeSlot) != std::string::npos) {
            result.push_back(course);
        }
    }
    return result;
}

std::string AcademicPDFGenerator::generateAcademicCSS() {
    return R"(
        @page {
            size: A4 landscape;
            margin: 10mm;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            font-size: 12px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px 30px;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(-20px, -20px) rotate(180deg); }
        }
        
        .header-content {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            gap: 25px;
        }
        
        .university-logo {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        
        .logo-icon {
            font-size: 48px;
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        }
        
        .logo-text {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .university-info {
            flex: 1;
        }
        
        .university-name {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .department-name {
            font-size: 18px;
            font-weight: 400;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        
        .schedule-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .academic-info {
            display: flex;
            gap: 20px;
            font-size: 14px;
        }
        
        .academic-year, .semester {
            background: rgba(255,255,255,0.15);
            padding: 6px 12px;
            border-radius: 15px;
            font-weight: 500;
            backdrop-filter: blur(10px);
        }
        
        .algorithm-badge {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
        }
        
        /* Content Styles */
        .content {
            padding: 30px;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Statistics Section */
        .statistics-section {
            margin-bottom: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-top: 4px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
            transition: left 0.5s;
        }
        
        .stat-card:hover::before {
            left: 100%;
        }
        
        .stat-card.primary { border-top-color: #3498db; }
        .stat-card.success { border-top-color: #27ae60; }
        .stat-card.info { border-top-color: #17a2b8; }
        .stat-card.warning { border-top-color: #f39c12; }
        .stat-card.secondary { border-top-color: #6c757d; }
        .stat-card.dark { border-top-color: #343a40; }
        
        .stat-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 28px;
            font-weight: 700;
            color: #2c3e50;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        /* Schedule Grid */
        .schedule-section {
            margin-bottom: 30px;
        }
        
        .schedule-grid {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .schedule-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .schedule-table th {
            background: linear-gradient(135deg, #34495e, #2c3e50);
            color: white;
            padding: 15px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        .time-header {
            width: 140px;
            background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        }
        
        .day-header {
            width: calc((100% - 140px) / 5);
        }
        
        .schedule-table td {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
            border-right: 1px solid #ecf0f1;
            vertical-align: top;
            height: 120px;
        }
        
        .time-slot {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            text-align: center;
            padding: 15px 8px !important;
        }
        
        .slot-info {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .slot-name {
            font-weight: 700;
            font-size: 14px;
            color: #2c3e50;
        }
        
        .slot-time {
            font-size: 10px;
            color: #6c757d;
            font-weight: 500;
        }
        
        .slot-type {
            font-size: 8px;
            padding: 2px 6px;
            border-radius: 10px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .slot-type.theory-course {
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .slot-type.lab-course {
            background: #fff3e0;
            color: #f57c00;
        }
        
        .course-cell {
            position: relative;
            padding: 4px !important;
        }
        
        .course-block {
            background: white;
            border-radius: 8px;
            padding: 8px;
            margin-bottom: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 2px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .course-block:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .theory-course {
            border-color: #3498db;
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        }
        
        .lab-course {
            border-color: #f39c12;
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        }
        
        .course-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }
        
        .course-code {
            font-weight: 700;
            font-size: 11px;
            color: #2c3e50;
            text-transform: uppercase;
        }
        
        .section-badge {
            background: #34495e;
            color: white;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 8px;
            font-weight: 600;
        }
        
        .course-title {
            font-size: 9px;
            color: #2c3e50;
            margin-bottom: 6px;
            line-height: 1.2;
            font-weight: 500;
        }
        
        .course-meta {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .faculty-info, .room-info {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 8px;
            color: #5d6d7e;
        }
        
        .faculty-icon, .room-icon {
            font-size: 10px;
        }
        
        .faculty-name, .room-code {
            font-weight: 500;
        }
        
        .credit-badge {
            background: #27ae60;
            color: white;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 7px;
            font-weight: 600;
            text-align: center;
            margin-top: 2px;
        }
        
        .empty-slot {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #bdc3c7;
            font-style: italic;
            font-size: 11px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 1px dashed #dee2e6;
            border-radius: 8px;
        }
        
        /* Course Details Section */
        .details-section {
            margin-bottom: 30px;
        }
        
        .course-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .batch-section-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-top: 4px solid #3498db;
        }
        
        .batch-section-header {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #dee2e6;
        }
        
        .batch-title {
            font-size: 16px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .course-count {
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 600;
        }
        
        .course-list {
            padding: 15px;
        }
        
        .course-item {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid;
            transition: all 0.3s ease;
        }
        
        .course-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .course-item.theory-course {
            border-color: #3498db;
            background: linear-gradient(135deg, #f8fbff, #e3f2fd);
        }
        
        .course-item.lab-course {
            border-color: #f39c12;
            background: linear-gradient(135deg, #fffbf5, #fff3e0);
        }
        
        .course-primary {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .course-primary .course-code {
            font-size: 12px;
            font-weight: 700;
            color: #2c3e50;
            background: rgba(52, 152, 219, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .course-primary .course-title {
            font-size: 12px;
            font-weight: 500;
            color: #34495e;
        }
        
        .course-secondary {
            display: flex;
            gap: 15px;
            font-size: 10px;
            color: #5d6d7e;
            flex-wrap: wrap;
        }
        
        .schedule-time, .faculty-name, .room-code, .credit-info {
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 500;
        }
        
        .schedule-time::before { content: '📅'; }
        .faculty-name::before { content: '👨‍🏫'; }
        .room-code::before { content: '🏫'; }
        .credit-info::before { content: '🎯'; }
        
        /* Footer */
        .footer {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            text-align: center;
            padding: 20px;
        }
        
        .footer-content {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .generation-info, .system-info, .print-info {
            font-size: 12px;
            opacity: 0.9;
        }
        
        .print-info {
            font-weight: 600;
            color: #f39c12;
        }
        
        /* Print Styles */
        @media print {
            body {
                background: white !important;
                font-size: 10px;
            }
            
            .container {
                box-shadow: none !important;
                border-radius: 0 !important;
            }
            
            .header, .footer {
                break-inside: avoid;
            }
            
            .course-block, .stat-card, .course-item {
                break-inside: avoid;
            }
            
            .schedule-table {
                page-break-inside: auto;
            }
            
            .schedule-table tr {
                page-break-inside: avoid;
                page-break-after: auto;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 1200px) {
            .container {
                margin: 10px;
                border-radius: 0;
            }
            
            .content {
                padding: 20px;
            }
        }
        
        @media (max-width: 768px) {
            .university-name {
                font-size: 24px;
            }
            
            .department-name {
                font-size: 16px;
            }
            
            .schedule-meta {
                flex-direction: column;
                gap: 10px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
            
            .course-details-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Comprehensive Routine Styles */
        .routine-table-container {
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            background: white;
            margin: 20px 0;
        }
        
        .routine-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            font-size: 11px;
        }
        
        .routine-table th {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 12px;
            border: 1px solid #1a252f;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .day-header {
            background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
            width: 100px;
        }
        
        .room-header {
            background: linear-gradient(135deg, #f39c12, #d68910) !important;
            width: 80px;
        }
        
        .time-header {
            background: linear-gradient(135deg, #3498db, #2980b9) !important;
            min-width: 120px;
        }
        
        .routine-row:nth-child(even) {
            background: #f8f9fa;
        }
        
        .routine-row:hover {
            background: #e3f2fd;
            transform: scale(1.001);
            transition: all 0.2s ease;
        }
        
        .day-cell {
            background: linear-gradient(135deg, #ecf0f1, #bdc3c7);
            font-weight: 700;
            font-size: 14px;
            text-align: center;
            vertical-align: middle;
            border: 2px solid #95a5a6;
            color: #2c3e50;
            text-transform: uppercase;
        }
        
        .day-name {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 8px;
        }
        
        .room-cell {
            background: linear-gradient(135deg, #fff3e0, #ffcc80);
            font-weight: 600;
            text-align: center;
            padding: 8px;
            border: 1px solid #ffb74d;
            color: #e65100;
        }
        
        .room-name {
            font-size: 12px;
            font-weight: 700;
        }
        
        .course-entry {
            background: white;
            border-radius: 6px;
            padding: 6px;
            margin: 2px;
            border-left: 4px solid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        
        .course-entry:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .course-entry.theory-course {
            border-left-color: #3498db;
            background: linear-gradient(135deg, #e8f4fd, #d4f1ff);
        }
        
        .course-entry.lab-course {
            border-left-color: #f39c12;
            background: linear-gradient(135deg, #fff8e1, #ffecb3);
        }
        
        .course-code {
            font-weight: 700;
            font-size: 10px;
            color: #2c3e50;
            text-transform: uppercase;
            margin-bottom: 2px;
        }
        
        .course-batch {
            font-size: 9px;
            color: #7f8c8d;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .faculty-name {
            font-size: 8px;
            color: #5d6d7e;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .empty-slot {
            padding: 12px;
            text-align: center;
            color: #95a5a6;
            font-style: italic;
        }
        
        .free-text {
            font-size: 10px;
            opacity: 0.7;
        }
        
        .comprehensive-stats {
            margin: 20px 0;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 12px;
            border: 1px solid #dee2e6;
        }
        
        .batch-breakdown {
            margin-top: 20px;
        }
        
        .batch-breakdown h4 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .batch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }
        
        .batch-card {
            background: white;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
            transition: all 0.2s ease;
        }
        
        .batch-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .batch-name {
            font-weight: 700;
            color: #2c3e50;
            font-size: 12px;
            margin-bottom: 4px;
        }
        
        .batch-count {
            color: #7f8c8d;
            font-size: 11px;
        }
        
        .schedule-title {
            font-size: 20px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 10px;
            font-weight: 600;
        }
    )";}

// Database-integrated schedule generation
bool AcademicPDFGenerator::generateScheduleFromDatabase(
    const std::string& batchCode,
    const std::string& sectionName,
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::cout << "🎓 Generating professional schedule for " << batchCode << " Section " << sectionName << std::endl;
    
    try {
        // Check that we have a valid database connection
        if (!dbManager) {
            std::cerr << "❌ Error: Database manager is not initialized" << std::endl;
            return false;
        }
        
        // Get schedule data from database
        std::cout << "📊 Fetching schedule data from database..." << std::endl;
        auto pdfData = dbManager->getPDFScheduleData(batchCode, sectionName, academicYear, semester);
        
        // Check if we got any schedule data
        if (pdfData.schedules.empty()) {
            std::cerr << "❌ No schedule data found for " << batchCode << " Section " << sectionName << std::endl;
            
            // Try to provide more information about why data might be missing
            if (pdfData.courses.empty()) {
                std::cerr << "   • No courses found for batch " << batchCode << std::endl;
            }
            if (pdfData.teachers.empty()) {
                std::cerr << "   • No teacher data available in database" << std::endl;
            }
            if (pdfData.rooms.empty()) {
                std::cerr << "   • No room data available in database" << std::endl;
            }
            if (pdfData.time_slots.empty()) {
                std::cerr << "   • No time slot data available in database" << std::endl;
            }
            
            std::cerr << "   • Try running with --init-db to reset and load sample data" << std::endl;
            return false;
        }
        
        std::cout << "✅ Found " << pdfData.schedules.size() << " scheduled sessions" << std::endl;
        
        // Convert database data to AcademicCourse format
        std::cout << "🔄 Converting database data to academic course format..." << std::endl;
        std::vector<AcademicCourse> courses = convertDBDataToAcademicCourses(pdfData);
        
        if (courses.empty()) {
            std::cerr << "❌ Failed to convert database data to course format" << std::endl;
            return false;
        }
        
        // Check for any "Unknown Course" entries
        int unknownCourseCount = 0;
        for (const auto& course : courses) {
            if (course.courseTitle == "Unknown Course") {
                unknownCourseCount++;
            }
        }
        
        if (unknownCourseCount > 0) {
            std::cerr << "⚠️ Warning: " << unknownCourseCount << " of " << courses.size() 
                      << " courses have unknown titles" << std::endl;
        }
        
        std::cout << "📊 Generated " << courses.size() << " course entries for the schedule" << std::endl;
        
        // Generate the schedule with professional academic formatting
        std::cout << "📄 Generating PDF schedule..." << std::endl;
        bool result = generateAcademicSchedulePDF(courses, outputPath, algorithm, academicYear, semester);
        
        if (result) {
            std::cout << "✅ Schedule generation successful!" << std::endl;
        } else {
            std::cerr << "❌ Failed to generate academic schedule PDF" << std::endl;
        }
        
        return result;
    }
    catch (const std::exception& e) {
        std::cerr << "❌ Exception during schedule generation: " << e.what() << std::endl;
        return false;
    }
    catch (...) {
        std::cerr << "❌ Unknown exception during schedule generation" << std::endl;
        return false;
    }
}

// Generate complete university schedule (all batches and sections)
bool AcademicPDFGenerator::generateUniversitySchedule(
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::cout << "🏛️ Generating complete university schedule..." << std::endl;
    
    // Get all batches from database
    auto batches = dbManager->getAllBatches();
    
    if (batches.empty()) {
        std::cerr << "❌ No batch data found in database" << std::endl;
        return false;
    }
    
    bool success = true;
    
    // Generate schedule for each batch and section
    for (const auto& batch : batches) {
        // Generate for Section A
        std::string sectionAPath = outputPath + "_" + batch.batch_code + "_A";
        if (!generateScheduleFromDatabase(batch.batch_code, "A", sectionAPath, algorithm, academicYear, semester)) {
            std::cerr << "⚠️ Failed to generate schedule for " << batch.batch_code << " Section A" << std::endl;
            success = false;
        }
        
        // Generate for Section B
        std::string sectionBPath = outputPath + "_" + batch.batch_code + "_B";
        if (!generateScheduleFromDatabase(batch.batch_code, "B", sectionBPath, algorithm, academicYear, semester)) {
            std::cerr << "⚠️ Failed to generate schedule for " << batch.batch_code << " Section B" << std::endl;
            success = false;
        }
    }
    
    if (success) {
        std::cout << "✅ University schedule generation completed!" << std::endl;
    }
    
    return success;
}

// Generate faculty-wise schedule from database
bool AcademicPDFGenerator::generateFacultyScheduleFromDB(
    const std::string& facultyCode,
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::cout << "👨‍🏫 Generating faculty schedule for " << facultyCode << std::endl;
    
    // Get all schedules and filter by faculty
    auto allSchedules = dbManager->getAllAcademicSchedules();
    auto allTeachers = dbManager->getAllTeachers();
    auto allCourses = dbManager->getAllAcademicCourses();
    auto allRooms = dbManager->getAllRooms();
    auto allTimeSlots = dbManager->getAllAcademicTimeSlots();
    
    // Find the teacher
    auto teacherIt = std::find_if(allTeachers.begin(), allTeachers.end(),
        [&facultyCode](const DatabaseManager::AcademicTeacher& t) {
            return t.teacher_code == facultyCode;
        });
    
    if (teacherIt == allTeachers.end()) {
        std::cerr << "❌ Faculty " << facultyCode << " not found" << std::endl;
        return false;
    }
    
    // Filter schedules for this teacher
    std::vector<DatabaseManager::AcademicSchedule> facultySchedules;
    std::copy_if(allSchedules.begin(), allSchedules.end(), std::back_inserter(facultySchedules),
        [&teacherIt](const DatabaseManager::AcademicSchedule& s) {
            return s.teacher_id == teacherIt->teacher_id &&
                   s.status == "SCHEDULED";
        });
    
    if (facultySchedules.empty()) {
        std::cerr << "❌ No schedule found for faculty " << facultyCode << std::endl;
        return false;
    }
    
    // Convert to AcademicCourse format
    std::vector<AcademicCourse> courses = convertSchedulesToCourses(
        facultySchedules, allCourses, allTeachers, allRooms, allTimeSlots);
    
    // Generate faculty-specific PDF
    return generateFacultySchedule(courses, teacherIt->full_name, outputPath, algorithm);
}

// Generate room utilization report from database
bool AcademicPDFGenerator::generateRoomUtilizationFromDB(
    const std::string& roomCode,
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::cout << "🏢 Generating room utilization for " << roomCode << std::endl;
    
    // Get all schedules and filter by room
    auto allSchedules = dbManager->getAllAcademicSchedules();
    auto allCourses = dbManager->getAllAcademicCourses();
    auto allTeachers = dbManager->getAllTeachers();
    auto allRooms = dbManager->getAllRooms();
    auto allTimeSlots = dbManager->getAllAcademicTimeSlots();
    
    // Find the room
    auto roomIt = std::find_if(allRooms.begin(), allRooms.end(),
        [&roomCode](const DatabaseManager::Room& r) {
            return r.room_code == roomCode;
        });
    
    if (roomIt == allRooms.end()) {
        std::cerr << "❌ Room " << roomCode << " not found" << std::endl;
        return false;
    }
    
    // Filter schedules for this room
    std::vector<DatabaseManager::AcademicSchedule> roomSchedules;
    std::copy_if(allSchedules.begin(), allSchedules.end(), std::back_inserter(roomSchedules),
        [&roomIt](const DatabaseManager::AcademicSchedule& s) {
            return s.room_id == roomIt->room_id &&
                   s.status == "SCHEDULED";
        });
    
    if (roomSchedules.empty()) {
        std::cerr << "❌ No schedule found for room " << roomCode << std::endl;
        return false;
    }
    
    // Convert to AcademicCourse format
    std::vector<AcademicCourse> courses = convertSchedulesToCourses(
        roomSchedules, allCourses, allTeachers, allRooms, allTimeSlots);
    
    // Generate room-specific schedule
    return generateRoomSchedule(courses, roomCode, outputPath, algorithm);
}

// Faculty schedule generation
bool AcademicPDFGenerator::generateFacultySchedule(
    const std::vector<AcademicCourse>& courses,
    const std::string& facultyName,
    const std::string& outputPath,
    const std::string& algorithm) {
    
    std::cout << "👨‍🏫 Generating faculty schedule for " << facultyName << std::endl;
    
    // Filter courses for this faculty
    std::vector<AcademicCourse> facultyCourses;
    std::copy_if(courses.begin(), courses.end(), std::back_inserter(facultyCourses),
        [&facultyName](const AcademicCourse& course) {
            return course.facultyName == facultyName;
        });
    
    if (facultyCourses.empty()) {
        std::cerr << "❌ No courses found for faculty " << facultyName << std::endl;
        return false;
    }
    
    // Generate faculty-specific HTML
    std::string htmlPath = outputPath + ".html";
    if (!generateFacultyScheduleHTML(facultyCourses, facultyName, htmlPath, algorithm)) {
        return false;
    }
    
    std::cout << "📄 Generated faculty HTML schedule: " << htmlPath << std::endl;
    
    // Try automatic PDF conversion
    std::string pdfPath = outputPath + ".pdf";
    if (PDFGenerator::convertHTMLtoPDF(htmlPath, pdfPath)) {
        std::cout << "✅ Faculty PDF generated successfully!" << std::endl;
        return PDFGenerator::openInBrowser(pdfPath);
    } else {
        std::cout << "📱 Opening HTML in browser for manual PDF conversion..." << std::endl;
        return PDFGenerator::openInBrowser(htmlPath);
    }
}

// Room schedule generation
bool AcademicPDFGenerator::generateRoomSchedule(
    const std::vector<AcademicCourse>& courses,
    const std::string& roomCode,
    const std::string& outputPath,
    const std::string& algorithm) {
    
    std::cout << "🏫 Generating room schedule for " << roomCode << std::endl;
    
    // Filter courses for this room
    std::vector<AcademicCourse> roomCourses;
    std::copy_if(courses.begin(), courses.end(), std::back_inserter(roomCourses),
        [&roomCode](const AcademicCourse& course) {
            return course.roomCode == roomCode;
        });
    
    if (roomCourses.empty()) {
        std::cerr << "❌ No courses found for room " << roomCode << std::endl;
        return false;
    }
    
    // Generate room-specific HTML
    std::string htmlPath = outputPath + ".html";
    if (!generateRoomScheduleHTML(roomCourses, roomCode, htmlPath, algorithm)) {
        return false;
    }
    
    std::cout << "📄 Generated room HTML schedule: " << htmlPath << std::endl;
    
    // Try automatic PDF conversion
    std::string pdfPath = outputPath + ".pdf";
    if (PDFGenerator::convertHTMLtoPDF(htmlPath, pdfPath)) {
        std::cout << "✅ Room PDF generated successfully!" << std::endl;
        return PDFGenerator::openInBrowser(pdfPath);
    } else {
        std::cout << "📱 Opening HTML in browser for manual PDF conversion..." << std::endl;
        return PDFGenerator::openInBrowser(htmlPath);
    }
}

// Faculty schedule HTML generation
bool AcademicPDFGenerator::generateFacultyScheduleHTML(
    const std::vector<AcademicCourse>& courses,
    const std::string& facultyName,
    const std::string& htmlPath,
    const std::string& algorithm) {
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "❌ Error: Cannot create HTML file " << htmlPath << std::endl;
        return false;
    }
    
    // Generate faculty-specific schedule HTML
    file << R"(<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faculty Schedule - )" << facultyName << R"(</title>
    <style>)" << generateAcademicCSS() << R"(</style>
</head>
<body>
    <div class="container">
        )" << generateProfessionalHeader("Faculty Schedule", "", "", "2024-25", "Spring") << R"(
        
        <div class="faculty-info">
            <h2>👨‍🏫 )" << facultyName << R"(</h2>
            <p class="faculty-details">Teaching Schedule - )" << algorithm << R"( Algorithm</p>
        </div>
        
        <main class="content">
            )" << generateStatistics(courses) << R"(
            
            <div class="schedule-section">
                <h3 class="section-title">📅 Weekly Teaching Schedule</h3>
                )" << generateTimeSlotGrid(courses) << R"(
            </div>
            
            <div class="details-section">
                <h3 class="section-title">📚 Course Assignments</h3>
                )" << generateCourseDetails(courses) << R"(
            </div>
        </main>
        
        <footer class="footer">
            <div class="footer-content">
                <p class="generation-info">📄 Generated on: )" << getCurrentTimestamp() << R"(</p>
                <p class="system-info">🖥️ BUP Faculty Scheduling System | Algorithm: )" << algorithm << R"(</p>
            </div>
        </footer>
    </div>
</body>
</html>)";
    
    file.close();
    return true;
}

// Room schedule HTML generation
bool AcademicPDFGenerator::generateRoomScheduleHTML(
    const std::vector<AcademicCourse>& courses,
    const std::string& roomCode,
    const std::string& htmlPath,
    const std::string& algorithm) {
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "❌ Error: Cannot create HTML file " << htmlPath << std::endl;
        return false;
    }
    
    // Generate room-specific schedule HTML
    file << R"(<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Room Schedule - )" << roomCode << R"(</title>
    <style>)" << generateAcademicCSS() << R"(</style>
</head>
<body>
    <div class="container">
        )" << generateProfessionalHeader("Room Utilization Schedule", "", "", "2024-25", "Spring") << R"(
        
        <div class="room-info">
            <h2>🏫 Room )" << roomCode << R"(</h2>
            <p class="room-details">Utilization Schedule - )" << algorithm << R"( Algorithm</p>
        </div>
        
        <main class="content">
            )" << generateStatistics(courses) << R"(
            
            <div class="schedule-section">
                <h3 class="section-title">📅 Room Usage Schedule</h3>
                )" << generateTimeSlotGrid(courses) << R"(
            </div>
            
            <div class="details-section">
                <h3 class="section-title">📚 Scheduled Classes</h3>
                )" << generateCourseDetails(courses) << R"(
            </div>
        </main>
        
        <footer class="footer">
            <div class="footer-content">
                <p class="generation-info">📄 Generated on: )" << getCurrentTimestamp() << R"(</p>
                <p class="system-info">🖥️ BUP Room Scheduling System | Algorithm: )" << algorithm << R"(</p>
            </div>
        </footer>
    </div>
</body>
</html>)";
    
    file.close();
    return true;
}

// Missing method implementations

std::string AcademicPDFGenerator::getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    auto tm = *std::localtime(&time_t);
    
    std::ostringstream oss;
    oss << std::put_time(&tm, "%B %d, %Y at %I:%M %p");
    return oss.str();
}

std::vector<AcademicCourse> AcademicPDFGenerator::convertDBDataToAcademicCourses(
    const DatabaseManager::PDFScheduleData& pdfData) {
    
    std::vector<AcademicCourse> courses;
    
    // Check if we have valid data before proceeding
    if (pdfData.schedules.empty()) {
        std::cerr << "⚠️ Warning: No schedule data available for conversion" << std::endl;
        return courses;
    }
    
    for (const auto& schedule : pdfData.schedules) {
        AcademicCourse course;
        
        // Set batch and section information from PDF data
        course.batchName = pdfData.batch_code;
        course.sectionName = pdfData.section_name;
        
        // Set default values in case we don't find matches
        course.courseCode = "CSE-XXX";
        course.courseTitle = "Unknown Course";
        course.facultyName = "TBA";
        course.facultyDesignation = "Faculty";
        course.roomCode = "TBD";
        course.timeSlot = "TBD";
        course.dayOfWeek = "MON";
        course.startTime = "09:00";
        course.endTime = "10:30";
        course.creditHours = 3.0;
        course.classType = "THEORY";
        course.isExternal = false;
        
        // Find corresponding course - safely
        if (!pdfData.courses.empty()) {
            auto courseIt = std::find_if(pdfData.courses.begin(), pdfData.courses.end(),
                [&](const DatabaseManager::AcademicCourse& c) { 
                    return c.course_id == schedule.course_id; 
                });
            
            if (courseIt != pdfData.courses.end()) {
                course.courseCode = courseIt->course_code.empty() ? "CSE-XXX" : courseIt->course_code;
                course.courseTitle = courseIt->course_title.empty() ? "Unknown Course" : courseIt->course_title;
                course.creditHours = courseIt->credit_hours;
                course.classType = courseIt->class_type.empty() ? "THEORY" : courseIt->class_type;
                
                // Log successful course processing
                std::cout << "  ✓ Processed: " << course.courseCode << " - " << course.courseTitle << std::endl;
            } else {
                // Log when course is not found
                std::cerr << "  ⚠️ Warning: No course data found for course_id: " << schedule.course_id << std::endl;
            }
        } else {
            // Log empty courses array
            std::cerr << "  ⚠️ Warning: No course data available in PDF data" << std::endl;
        }
        
        // Find corresponding teacher - safely
        if (!pdfData.teachers.empty()) {
            auto teacherIt = std::find_if(pdfData.teachers.begin(), pdfData.teachers.end(),
                [&](const DatabaseManager::AcademicTeacher& t) { 
                    return t.teacher_id == schedule.teacher_id; 
                });
            
            if (teacherIt != pdfData.teachers.end()) {
                course.facultyName = teacherIt->full_name.empty() ? "TBA" : teacherIt->full_name;
                course.facultyDesignation = teacherIt->designation.empty() ? "Faculty" : teacherIt->designation;
                course.isExternal = teacherIt->external_faculty;
                
                // Log teacher assignment
                std::cout << "    → Assigned teacher: " << course.facultyName;
                if (!course.facultyDesignation.empty()) {
                    std::cout << " (" << course.facultyDesignation << ")";
                }
                std::cout << std::endl;
            } else {
                std::cerr << "    ⚠️ Warning: No teacher found for teacher_id: " << schedule.teacher_id << std::endl;
            }
        } else {
            std::cerr << "    ⚠️ Warning: No teacher data available in PDF data" << std::endl;
        }
        
        // Find corresponding room - safely
        if (!pdfData.rooms.empty()) {
            auto roomIt = std::find_if(pdfData.rooms.begin(), pdfData.rooms.end(),
                [&](const DatabaseManager::Room& r) { 
                    return r.room_id == schedule.room_id; 
                });
            
            if (roomIt != pdfData.rooms.end()) {
                course.roomCode = roomIt->room_code.empty() ? "TBD" : roomIt->room_code;
                std::cout << "    → Assigned room: " << course.roomCode << std::endl;
            } else {
                std::cerr << "    ⚠️ Warning: No room found for room_id: " << schedule.room_id << std::endl;
            }
        } else {
            std::cerr << "    ⚠️ Warning: No room data available in PDF data" << std::endl;
        }
        
        // Find corresponding time slot - safely
        if (!pdfData.time_slots.empty()) {
            auto timeSlotIt = std::find_if(pdfData.time_slots.begin(), pdfData.time_slots.end(),
                [&](const DatabaseManager::AcademicTimeSlot& ts) { 
                    return ts.slot_id == schedule.slot_id; 
                });
            
            if (timeSlotIt != pdfData.time_slots.end()) {
                course.timeSlot = timeSlotIt->slot_name.empty() ? "TBD" : timeSlotIt->slot_name;
                course.dayOfWeek = timeSlotIt->day_of_week.empty() ? "MON" : timeSlotIt->day_of_week;
                course.startTime = timeSlotIt->start_time.empty() ? "09:00" : timeSlotIt->start_time;
                course.endTime = timeSlotIt->end_time.empty() ? "10:30" : timeSlotIt->end_time;
                
                std::cout << "    → Scheduled: " << course.dayOfWeek << " " 
                          << course.startTime << "-" << course.endTime
                          << " (" << course.timeSlot << ")" << std::endl;
            } else {
                std::cerr << "    ⚠️ Warning: No time slot found for slot_id: " << schedule.slot_id << std::endl;
            }
        } else {
            std::cerr << "    ⚠️ Warning: No time slot data available in PDF data" << std::endl;
        }
        
        // Calculate session duration based on credit hours and type
        if (course.classType == "LAB") {
            course.sessionDuration = 180; // 3 hours for lab
        } else {
            course.sessionDuration = static_cast<int>(course.creditHours * 60); // 1 hour per credit
        }
        
        // Set session number and enrolled students
        course.sessionNumber = schedule.session_number;
        course.enrolledStudents = 40; // Default enrollment
        
        // Add the course to our list
        courses.push_back(course);
        
        std::cout << "  ✓ Processed: " << course.courseCode << " - " << course.courseTitle << std::endl;
    }
    
    // Sort courses by day and time for better display
    std::sort(courses.begin(), courses.end(), [](const AcademicCourse& a, const AcademicCourse& b) {
        // First sort by day of week
        static const std::map<std::string, int> dayOrder = {
            {"SUN", 0}, {"MON", 1}, {"TUE", 2}, {"WED", 3}, {"THU", 4}, {"FRI", 5}, {"SAT", 6}
        };
        
        int aDay = dayOrder.count(a.dayOfWeek) ? dayOrder.at(a.dayOfWeek) : 7;
        int bDay = dayOrder.count(b.dayOfWeek) ? dayOrder.at(b.dayOfWeek) : 7;
        
        if (aDay != bDay) return aDay < bDay;
        
        // Then sort by start time
        return a.startTime < b.startTime;
    });
    
    std::cout << "📊 Generated " << courses.size() << " course entries for the schedule" << std::endl;
    return courses;
}

std::vector<AcademicCourse> AcademicPDFGenerator::convertSchedulesToCourses(
    const std::vector<DatabaseManager::AcademicSchedule>& schedules,
    const std::vector<DatabaseManager::AcademicCourse>& allCourses,
    const std::vector<DatabaseManager::AcademicTeacher>& allTeachers,
    const std::vector<DatabaseManager::Room>& allRooms,
    const std::vector<DatabaseManager::AcademicTimeSlot>& allTimeSlots) {
    
    std::vector<AcademicCourse> courses;
    
    // Check if we have any schedules to process
    if (schedules.empty()) {
        std::cerr << "⚠️ Warning: No schedules provided for conversion" << std::endl;
        return courses;
    }
    
    // Log what we're processing
    std::cout << "🔄 Processing " << schedules.size() << " schedule entries" << std::endl;
    std::cout << "📚 Available data: " 
              << allCourses.size() << " courses, " 
              << allTeachers.size() << " teachers, " 
              << allRooms.size() << " rooms, " 
              << allTimeSlots.size() << " time slots" << std::endl;
    
    for (const auto& schedule : schedules) {
        AcademicCourse course;
        
        // Set default values in case we don't find matches
        course.courseCode = "CSE-XXX";
        course.courseTitle = "Unknown Course";
        course.creditHours = 3.0;
        course.classType = "THEORY";
        course.facultyName = "TBA";
        course.facultyDesignation = "Faculty";
        course.isExternal = false;
        course.roomCode = "TBD";
        course.timeSlot = "TBD";
        course.dayOfWeek = "MON";
        course.startTime = "09:00";
        course.endTime = "10:30";
        
        // Find corresponding course - safely
        if (!allCourses.empty()) {
            auto courseIt = std::find_if(allCourses.begin(), allCourses.end(),
                [&](const DatabaseManager::AcademicCourse& c) { return c.course_id == schedule.course_id; });
            
            if (courseIt != allCourses.end()) {
                course.courseCode = courseIt->course_code.empty() ? "CSE-XXX" : courseIt->course_code;
                course.courseTitle = courseIt->course_title.empty() ? "Unknown Course" : courseIt->course_title;
                course.creditHours = courseIt->credit_hours;
                course.classType = courseIt->class_type.empty() ? "THEORY" : courseIt->class_type;
            }
        }
        
        // Find corresponding teacher - safely
        if (!allTeachers.empty()) {
            auto teacherIt = std::find_if(allTeachers.begin(), allTeachers.end(),
                [&](const DatabaseManager::AcademicTeacher& t) { return t.teacher_id == schedule.teacher_id; });
            
            if (teacherIt != allTeachers.end()) {
                course.facultyName = teacherIt->full_name.empty() ? "TBA" : teacherIt->full_name;
                course.facultyDesignation = teacherIt->designation.empty() ? "Faculty" : teacherIt->designation;
                course.isExternal = teacherIt->external_faculty;
            }
        }
        
        // Find corresponding room - safely
        if (!allRooms.empty()) {
            auto roomIt = std::find_if(allRooms.begin(), allRooms.end(),
                [&](const DatabaseManager::Room& r) { return r.room_id == schedule.room_id; });
            
            if (roomIt != allRooms.end()) {
                course.roomCode = roomIt->room_code.empty() ? "TBD" : roomIt->room_code;
            }
        }
        
        // Find corresponding time slot - safely
        if (!allTimeSlots.empty()) {
            auto timeSlotIt = std::find_if(allTimeSlots.begin(), allTimeSlots.end(),
                [&](const DatabaseManager::AcademicTimeSlot& ts) { return ts.slot_id == schedule.slot_id; });
            if (timeSlotIt != allTimeSlots.end()) {
                course.timeSlot = timeSlotIt->slot_name;
                course.dayOfWeek = timeSlotIt->day_of_week;
                course.startTime = timeSlotIt->start_time;
                course.endTime = timeSlotIt->end_time;
            }
        }
        
        // Set batch and section from schedule (will need to be passed separately or looked up)
        course.batchName = "BCSE23"; // Default batch name - should be passed as parameter
        course.sectionName = "A";    // Default section - should be passed as parameter
        
        // Calculate session duration
        if (course.classType == "LAB") {
            course.sessionDuration = 180; // 3 hours for lab
        } else {
            course.sessionDuration = static_cast<int>(course.creditHours * 60); // 1 hour per credit
        }
        
        course.sessionNumber = schedule.session_number;
        course.enrolledStudents = 40; // Default enrollment
        
        courses.push_back(course);
    }
    
    return courses;
}

std::string AcademicPDFGenerator::generateProfessionalHeader(
    const std::string& title,
    const std::string& batchCode,
    const std::string& sectionName,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::ostringstream header;
    header << "<header class=\"main-header\">";
    header << "<div class=\"university-info\">";
    header << "<div class=\"university-logo\">";
    header << "<h1 class=\"university-name\">🎓 Bangladesh University of Professionals</h1>";
    header << "<p class=\"university-subtitle\">Faculty of Science & Technology</p>";
    header << "</div>";
    header << "<div class=\"schedule-info\">";
    header << "<h2 class=\"schedule-title\">" << title << "</h2>";
    
    if (!batchCode.empty()) {
        header << "<div class=\"academic-details\">";
        header << "<span class=\"batch-info\">📚 Batch: " << batchCode << "</span>";
        if (!sectionName.empty()) {
            header << " | <span class=\"section-info\">📝 Section: " << sectionName << "</span>";
        }
        header << "<br>";
        header << "<span class=\"year-info\">📅 Academic Year: " << academicYear << "</span>";
        header << " | <span class=\"semester-info\">🌟 Semester: " << semester << "</span>";
        header << "</div>";
    }
    
    header << "</div>";
    header << "</div>";
    header << "</header>";
    
    return header.str();
}

// Generate comprehensive university routine (proper format with days as rows, rooms as sub-rows, time slots as columns)
bool AcademicPDFGenerator::generateComprehensiveUniversityRoutine(
    const std::string& outputPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    std::cout << "🏛️ Generating comprehensive university routine for all batches..." << std::endl;
    
    // Get all data from database
    auto batches = dbManager->getAllBatches();
    auto allCourses = dbManager->getAllAcademicCourses();
    auto allSchedules = dbManager->getAllAcademicSchedules();
    auto allTeachers = dbManager->getAllTeachers();
    auto allRooms = dbManager->getAllRooms();
    auto allTimeSlots = dbManager->getAllAcademicTimeSlots();
    
    if (batches.empty() || allCourses.empty()) {
        std::cerr << "❌ No data found in database for comprehensive routine" << std::endl;
        return false;
    }
    
    std::cout << "📊 Found data: " << batches.size() << " batches, " 
              << allCourses.size() << " courses, " << allSchedules.size() << " schedules" << std::endl;
    
    // Convert all database data to AcademicCourse format
    std::vector<AcademicCourse> comprehensiveCourses;
    
    for (const auto& batch : batches) {
        for (const std::string& section : {"A", "B"}) {
            std::cout << "🔄 Processing " << batch.batch_code << " Section " << section << std::endl;
            
            // Get schedule data for this batch and section
            auto scheduleData = dbManager->getPDFScheduleData(batch.batch_code, section, academicYear, semester);
            auto batchCourses = convertDBDataToAcademicCourses(scheduleData);
            
            // Add to comprehensive list
            comprehensiveCourses.insert(comprehensiveCourses.end(), batchCourses.begin(), batchCourses.end());
        }
    }
    
    std::cout << "✅ Total courses processed: " << comprehensiveCourses.size() << std::endl;
    
    if (comprehensiveCourses.empty()) {
        std::cerr << "❌ No courses found after processing all batches" << std::endl;
        return false;
    }
    
    // Generate HTML with comprehensive routine format
    std::string htmlPath = outputPath + "_comprehensive_routine.html";
    if (!generateComprehensiveRoutineHTML(comprehensiveCourses, htmlPath, algorithm, academicYear, semester)) {
        return false;
    }
    
    std::cout << "📄 Generated comprehensive HTML routine: " << htmlPath << std::endl;
    
    // Generate PDF
    std::string pdfPath = outputPath + "_comprehensive_routine.pdf";
    if (PDFGenerator::convertHTMLtoPDF(htmlPath, pdfPath)) {
        std::cout << "✅ Comprehensive university routine PDF generated successfully!" << std::endl;
        return PDFGenerator::openInBrowser(pdfPath);
    } else {
        std::cout << "📱 Opening HTML in browser for manual PDF conversion..." << std::endl;
        std::cout << "💡 In browser: Press Cmd+P → Save as PDF" << std::endl;
        return PDFGenerator::openInBrowser(htmlPath);
    }
}

// Generate comprehensive routine HTML with proper university format
bool AcademicPDFGenerator::generateComprehensiveRoutineHTML(
    const std::vector<AcademicCourse>& courses,
    const std::string& htmlPath,
    const std::string& algorithm,
    const std::string& academicYear,
    const std::string& semester) {
    
    // Create parent directories if they don't exist
    size_t lastSlash = htmlPath.find_last_of("/\\");
    if (lastSlash != std::string::npos) {
        std::string directory = htmlPath.substr(0, lastSlash);
        std::string mkdirCommand = "mkdir -p \"" + directory + "\"";
        system(mkdirCommand.c_str());
    }
    
    std::ofstream file(htmlPath);
    if (!file.is_open()) {
        std::cerr << "❌ Error: Cannot create HTML file " << htmlPath << std::endl;
        std::cerr << "   Path: " << htmlPath << std::endl;
        return false;
    }
    
    // HTML Document Structure with new layout
    file << R"(<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive University Routine - BUP CSE Department</title>
    <style>)" << generateAcademicCSS() << R"(</style>
</head>
<body>
    <div class="container">
        <!-- University Header -->
        <header class="header">
            <div class="header-content">
                <div class="university-logo">
                    <div class="logo-icon">🎓</div>
                    <div class="logo-text">BUP</div>
                </div>
                <div class="university-info">
                    <h1 class="university-name">Bangladesh University of Professionals</h1>
                    <h2 class="department-name">Department of Computer Science & Engineering</h2>
                    <h3 class="schedule-title">Comprehensive Class Routine - All Batches</h3>
                    <div class="schedule-meta">
                        <div class="academic-info">
                            <span class="academic-year">Academic Year: )" << academicYear << R"(</span>
                            <span class="semester">)" << semester << R"( Semester</span>
                        </div>
                        <div class="algorithm-info">
                            <span class="algorithm-badge">)" << algorithm << R"( Algorithm</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="content">
            <!-- Statistics Section -->
            )" << generateAllBatchesStatistics(courses) << R"(
            
            <!-- Comprehensive Routine Table -->
            <div class="routine-section">
                <h3 class="section-title">📅 University Class Routine (All Batches & Sections)</h3>
                )" << generateDayBasedScheduleTable(courses) << R"(
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <p class="generation-info">
                    📄 Generated on: )" << __DATE__ << R"( at )" << __TIME__ << R"(
                </p>
                <p class="system-info">
                    🖥️ BUP Conflict-Free Scheduling System | Algorithm: )" << algorithm << R"( | Comprehensive Routine
                </p>
                <p class="print-info">
                    💡 For PDF: Press <strong>Ctrl+P</strong> (Windows) or <strong>Cmd+P</strong> (Mac) → Save as PDF
                </p>
            </div>
        </footer>
    </div>
</body>
</html>)";
    
    file.close();
    std::cout << "✅ Comprehensive routine HTML file generated successfully: " << htmlPath << std::endl;
    return true;
}

// Generate day-based schedule table (Days as rows, rooms as sub-rows, time slots as columns)
std::string AcademicPDFGenerator::generateDayBasedScheduleTable(const std::vector<AcademicCourse>& allCourses) {
    std::ostringstream table;
    // Fix: University working days are SUN-THU only (not FRI/SAT)
    std::vector<std::string> days = {"SUN", "MON", "TUE", "WED", "THU"};
    
    // Fix: Get dynamic time slots from database instead of hardcoded values
    auto allTimeSlots = dbManager->getAllAcademicTimeSlots();
    std::map<std::string, std::vector<std::string>> dayTimeSlots;
    
    // Group time slots by day and extract unique slot patterns
    for (const auto& slot : allTimeSlots) {
        std::string dayKey = slot.day_of_week;
        std::string slotDisplay = extractSlotPattern(slot.slot_name) + " (" + 
                                 slot.start_time.substr(0, 5) + "-" + 
                                 slot.end_time.substr(0, 5) + ")";
        dayTimeSlots[dayKey].push_back(slotDisplay);
    }
    
    // Get unified time slot list (use SUN as reference since all days should be similar)
    std::vector<std::string> timeSlots;
    if (dayTimeSlots.find("SUN") != dayTimeSlots.end()) {
        timeSlots = dayTimeSlots["SUN"];
    } else {
        // Fallback to updated time slots with lunch break
        timeSlots = {"S1 (08:30-10:00)", "S2 (10:05-11:35)", "S3 (11:40-13:10)", 
                    "LUNCH (13:10-13:55)", "S4 (13:55-15:25)", "S5 (15:30-17:00)"};
    }
    
    // Get all unique rooms
    std::set<std::string> roomSet;
    for (const auto& course : allCourses) {
        if (!course.roomCode.empty()) {
            roomSet.insert(course.roomCode);
        }
    }
    std::vector<std::string> rooms(roomSet.begin(), roomSet.end());
    std::sort(rooms.begin(), rooms.end());
    
    table << R"DELIM(
        <div class="routine-table-container">
            <table class="routine-table">
                <thead>
                    <tr>
                        <th class="day-header">Day</th>
                        <th class="room-header">Room</th>)DELIM";
    
    // Time slot headers
    for (const auto& slot : timeSlots) {
        table << R"DELIM(
                        <th class="time-header">)DELIM" << slot << R"DELIM(</th>)DELIM";
    }
    
    table << R"DELIM(
                    </tr>
                </thead>
                <tbody>)DELIM";
    
    // Generate rows for each day
    for (const auto& day : days) {
        bool firstRoom = true;
        
        for (const auto& room : rooms) {
            table << R"DELIM(
                    <tr class="routine-row">)DELIM";
            
            // Day column (merged for first room only)
            if (firstRoom) {
                table << R"DELIM(
                        <td class="day-cell" rowspan=")DELIM" << rooms.size() << R"DELIM(">
                            <div class="day-name">)DELIM" << getDayName(day) << R"DELIM(</div>
                        </td>)DELIM";
                firstRoom = false;
            }
            
            // Room column
            table << R"DELIM(
                        <td class="room-cell">
                            <div class="room-name">)DELIM" << room << R"DELIM(</div>
                        </td>)DELIM";
            
            // Time slot columns
            for (const auto& timeSlot : timeSlots) {
                table << R"DELIM(
                        <td class="course-cell">)DELIM";
                
                // Extract slot pattern for matching (e.g., "SLOT1 (08:30-10:00)" -> "SLOT1")
                std::string slotPattern = timeSlot.substr(0, timeSlot.find(' '));
                
                // Find courses for this day, room, and time slot
                std::vector<AcademicCourse> slotCourses;
                for (const auto& course : allCourses) {
                    if (course.dayOfWeek == day && course.roomCode == room) {
                        // Check if course time slot matches this slot pattern
                        std::string courseSlotPattern = extractSlotPattern(course.timeSlot);
                        if (courseSlotPattern == slotPattern || 
                            course.timeSlot.find(slotPattern) != std::string::npos) {
                            slotCourses.push_back(course);
                        }
                    }
                }
                
                if (!slotCourses.empty()) {
                    for (const auto& course : slotCourses) {
                        table << R"DELIM(
                            <div class="course-entry )DELIM" << getCourseTypeClass(course.classType) << R"DELIM(">
                                <div class="course-code">)DELIM" << course.courseCode << R"DELIM(</div>
                                <div class="course-batch">)DELIM" << course.batchName << R"DELIM(-)DELIM" << course.sectionName << R"DELIM(</div>
                                <div class="faculty-name">)DELIM" << course.facultyName << R"DELIM(</div>
                            </div>)DELIM";
                    }
                } else {
                    table << R"DELIM(
                            <div class="empty-slot">
                                <span class="free-text">Free</span>
                            </div>)DELIM";
                }
                
                table << R"DELIM(
                        </td>)DELIM";
            }
            
            table << R"DELIM(
                    </tr>)DELIM";
        }
    }
    
    table << R"DELIM(
                </tbody>
            </table>
        </div>)DELIM";
    
    return table.str();
}

// Generate statistics for all batches
std::string AcademicPDFGenerator::generateAllBatchesStatistics(const std::vector<AcademicCourse>& allCourses) {
    std::set<std::string> uniqueBatches, uniqueSections, uniqueFaculty, uniqueRooms;
    int totalTheory = 0, totalLab = 0;
    double totalCredits = 0;
    
    // Group by batches
    std::map<std::string, int> batchCounts;
    
    for (const auto& course : allCourses) {
        uniqueBatches.insert(course.batchName);
        uniqueSections.insert(course.batchName + "-" + course.sectionName);
        uniqueFaculty.insert(course.facultyName);
        uniqueRooms.insert(course.roomCode);
        
        batchCounts[course.batchName + "-" + course.sectionName]++;
        
        if (course.classType == "THEORY") totalTheory++;
        else if (course.classType == "LAB") totalLab++;
        
        totalCredits += course.creditHours;
    }
    
    std::ostringstream stats;
    stats << R"DELIM(
        <div class="comprehensive-stats">
            <h3 class="section-title">📊 University Schedule Overview</h3>
            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon">🎓</div>
                    <div class="stat-number">4</div>
                    <div class="stat-label">Batches</div>
                </div>
                <div class="stat-card info">
                    <div class="stat-icon">👥</div>
                    <div class="stat-number">8</div>
                    <div class="stat-label">Sections</div>
                </div>
                <div class="stat-card success">
                    <div class="stat-icon">📚</div>
                    <div class="stat-number">)DELIM" << allCourses.size() << R"DELIM(</div>
                    <div class="stat-label">Total Classes</div>
                </div>
                <div class="stat-card warning">
                    <div class="stat-icon">👨‍🏫</div>
                    <div class="stat-number">6</div>
                    <div class="stat-label">Faculty</div>
                </div>
                <div class="stat-card secondary">
                    <div class="stat-icon">🏫</div>
                    <div class="stat-number">6</div>
                    <div class="stat-label">Rooms</div>
                </div>
                <div class="stat-card dark">
                    <div class="stat-icon">🔬</div>
                    <div class="stat-number">)DELIM" << totalLab << R"DELIM(/)DELIM" << totalTheory << R"DELIM(</div>
                    <div class="stat-label">Lab/Theory</div>
                </div>
            </div>
            
            <!-- Batch-wise breakdown -->
            <div class="batch-breakdown">
                <h4>📋 Batch-wise Schedule Distribution</h4>
                <div class="batch-grid">)DELIM";
    
    for (const auto& batchPair : batchCounts) {
        stats << R"DELIM(
                    <div class="batch-card">
                        <div class="batch-name">)DELIM" << batchPair.first << R"DELIM(</div>
                        <div class="batch-count">)DELIM" << batchPair.second << R"DELIM( classes</div>
                    </div>)DELIM";
    }
    
    stats << R"DELIM(
                </div>
            </div>
        </div>)DELIM";
    
    return stats.str();
}

// Extract slot pattern from database slot names (handles SUN_S1, SUN_SLOT1, etc.)
std::string AcademicPDFGenerator::extractSlotPattern(const std::string& slotName) {
    // Handle different slot name formats from database
    size_t underscorePos = slotName.find('_');
    if (underscorePos != std::string::npos) {
        std::string slotPart = slotName.substr(underscorePos + 1);
        
        // Convert SUN_S1 -> S1, SUN_SLOT1 -> SLOT1, etc.
        if (slotPart.substr(0, 4) == "SLOT") {
            // Handle SUN_SLOT1 format -> SLOT1
            return slotPart;
        } else if (slotPart.length() >= 2 && (slotPart[0] == 'S' || slotPart[0] == 'L')) {
            // Handle SUN_S1, SUN_L1 format -> S1, L1
            return slotPart;
        }
    }
    
    // Fallback: return the original name
    return slotName;
}

// CSV to Academic Course conversion for enhanced weekly routine generation
std::vector<AcademicCourse> AcademicPDFGenerator::convertActivitiesToAcademicCourses(
    const std::vector<Activity>& activities,
    const std::vector<std::string>& courseNames,
    const std::vector<std::string>& teacherNames) {
    
    std::vector<AcademicCourse> academicCourses;
    
    // Define default mapping for time slots to days and periods
    std::map<int, std::pair<std::string, std::string>> timeSlotMapping = {
        {8, {"SUN", "S1"}}, {9, {"SUN", "S2"}}, {10, {"MON", "S1"}}, {11, {"MON", "S2"}},
        {12, {"TUE", "S1"}}, {13, {"TUE", "S2"}}, {14, {"WED", "S1"}}, {15, {"WED", "S2"}},
        {16, {"THU", "S1"}}, {17, {"THU", "S2"}}, {18, {"THU", "S3"}}
    };
    
    // Default room assignments
    std::vector<std::string> rooms = {"CR303", "CR304", "CR302", "LAB1", "LAB2"};
    
    for (size_t i = 0; i < activities.size(); ++i) {
        const auto& activity = activities[i];
        AcademicCourse course;
        
        // Basic course information
        course.courseCode = "CSE" + std::to_string(2200 + activity.id);
        course.courseTitle = (i < courseNames.size()) ? courseNames[i] : "Course " + std::to_string(activity.id);
        course.facultyName = (i < teacherNames.size()) ? teacherNames[i] : "Faculty " + std::to_string(activity.id);
        course.facultyDesignation = "Professor";
        course.roomCode = rooms[i % rooms.size()];
        course.sectionName = (i % 2 == 0) ? "A" : "B";
        course.batchName = "BCSE24";
        course.creditHours = 3.0;
        course.classType = "THEORY";
        course.sessionDuration = 90;
        course.enrolledStudents = static_cast<int>(activity.weight);
        course.isExternal = false;
        course.sessionNumber = 1;
        
        // Time mapping
        auto timeMapping = timeSlotMapping.find(activity.start);
        if (timeMapping != timeSlotMapping.end()) {
            course.dayOfWeek = timeMapping->second.first;
            course.timeSlot = timeMapping->second.first + "_" + timeMapping->second.second;
        } else {
            course.dayOfWeek = "SUN";
            course.timeSlot = "SUN_S1";
        }
        
        // Format times
        course.startTime = std::to_string(activity.start) + ":00";
        course.endTime = std::to_string(activity.end) + ":00";
        
        academicCourses.push_back(course);
    }
    
    return academicCourses;
}

// Generate weekly routine from CSV input
bool AcademicPDFGenerator::generateWeeklyRoutineFromCSV(
    const std::vector<Activity>& activities,
    const std::vector<std::string>& courseNames, 
    const std::vector<std::string>& teacherNames,
    const std::string& outputPath,
    const std::string& algorithm) {
    
    std::cout << "\n🎓 === Generating Weekly Routine from CSV ===" << std::endl;
    std::cout << "Converting CSV data to academic schedule format..." << std::endl;
    
    // Convert activities to academic courses
    auto academicCourses = convertActivitiesToAcademicCourses(activities, courseNames, teacherNames);
    
    if (academicCourses.empty()) {
        std::cerr << "❌ Failed to convert activities to academic courses" << std::endl;
        return false;
    }
    
    std::cout << "✅ Converted " << academicCourses.size() << " courses to academic format" << std::endl;
    
    // Generate HTML with comprehensive routine format
    std::string htmlPath = outputPath + "_weekly_routine.html";
    if (!generateComprehensiveRoutineHTML(academicCourses, htmlPath, algorithm, "2024-25", "Spring")) {
        std::cerr << "❌ Failed to generate weekly routine HTML" << std::endl;
        return false;
    }
    
    std::cout << "📄 Generated weekly routine HTML: " << htmlPath << std::endl;
    
    // Try to generate PDF
    std::string pdfPath = outputPath + "_weekly_routine.pdf";
    if (PDFGenerator::convertHTMLtoPDF(htmlPath, pdfPath)) {
        std::cout << "✅ Weekly routine PDF generated successfully!" << std::endl;
        return PDFGenerator::openInBrowser(pdfPath);
    } else {
        std::cout << "📱 Opening HTML in browser for manual PDF conversion..." << std::endl;
        std::cout << "💡 In browser: Press Cmd+P → Save as PDF" << std::endl;
        return PDFGenerator::openInBrowser(htmlPath);
    }
}
