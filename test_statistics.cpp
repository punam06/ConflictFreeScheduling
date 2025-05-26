#include <iostream>
#include <memory>
#include "src/database/database_manager.h"
#include "src/utils/academic_pdf_generator.h"

int main() {
    try {
        std::cout << "🧪 Testing updated statistics in PDF generation..." << std::endl;
        
        // Initialize database manager
        auto dbManager = std::make_shared<DatabaseManager>("scheduling.db");
        
        // Initialize academic PDF generator
        AcademicPDFGenerator generator(dbManager);
        
        // Generate a single batch schedule to test statistics  
        std::string outputPath = "output/test_updated_statistics";
        bool success = generator.generateScheduleFromDatabase(
            "BCSE25",
            "A", 
            outputPath,
            "graph-coloring", 
            "2024-25", 
            "Spring"
        );
        
        if (success) {
            std::cout << "✅ PDF generation with updated statistics completed!" << std::endl;
            std::cout << "📄 Check the PDF for the following updated values:" << std::endl;
            std::cout << "   - Batches: 4" << std::endl;
            std::cout << "   - Sections: 8" << std::endl;
            std::cout << "   - Faculty: 6" << std::endl;
            std::cout << "   - Rooms: 6" << std::endl;
        } else {
            std::cerr << "❌ PDF generation failed!" << std::endl;
            return 1;
        }
        
    } catch (const std::exception& e) {
        std::cerr << "❌ Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
