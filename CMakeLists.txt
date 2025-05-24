cmake_minimum_required(VERSION 3.16)
project(ConflictFreeScheduling VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Include directories
include_directories(src)
include_directories(src/algorithms)
include_directories(src/utils)
include_directories(src/database)

# Find packages
find_package(PkgConfig REQUIRED)
pkg_check_modules(SQLITE3 REQUIRED sqlite3)

# Optional: PostgreSQL support
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(POSTGRESQL libpq)
endif()

# Find source files
file(GLOB_RECURSE SOURCES 
    "src/*.cpp"
    "src/algorithms/*.cpp"
    "src/utils/*.cpp"
    "src/database/*.cpp"
)

file(GLOB_RECURSE HEADERS
    "src/*.h"
    "src/algorithms/*.h"
    "src/utils/*.h"
    "src/database/*.h"
)

# Create main executable
add_executable(scheduler ${SOURCES} ${HEADERS})

# Link SQLite3 library
target_link_libraries(scheduler ${SQLITE3_LIBRARIES})
target_include_directories(scheduler PRIVATE ${SQLITE3_INCLUDE_DIRS})
target_compile_options(scheduler PRIVATE ${SQLITE3_CFLAGS_OTHER})

# Link PostgreSQL if available
if(POSTGRESQL_FOUND)
    target_link_libraries(scheduler ${POSTGRESQL_LIBRARIES})
    target_include_directories(scheduler PRIVATE ${POSTGRESQL_INCLUDE_DIRS})
    target_compile_definitions(scheduler PRIVATE POSTGRESQL_SUPPORT)
endif()

# Optional: Enable testing
option(BUILD_TESTS "Build test programs" ON)

if(BUILD_TESTS)
    enable_testing()
    
    # Find test source files
    file(GLOB_RECURSE TEST_SOURCES 
        "tests/*.cpp"
        "tests/test_algorithms/*.cpp"
        "tests/test_utils/*.cpp"
    )
    
    # Create test executable
    add_executable(run_tests ${TEST_SOURCES} ${SOURCES})
    
    # Link libraries for tests
    target_link_libraries(run_tests ${SQLITE3_LIBRARIES})
    target_include_directories(run_tests PRIVATE ${SQLITE3_INCLUDE_DIRS})
    
    # Remove main.cpp from test build to avoid multiple main functions
    list(FILTER SOURCES EXCLUDE REGEX ".*main\\.cpp$")
    
    add_test(NAME ConflictFreeSchedulingTests COMMAND run_tests)
endif()

# Installation
install(TARGETS scheduler DESTINATION bin)

# Documentation
find_package(Doxygen)
if(DOXYGEN_FOUND)
    set(DOXYGEN_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/docs)
    doxygen_add_docs(docs ${CMAKE_CURRENT_SOURCE_DIR}/src)
endif()

# Print build information
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ flags: ${CMAKE_CXX_FLAGS}")
