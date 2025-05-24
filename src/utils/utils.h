#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>
#include <sstream>

/**
 * @brief Utility functions for the scheduling system
 */
namespace Utils {
    /**
     * @brief Convert time from 24-hour format to minutes since midnight
     * @param timeStr Time string in format "HH:MM"
     * @return Minutes since midnight
     */
    inline int convertTimeToMinutes(const std::string& timeStr) {
        int hours = std::stoi(timeStr.substr(0, 2));
        int minutes = std::stoi(timeStr.substr(3, 2));
        return hours * 60 + minutes;
    }
    
    /**
     * @brief Convert minutes since midnight to 24-hour time format
     * @param minutes Minutes since midnight
     * @return Time string in format "HH:MM"
     */
    inline std::string convertMinutesToTime(int minutes) {
        int hours = minutes / 60;
        int mins = minutes % 60;
        
        std::string hoursStr = (hours < 10) ? "0" + std::to_string(hours) : std::to_string(hours);
        std::string minsStr = (mins < 10) ? "0" + std::to_string(mins) : std::to_string(mins);
        
        return hoursStr + ":" + minsStr;
    }
    
    /**
     * @brief Calculate the duration between two time points in minutes
     * @param startTime Start time in minutes since midnight
     * @param endTime End time in minutes since midnight
     * @return Duration in minutes
     */
    inline int calculateDuration(int startTime, int endTime) {
        return endTime - startTime;
    }
    
    /**
     * @brief Split a string by delimiter
     * @param s String to split
     * @param delimiter Delimiter character
     * @return Vector of split strings
     */
    inline std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }
    
    /**
     * @brief Calculate the day of week from a date string
     * @param dateStr Date string in format "YYYY-MM-DD"
     * @return Day of week (0 = Sunday, ..., 6 = Saturday)
     */
    inline int calculateDayOfWeek(const std::string& dateStr) {
        // Simple placeholder - would need actual calendar calculation
        // in a production system
        return 1; // Monday
    }
}

#endif // UTILS_H
