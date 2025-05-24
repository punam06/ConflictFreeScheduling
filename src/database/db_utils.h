#ifndef DB_UTILS_H
#define DB_UTILS_H

#include <string>
#include <vector>
#include <map>

/**
 * @brief Database utility functions for Conflict-Free Scheduling System
 */
namespace DBUtils {
    
    /**
     * @brief Configuration parser for database settings
     */
    class ConfigParser {
    private:
        std::map<std::string, std::map<std::string, std::string>> config_data;
        
    public:
        bool loadFromFile(const std::string& config_file);
        std::string getString(const std::string& section, const std::string& key, const std::string& default_value = "");
        int getInt(const std::string& section, const std::string& key, int default_value = 0);
        bool getBool(const std::string& section, const std::string& key, bool default_value = false);
    };
    
    /**
     * @brief Database connection string builder
     */
    class ConnectionBuilder {
    public:
        static std::string buildSQLiteConnection(const std::string& db_file);
        static std::string buildPostgreSQLConnection(const std::string& host, int port, 
                                                    const std::string& database, 
                                                    const std::string& username, 
                                                    const std::string& password);
        static std::string buildMySQLConnection(const std::string& host, int port,
                                              const std::string& database,
                                              const std::string& username,
                                              const std::string& password);
    };
    
    /**
     * @brief SQL query builders for common operations
     */
    class QueryBuilder {
    public:
        static std::string buildInsertQuery(const std::string& table, const std::vector<std::string>& columns);
        static std::string buildUpdateQuery(const std::string& table, const std::vector<std::string>& columns, const std::string& where_clause);
        static std::string buildSelectQuery(const std::string& table, const std::vector<std::string>& columns, const std::string& where_clause = "");
        static std::string buildDeleteQuery(const std::string& table, const std::string& where_clause);
    };
    
    /**
     * @brief Database migration utilities
     */
    class Migration {
    public:
        static bool createBackup(const std::string& source_db, const std::string& backup_path);
        static bool executeMigrationScript(const std::string& db_path, const std::string& script_path);
        static std::vector<std::string> getAvailableMigrations(const std::string& migrations_dir);
        static bool checkSchemaVersion(const std::string& db_path);
    };
    
    /**
     * @brief Data validation utilities
     */
    class Validator {
    public:
        static bool isValidEmail(const std::string& email);
        static bool isValidTimeFormat(const std::string& time_str);
        static bool isValidDateFormat(const std::string& date_str);
        static bool isValidRoomCode(const std::string& room_code);
        static bool isValidCourseCode(const std::string& course_code);
    };
    
    /**
     * @brief Performance monitoring utilities
     */
    class PerformanceMonitor {
    private:
        static std::map<std::string, double> query_times;
        
    public:
        static void startQuery(const std::string& query_name);
        static void endQuery(const std::string& query_name);
        static double getAverageQueryTime(const std::string& query_name);
        static void logSlowQueries(double threshold_ms);
        static void resetStatistics();
    };
}

#endif // DB_UTILS_H
