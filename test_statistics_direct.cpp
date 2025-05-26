#include <iostream>
#include <vector>
#include "src/utils/academic_pdf_generator.h"

int main() {
    try {
        std::cout << "🧪 Testing updated statistics directly..." << std::endl;
        
        // Create mock academic courses for testing
        std::vector<AcademicCourse> mockCourses = {
            {"CS101", "Data Structures", "BCSE25", "A", "THEORY", "Dr. Smith", "CR1003", "09:00-10:00", "MON", 3.0},
            {"CS102", "Algorithms Lab", "BCSE25", "A", "LAB", "Dr. Johnson", "CR1003", "10:00-13:00", "MON", 1.5},
            {"CS201", "Database Systems", "BCSE24", "B", "THEORY", "Dr. Brown", "CR1003", "14:00-15:00", "TUE", 3.0},
            {"CS202", "Networks Lab", "BCSE24", "B", "LAB", "Dr. Davis", "CR1003", "15:00-18:00", "TUE", 1.5},
            {"CS301", "AI Fundamentals", "BCSE23", "A", "THEORY", "Dr. Wilson", "CR1003", "09:00-10:00", "WED", 3.0},
            {"CS302", "ML Lab", "BCSE23", "A", "LAB", "Dr. Miller", "CR1003", "10:00-13:00", "WED", 1.5}
        };
        
        // Initialize academic PDF generator
        AcademicPDFGenerator generator;
        
        // Test the statistics generation functions directly
        std::cout << "📊 Testing generateStatistics function..." << std::endl;
        std::string stats = generator.generateStatistics(mockCourses);
        std::cout << "✅ Statistics HTML generated successfully!" << std::endl;
        std::cout << "📋 Statistics should show: 8 sections, 6 faculty, 6 rooms" << std::endl;
        
        std::cout << "\n📊 Testing generateAllBatchesStatistics function..." << std::endl;
        std::string allStats = generator.generateAllBatchesStatistics(mockCourses);
        std::cout << "✅ All batches statistics HTML generated successfully!" << std::endl;
        std::cout << "📋 Should show: 4 batches, 8 sections, 6 faculty, 6 rooms" << std::endl;
        
        // Generate a complete HTML file for manual verification
        std::string outputPath = "output/test_statistics_verification";
        bool success = generator.generateAcademicScheduleHTML(
            mockCourses,
            outputPath + ".html",
            "graph-coloring",
            "2024-25",
            "Spring"
        );
        
        if (success) {
            std::cout << "\n✅ Complete HTML file generated: " << outputPath << ".html" << std::endl;
            std::cout << "🔍 Please check the HTML file to verify the updated statistics:" << std::endl;
            std::cout << "   - Sections: 8 (fixed value)" << std::endl;
            std::cout << "   - Faculty: 6 (fixed value)" << std::endl;
            std::cout << "   - Rooms: 6 (fixed value)" << std::endl;
            std::cout << "   - Total Classes: " << mockCourses.size() << " (dynamic value)" << std::endl;
        } else {
            std::cerr << "❌ HTML generation failed!" << std::endl;
            return 1;
        }
        
    } catch (const std::exception& e) {
        std::cerr << "❌ Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
