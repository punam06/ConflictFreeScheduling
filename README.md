# Conflict-Free Class Scheduling System

An academic project implementing conflict-free scheduling algorithms specifically designed for CSE department class scheduling and resource allocation optimization.

## 📋 Table of Contents

- [Overview](#overview)
- [Academic Context](#academic-context)
- [Features](#features)
- [Algorithm Details](#algorithm-details)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Performance Analysis](#performance-analysis)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [License](#license)

## 🚀 Current Status

**Project Status: COMPLETE - ENHANCED** ✅

All 4 core algorithms are fully implemented, tested, and operational. Plus new enhancements!

✅ **Graph Coloring Algorithm** - Fixed conflict resolution bug, working perfectly  
✅ **Dynamic Programming Algorithm** - Complete implementation with optimal weighted activity selection  
✅ **Backtracking Algorithm** - Exhaustive search with pruning  
✅ **Genetic Algorithm** - Population-based evolutionary optimization  
✅ **Enhanced Routine Generator** - NEW! Comprehensive schedule optimizer with PDF output

✅ **PDF Generation** - Fixed path handling and added automatic directory creation
✅ **Comprehensive Routine** - Full departmental schedule with all courses and sections
✅ **Test Suite** - 100% test coverage with comprehensive algorithm validation  
✅ **Performance Benchmarking** - Execution timing for all algorithms  
✅ **CLI Interface** - Full command-line functionality with visualization  
✅ **Build System** - Complete Makefile with test targets  

### Recent Achievements
- Fixed Graph Coloring conflict resolution bug
- Implemented complete Dynamic Programming algorithm  
- Added performance benchmarking with microsecond precision
- Enhanced visualization with timeline display
- Achieved 100% test pass rate across all algorithms


This project implements various algorithms for solving conflict-free scheduling problems, with a primary focus on **academic class scheduling for the CSE (Computer Science and Engineering) department**. The algorithms ensure optimal allocation of classroom resources, time slots, and faculty assignments while avoiding scheduling conflicts.

## 🎓 Academic Context

This project addresses real-world academic scheduling challenges:

- **Course Scheduling**: Optimal time slot allocation for CSE courses
- **Classroom Management**: Efficient room assignment avoiding conflicts  
- **Faculty Scheduling**: Professor availability and course assignments
- **Resource Optimization**: Maximizing utilization of limited academic resources

### Problem Statement

Given a set of academic activities (courses, labs, exams) with specific time constraints and resource requirements, the goal is to create an optimal schedule that:

1. **Minimizes conflicts** between courses and resources
2. **Maximizes resource utilization** (classrooms, labs, faculty time)
3. **Accommodates constraints** like faculty availability and student prerequisites
4. **Optimizes student experience** by reducing scheduling conflicts

### Real-World Applications

- **University Course Scheduling**: CSE department class timetables
- **Resource Management**: Classroom and lab allocation
- **Exam Scheduling**: Conflict-free examination timetables  
- **Faculty Management**: Teaching load distribution
- **Student Optimization**: Minimizing schedule conflicts for students

## ✨ Features

- **Multiple Algorithm Implementations**
  - Greedy Algorithm (Activity Selection)
  - Dynamic Programming Approach
  - Branch and Bound Method
  - Heuristic Solutions

- **Database Integration**
  - SQLite support for lightweight deployment
  - PostgreSQL ready for production scaling
  - Persistent data storage and retrieval
  - Conflict logging and resolution tracking
  - Schedule analytics and reporting

- **Comprehensive Analysis**
  - Time complexity analysis
  - Space complexity evaluation
  - Performance benchmarking
  - Comparative studies

- **Flexible Input Handling**
  - Database-driven course management
  - CSV file import/export
  - Real-time data processing
  - Batch processing capabilities

- **Visualization Tools**
  - Schedule visualization
  - Algorithm performance graphs
  - Conflict detection displays
  - Database statistics dashboard

- **Professional PDF Output**
  - Automatic HTML-to-PDF conversion using Chrome
  - University-branded schedule layouts
  - Timeline visualization with color coding
  - Cross-platform browser opening for PDF generation
  - Professional quality suitable for institutional use

## 🗄️ Database Features

- **SQLite Integration**: Lightweight, serverless database perfect for development and small deployments
- **PostgreSQL Support**: Production-ready database for large-scale academic institutions
- **Data Models**: Comprehensive schema for courses, rooms, time slots, and scheduling assignments
- **Conflict Management**: Automatic conflict detection and resolution logging
- **Analytics**: Built-in reporting for schedule utilization and performance metrics
- **Migration Support**: Database versioning and migration scripts

## 🧮 Algorithm Details

### Greedy Algorithm (Activity Selection)
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Approach**: Sort by finish time and select non-overlapping activities

### Dynamic Programming
- **Time Complexity**: O(n²)
- **Space Complexity**: O(n)
- **Approach**: Optimal substructure with memoization

### Branch and Bound
- **Time Complexity**: O(2ⁿ) worst case, better on average
- **Space Complexity**: O(n)
- **Approach**: Systematic enumeration with pruning

For detailed algorithm explanations, see [ALGORITHMS.md](./docs/ALGORITHMS.md).

## 🚀 Installation

### Prerequisites

```bash
# C++ Development Environment
g++ >= 9.0 (or clang++ >= 10.0)
cmake >= 3.16
make

# Optional dependencies for visualization
gnuplot (for generating performance graphs)
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ConflictFreeScheduling.git
cd ConflictFreeScheduling

# Build the project
mkdir build && cd build
cmake ..
make

# Run the executable
./scheduler
```

## 💻 Usage

### Basic Example

```cpp
// C++ example
#include "scheduler.h"
#include <vector>
#include <iostream>

int main() {
    // Define tasks with start and end times
    std::vector<Task> tasks = {
        {1, 1, 4},  // id, start, end
        {2, 3, 5},
        {3, 0, 6},
        {4, 5, 7},
        {5, 8, 9}
    };

    // Initialize scheduler
    ConflictFreeScheduler scheduler;

    // Find optimal schedule
    std::vector<Task> optimalSchedule = scheduler.greedySchedule(tasks);
    
    std::cout << "Scheduled tasks: ";
    for (const auto& task : optimalSchedule) {
        std::cout << task.id << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
```

### Command Line Interface

```bash
# Build first
make clean && make

# Generate schedule with automatic PDF download
./bin/scheduler --input data/sample_courses.txt --algorithm dynamic-prog --pdf --no-database

# Compare multiple algorithms  
./bin/scheduler --run-all --input data/sample_courses.txt --no-database

# Generate PDF with custom input
./bin/scheduler --input my_courses.txt --algorithm genetic --pdf --no-database

# Show help
./bin/scheduler --help
```

### 📥 **PDF Download Process**
1. **Run command** with `--pdf` flag
2. **HTML generated** automatically (e.g., `dynamic-prog.html`)
3. **PDF created** automatically (e.g., `dynamic-prog.pdf`) 
4. **File opens** in browser/PDF viewer
5. **Download complete** - PDF ready for sharing!

**Quick Example:**
```bash
./bin/scheduler --input data/sample_courses.txt --algorithm backtracking --pdf --no-database
# ✅ Output: backtracking.pdf (229 KB, professional quality)
```

## 📊 Examples

### Example 1: Meeting Room Scheduling

```
Input:
Meeting 1: 9:00 AM - 10:30 AM
Meeting 2: 10:00 AM - 11:00 AM
Meeting 3: 11:00 AM - 12:00 PM
Meeting 4: 1:00 PM - 2:00 PM

Output:
Selected: Meeting 1, Meeting 3, Meeting 4
Total meetings scheduled: 3
```

### Example 2: CPU Process Scheduling

```
Input:
Process A: [0, 3]
Process B: [1, 4]
Process C: [2, 6]
Process D: [5, 7]

Output:
Optimal Schedule: A → D
CPU Utilization: 5/7 ≈ 71.4%
```

For more examples, see [EXAMPLES.md](./docs/EXAMPLES.md).

## 📈 Performance Analysis

| Algorithm | Time Complexity | Space Complexity | Optimality | Use Case |
|-----------|----------------|------------------|------------|----------|
| Greedy | O(n log n) | O(1) | Optimal for activity selection | Large datasets |
| Dynamic Programming | O(n²) | O(n) | Optimal | Weighted scheduling |
| Branch & Bound | O(2ⁿ) | O(n) | Optimal | Small to medium datasets |

For detailed performance analysis, see [PERFORMANCE.md](./docs/PERFORMANCE.md).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./docs/CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `make test`
5. Submit a pull request

## 📚 Documentation

- **[📖 Complete User Guide](USER_GUIDE.md)** - Comprehensive documentation with examples
- **[🚀 Quick Reference](QUICK_REFERENCE.md)** - Essential commands and usage patterns  
- **[📥 PDF Download Guide](PDF_DOWNLOAD_GUIDE.md)** - Complete PDF generation and download instructions
- **[📄 Input to PDF Summary](SIMPLE_INPUT_TO_PDF_SUMMARY.md)** - New features overview

### Technical Documentation
- **[🔧 Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical details and architecture
- **[📊 Performance Analysis](docs/PERFORMANCE.md)** - Algorithm benchmarks and comparisons
- **[🧪 Testing Guide](docs/TESTING.md)** - Test suite and validation procedures

### Quick Usage
```bash
# Create course schedule from text file
echo "Data Structures,9,11,50
Algorithms,10,12,45" > courses.txt

# Generate professional PDF schedule
./bin/scheduler --input courses.txt --algorithm dynamic-prog --pdf --no-database
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Course: Algorithm Analysis and Design
- Semester: 2-2
- Academic Year: 2024-2025
- Institution: [Bangladesh University of Professionals]

## 📞 Contact

- **Author**: [Umme Hani Punam] [Rebeka Sultana Orce]
- **Email**: [ummehanipunam8@gmail.com]
- **Project Link**: [https://github.com/yourusername/ConflictFreeScheduling](https://github.com/yourusername/ConflictFreeScheduling)

---

**Note**: This project is part of an academic assignment for Algorithm Analysis and Design course. The implementations focus on understanding algorithmic concepts and their practical applications
