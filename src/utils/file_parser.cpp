#include "file_parser.h"
#include <iostream>
#include <algorithm>

std::vector<Activity> FileParser::parseSimpleFormat(const std::string& filename) {
    std::vector<Activity> activities;
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        return activities;
    }
    
    std::string line;
    int id = 1;
    
    while (std::getline(file, line)) {
        line = trim(line);
        
        // Skip empty lines and comments
        if (line.empty() || line[0] == '#') {
            continue;
        }
        
        auto parts = split(line, ',');
        if (parts.size() >= 4) {
            try {
                std::string courseName = trim(parts[0]);
                int startTime = std::stoi(trim(parts[1]));
                int endTime = std::stoi(trim(parts[2]));
                double students = std::stod(trim(parts[3]));
                
                activities.push_back({id++, startTime, endTime, students});
            } catch (const std::exception& e) {
                std::cerr << "Error parsing line: " << line << std::endl;
            }
        }
    }
    
    file.close();
    std::cout << "Loaded " << activities.size() << " courses from " << filename << std::endl;
    return activities;
}

std::pair<std::vector<Activity>, std::vector<std::string>> FileParser::parseCSVFormat(const std::string& filename) {
    std::vector<Activity> activities;
    std::vector<std::string> courseNames;
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        return {activities, courseNames};
    }
    
    std::string line;
    int id = 1;
    bool firstLine = true;
    
    while (std::getline(file, line)) {
        line = trim(line);
        
        // Skip empty lines and comments
        if (line.empty() || line[0] == '#') {
            continue;
        }
        
        // Skip header line if it contains "Course" or "Name"
        if (firstLine && (line.find("Course") != std::string::npos || 
                         line.find("Name") != std::string::npos)) {
            firstLine = false;
            continue;
        }
        firstLine = false;
        
        auto parts = split(line, ',');
        if (parts.size() >= 4) {
            try {
                std::string courseName = trim(parts[0]);
                int startTime = std::stoi(trim(parts[1]));
                int endTime = std::stoi(trim(parts[2]));
                double students = std::stod(trim(parts[3]));
                
                activities.push_back({id++, startTime, endTime, students});
                courseNames.push_back(courseName);
            } catch (const std::exception& e) {
                std::cerr << "Error parsing line: " << line << std::endl;
            }
        }
    }
    
    file.close();
    std::cout << "Loaded " << activities.size() << " courses from " << filename << std::endl;
    return {activities, courseNames};
}

std::string FileParser::trim(const std::string& str) {
    size_t start = str.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) {
        return "";
    }
    size_t end = str.find_last_not_of(" \t\r\n");
    return str.substr(start, end - start + 1);
}

std::vector<std::string> FileParser::split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    
    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    
    return tokens;
}
