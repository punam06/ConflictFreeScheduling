#ifndef FILE_PARSER_H
#define FILE_PARSER_H

#include "../scheduler.h"
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <tuple>

/**
 * @brief Simple file parser for course input
 */
class FileParser {
public:
    /**
     * @brief Parse course data from a simple text file
     * @param filename Path to the input file
     * @return Vector of Activity objects
     */
    static std::vector<Activity> parseSimpleFormat(const std::string& filename);
    
    /**
     * @brief Parse course data from CSV format
     * @param filename Path to the CSV file
     * @return Tuple of Activity objects, course names, and teacher names
     */
    static std::tuple<std::vector<Activity>, std::vector<std::string>, std::vector<std::string>> parseCSVFormat(const std::string& filename);
    
private:
    /**
     * @brief Remove leading and trailing whitespace
     */
    static std::string trim(const std::string& str);
    
    /**
     * @brief Split string by delimiter
     */
    static std::vector<std::string> split(const std::string& str, char delimiter);
};

#endif // FILE_PARSER_H
