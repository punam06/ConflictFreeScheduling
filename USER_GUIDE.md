# 📚 Conflict-Free Class Scheduling System - Complete User Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Input File Formats](#input-file-formats)
5. [Command Line Interface](#command-line-interface)
6. [Algorithms Explained](#algorithms-explained)
7. [Output Options](#output-options)
8. [Database Integration](#database-integration)
9. [Enhanced Routine Generator](#enhanced-routine-generator)
10. [Examples & Use Cases](#examples--use-cases)
11. [Troubleshooting](#troubleshooting)
12. [Advanced Features](#advanced-features)

---

## Overview

The **Conflict-Free Class Scheduling System** is a comprehensive tool designed for academic institutions to automatically generate optimal class schedules. It implements four different algorithmic approaches to solve scheduling conflicts and provides multiple output formats including professional PDF documents.

### Key Features
- ✅ **4 Core Algorithms**: Graph Coloring, Dynamic Programming, Backtracking, Genetic Algorithm
- ✅ **Enhanced Routine Generator**: Specialized for BUP CSE Department scheduling
- ✅ **Simple Text Input**: CSV and plain text file support
- ✅ **Professional PDF Output**: University-branded, printable schedules
- ✅ **Database Integration**: SQLite support for large-scale scheduling
- ✅ **Performance Analysis**: Algorithm comparison and benchmarking
- ✅ **Cross-Platform**: Works on macOS, Windows, and Linux

---

## Installation

### Prerequisites
```bash
# macOS
brew install sqlite3

# Ubuntu/Debian
sudo apt-get install libsqlite3-dev

# CentOS/RHEL
sudo yum install sqlite-devel
```

### Build from Source
```bash
# Clone the repository
git clone https://github.com/punam06/ConflictFreeScheduling.git
cd ConflictFreeScheduling

# Build the project
make clean
make

# Verify installation
./bin/scheduler --help
```

### Alternative: CMake Build
```bash
mkdir build && cd build
cmake ..
make
```

---

## Quick Start

### 1. Basic Usage with Built-in Data
```bash
# Run with default algorithm (Graph Coloring)
./bin/scheduler

# Compare all 4 algorithms
./bin/scheduler --run-all --visualize
```

### 2. Using Input Files
```bash
# Create a simple course file
echo "Data Structures,9,11,50
Algorithms,10,12,45
Database Systems,13,15,40" > my_courses.txt

# Run scheduling with PDF output
./bin/scheduler --input my_courses.txt --algorithm dynamic-prog --pdf --no-database
```

### 3. With Database Integration
```bash
# Initialize database with sample data
./bin/scheduler --init-db

# Run scheduling using database
./bin/scheduler --algorithm graph-coloring --visualize
```

---

## Input File Formats

### CSV Format (Recommended)
```csv
# Course scheduling input file
# Format: Course Name, Start Time, End Time, Students

Data Structures,9,11,50
Algorithms,10,12,45
Database Systems,13,15,40
Computer Networks,14,16,35
Software Engineering,16,18,30
Operating Systems,11,13,25
Machine Learning,15,17,20
```

### Key Rules:
- **Time Format**: 24-hour format (9 = 9:00 AM, 14 = 2:00 PM)
- **Comments**: Lines starting with `#` are ignored
- **Empty Lines**: Automatically skipped
- **Students**: Number of students (used as weight for optimization)

### Simple Format Example
```
Math 101,9,10,30
Physics 101,10,11,25
Chemistry 101,11,12,35
Biology 101,12,13,40
English 101,13,14,20
```

### Complex Schedule Example
```csv
# Computer Science Department Schedule
# Fall 2025 Semester

Programming Fundamentals,8,10,60
Data Structures and Algorithms,10,12,55
Object-Oriented Programming,13,15,50
Database Management Systems,14,16,45
Computer Networks,15,17,40
Operating Systems,9,11,42
Software Engineering,11,13,38
Web Development,16,18,35
Machine Learning,17,19,30
Mobile App Development,8,10,25
```

---

## Command Line Interface

### Core Options

| Option | Description | Example |
|--------|-------------|---------|
| `--algorithm <type>` | Choose specific algorithm | `--algorithm dynamic-prog` |
| `--run-all` | Run all 4 algorithms and compare | `--run-all` |
| `--input <file>` | Input file with course data | `--input courses.txt` |
| `--output <file>` | Save results to file | `--output schedule.txt` |
| `--pdf` | Generate PDF output | `--pdf` |
| `--visualize` | Show timeline visualization | `--visualize` |
| `--no-database` | Disable database, use file input only | `--no-database` |
| `--init-db` | Initialize database with sample data | `--init-db` |
| `--help, -h` | Show help message | `--help` |

### Command Line Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-h`, `--help` | Show help message | `./bin/scheduler --help` |
| `--input <file>` | Specify input file | `./bin/scheduler --input data/sample.txt` |
| `--output <file>` | Specify output file | `./bin/scheduler --output results.txt` |
| `--algorithm <name>` | Choose algorithm | `./bin/scheduler --algorithm graph-coloring` |
| `--pdf` | Generate PDF output | `./bin/scheduler --output schedule --pdf` |
| `--visualize` | Create visual output | `./bin/scheduler --visualize` |
| `--init-db` | Initialize database | `./bin/scheduler --init-db` |
| `--no-database` | Skip database (use file) | `./bin/scheduler --no-database` |
| `--run-all` | Run and compare all algorithms | `./bin/scheduler --run-all` |
| `--enhanced-generator` | Use enhanced routine generator | `./bin/scheduler --enhanced-generator` |
| `--comprehensive-routine` | Create complete department schedule | `./bin/scheduler --enhanced-generator --comprehensive-routine` |
| `--batch <batch_name>` | Generate for specific batch | `./bin/scheduler --enhanced-generator --batch BCSE23` |

### Algorithm Types

| Algorithm | Flag | Best For |
|-----------|------|----------|
| Graph Coloring | `graph-coloring` | Scheduling all courses (may use multiple time slots) |
| Dynamic Programming | `dynamic-prog` | Optimal weighted selection (maximum students) |
| Backtracking | `backtracking` | Exhaustive optimal solutions |
| Genetic Algorithm | `genetic` | Complex constraints and large datasets |

---

## Algorithms Explained

### 1. Graph Coloring Algorithm
- **Purpose**: Models course conflicts as graph edges, assigns time slots as colors
- **Strength**: Can schedule ALL courses by using multiple time slots
- **Use Case**: When you need to schedule every course regardless of conflicts
- **Output**: Maximum courses scheduled, may use many time slots

```bash
./bin/scheduler --algorithm graph-coloring --visualize
```

### 2. Dynamic Programming Algorithm
- **Purpose**: Finds optimal weighted activity selection with maximum students
- **Strength**: Mathematically optimal solution for weight maximization
- **Use Case**: When maximizing total students served is priority
- **Output**: Fewer courses but maximum student coverage

```bash
./bin/scheduler --algorithm dynamic-prog --pdf
```

### 3. Backtracking Algorithm
- **Purpose**: Exhaustive search with pruning for optimal solutions
- **Strength**: Guarantees finding the best possible solution
- **Use Case**: Small to medium datasets requiring perfect optimization
- **Output**: Optimal solution with detailed search statistics

```bash
./bin/scheduler --algorithm backtracking --visualize
```

### 4. Genetic Algorithm
- **Purpose**: Population-based evolutionary optimization
- **Strength**: Handles complex constraints and large datasets
- **Use Case**: Large universities with complex scheduling requirements
- **Output**: Near-optimal solutions with evolution statistics

```bash
./bin/scheduler --algorithm genetic --visualize
```

---

## Output Options

### 1. Console Output
**Basic Information:**
- Input course summary table
- Algorithm execution time
- Scheduled activities list
- Statistics (utilization, students served)

### 2. Text File Output
```bash
./bin/scheduler --output results.txt
```
**Contains:**
- Algorithm name and parameters
- Complete scheduling results
- Performance metrics

### 3. Timeline Visualization
```bash
./bin/scheduler --visualize
```
**Shows:**
```
Time:  9 10 11 12 13 14 15 16 17 18
      =============================
C1:   ██ ██                         
C3:         ██ ██                   
C5:               ██ ██             
C7:                     ██ ██       
```

### 4. Professional PDF Output
```bash
./bin/scheduler --pdf
```
**Features:**
- University branding (BUP logo and colors)
- Professional layout for printing
- Timeline visualization with color coding
- Statistics dashboard
- Algorithm performance metrics
- Automatically opens in browser for PDF conversion

**PDF Contents:**
- Header with university branding
- Schedule overview table
- Visual timeline representation
- Algorithm performance statistics
- Course conflict analysis
- Utilization metrics

---

## Database Integration

### Initialize Database
```bash
# Create database with sample data
./bin/scheduler --init-db

# Check database statistics
./bin/scheduler --algorithm graph-coloring
```

### Database vs File Input Priority
1. **`--input file.txt`** → File input (highest priority)
2. **Database enabled** → Load from SQLite database
3. **`--no-database`** → Use built-in sample data

### Database Schema
The system uses SQLite with tables for:
- **Courses**: Course information and constraints
- **Rooms**: Available classrooms and capacity
- **Time Slots**: Available time periods
- **Schedule Assignments**: Final scheduling results
- **Conflicts**: Conflict detection and resolution logs

---

## Enhanced Routine Generator

The **Enhanced Routine Generator** is a specialized scheduling module designed specifically for the Bangladesh University of Professionals (BUP) Computer Science and Engineering Department. It provides comprehensive scheduling capabilities with academic-focused constraints and outputs.

### Key Capabilities

- **Department-Specific Design**: Optimized for BUP CSE Department structure and requirements
- **Multi-Batch Handling**: Manages scheduling for 4 batches simultaneously (BCSE22, BCSE23, BCSE24, BCSE25)
- **Room Resource Allocation**: Efficiently assigns 5 different classrooms (CR302, CR303, CR304, CR504, CR1003)
- **Academic Time Slot Management**: Handles standard academic hours (8:30 AM - 5:00 PM) with lunch break considerations
- **Course Credit Handling**: Supports different credit structures:
  - Theory: 1.5 hours (2 sessions/week, 3.0 credit)
  - Labs: 3 hours (1 session/week, 1.5 credit) or (1 session/2 weeks, 0.75 credit)

### Using the Enhanced Generator

#### Basic Usage

```bash
# Navigate to build directory
cd build

# Run enhanced generator
./scheduler --enhanced-generator

# Generate comprehensive routine PDF
./scheduler --enhanced-generator --comprehensive-routine
```

#### Batch-Specific Scheduling

```bash
# Generate schedule for a specific batch
./scheduler --enhanced-generator --batch BCSE23

# Generate comprehensive routine with custom output path
./scheduler --enhanced-generator --comprehensive-routine --output custom_path/routine
```

#### Convenience Script

A convenience script is provided to quickly generate comprehensive routines:

```bash
# Run from project root
./scripts/run_enhanced_generator.sh

# View the generated PDF
open output/enhanced_schedule_comprehensive_routine.pdf
```

### Comprehensive Routine Generation

The comprehensive routine feature generates a complete departmental schedule in both HTML and PDF formats. This schedule includes:

- Day-wise scheduling (Sunday through Thursday)
- All batches in a single view
- Color-coding for different course types
- Room allocations
- Faculty assignments
- Time slot visualizations

#### Sample Command

```bash
# Initialize fresh database and generate comprehensive routine
./build/scheduler --init-db
./build/scheduler --enhanced-generator --comprehensive-routine --output output/enhanced_schedule
```

### Output Files

The enhanced generator produces two main output types:

1. **HTML Output**: `enhanced_schedule_comprehensive_routine.html`
   - Interactive format viewable in any browser
   - Contains all scheduling data in tabular format
   - Includes CSS styling for visual clarity

2. **PDF Output**: `enhanced_schedule_comprehensive_routine.pdf`
   - Professional print-ready format
   - Preserves all styling and layout from HTML
   - Suitable for official department distribution
   
Both files are created in the specified output directory (defaults to `output/` in the project root).

---

## Examples & Use Cases

### Example 1: Computer Science Department
```bash
# Create CS department schedule
cat > cs_schedule.txt << EOF
Programming I,8,10,75
Programming II,10,12,65
Data Structures,9,11,60
Algorithms,11,13,55
Database Systems,13,15,50
Computer Networks,14,16,45
Operating Systems,15,17,40
Software Engineering,16,18,35
EOF

# Generate schedule with all algorithms
./bin/scheduler --input cs_schedule.txt --run-all --pdf --visualize --no-database
```

### Example 2: Medical School Schedule
```bash
# Create medical courses file
cat > medical_schedule.txt << EOF
Anatomy,8,11,120
Physiology,9,12,110
Biochemistry,13,15,100
Pharmacology,14,16,90
Pathology,15,17,85
Microbiology,16,18,80
EOF

# Find optimal schedule for maximum students
./bin/scheduler --input medical_schedule.txt --algorithm dynamic-prog --pdf --no-database
```

### Example 3: Engineering Department
```bash
# Large engineering schedule
cat > engineering_schedule.txt << EOF
Mathematics I,8,10,80
Physics I,9,11,75
Chemistry,10,12,70
Engineering Drawing,11,13,65
Programming,13,15,60
Electronics,14,16,55
Mechanics,15,17,50
Thermodynamics,16,18,45
Materials Science,8,10,40
Control Systems,17,19,35
EOF

# Compare all algorithms
./bin/scheduler --input engineering_schedule.txt --run-all --visualize --output comparison.txt --no-database
```

### Example 4: Small College
```bash
# Simple schedule with no conflicts
cat > simple_schedule.txt << EOF
English 101,9,10,30
Math 101,10,11,35
History 101,11,12,25
Science 101,12,13,40
Art 101,13,14,20
EOF

# Should schedule all courses
./bin/scheduler --input simple_schedule.txt --algorithm graph-coloring --pdf --visualize --no-database
```

---

## Troubleshooting

### Common Issues

#### 1. Build Errors
```bash
# Missing SQLite
# macOS:
brew install sqlite3

# Ubuntu:
sudo apt-get install libsqlite3-dev

# Clean and rebuild
make clean && make
```

#### 2. Input File Errors
```bash
# Check file format
cat your_file.txt

# Validate with simple example
echo "Test Course,9,10,20" > test.txt
./bin/scheduler --input test.txt --no-database
```

#### 3. PDF Generation Issues
- **Browser doesn't open**: PDF generation creates HTML file, manually open in browser
- **No styling**: Check if CSS is embedded in HTML file
- **Permission issues**: Ensure write permissions in project directory
- **"No schedule data available for conversion"**: Ensure the enhanced generator has completed successfully
- **"Cannot create HTML file"**: Check that the output directory exists; the system now automatically creates directories

```bash
# Manually create output directory if needed
mkdir -p output
chmod 755 output

# Run with explicit output path
./build/scheduler --enhanced-generator --comprehensive-routine --output $(pwd)/output/schedule
```

#### 4. Database Errors
```bash
# Reset database
rm data/scheduling.db
./bin/scheduler --init-db

# Use file input instead
./bin/scheduler --no-database --input your_file.txt
```

### Error Messages

| Error | Solution |
|-------|----------|
| "Failed to parse input file" | Check CSV format, ensure proper commas |
| "Database initialization failed" | Check SQLite installation, file permissions |
| "No activities loaded" | Verify input file exists and has valid format |
| "Algorithm execution failed" | Check for valid time ranges and course data |

---

## Advanced Features

### 1. Performance Benchmarking
```bash
# Compare algorithm performance
./bin/scheduler --run-all --input large_dataset.txt --output benchmark.txt
```

### 2. Custom Time Ranges
```bash
# Extended hours (6 AM to 10 PM)
cat > extended_schedule.txt << EOF
Early Morning Class,6,8,25
Regular Morning,8,10,50
Late Evening,20,22,30
EOF
```

### 3. Weighted Optimization
- **Student Count**: Used as weight for optimization algorithms
- **Higher student count** = **Higher priority** in Dynamic Programming
- **Graph Coloring**: Attempts to schedule high-enrollment courses first

### 4. Conflict Analysis
The system automatically detects and reports:
- **Time Overlap Conflicts**: Courses scheduled at same time
- **Resource Conflicts**: Multiple courses requiring same room
- **Constraint Violations**: Courses violating institutional rules

### 5. Algorithm Selection Guide

| Scenario | Recommended Algorithm | Reason |
|----------|----------------------|---------|
| Small department (< 10 courses) | **Backtracking** | Guarantees optimal solution |
| Medium department (10-50 courses) | **Dynamic Programming** | Fast and optimal for weighted selection |
| Large university (> 50 courses) | **Genetic Algorithm** | Handles complexity and constraints |
| Must schedule ALL courses | **Graph Coloring** | Only algorithm that schedules everything |
| Maximize student satisfaction | **Dynamic Programming** | Optimizes for highest enrollment courses |
| Complex constraints | **Genetic Algorithm** | Most flexible for custom requirements |

### 6. Output Customization
```bash
# Minimal output
./bin/scheduler --input file.txt --algorithm dp > results.txt 2>/dev/null

# Detailed analysis
./bin/scheduler --input file.txt --run-all --visualize --output detailed.txt

# PDF with specific filename
./bin/scheduler --input file.txt --pdf  # Creates algorithm-name.html
```

### 7. Integration with Other Systems
```bash
# Export for external systems
./bin/scheduler --input courses.txt --output schedule.csv

# Batch processing
for file in schedules/*.txt; do
    ./bin/scheduler --input "$file" --algorithm dynamic-prog --output "results/$(basename "$file" .txt)_schedule.txt"
done
```

---

## Best Practices

### 1. Input File Preparation
- ✅ Use descriptive course names
- ✅ Ensure accurate time ranges
- ✅ Include realistic student counts
- ✅ Add comments for documentation
- ❌ Avoid special characters in course names
- ❌ Don't use overlapping time ranges unless intended

### 2. Algorithm Selection
- **Start with `--run-all`** to compare all algorithms
- **Use Dynamic Programming** for most scheduling scenarios
- **Use Graph Coloring** when you must schedule every course
- **Use Genetic Algorithm** for large, complex schedules

### 3. Output Management
- **Always use `--pdf`** for presentation-quality schedules
- **Use `--visualize`** to quickly spot conflicts
- **Save results with `--output`** for record keeping
- **Use descriptive filenames** for multiple runs

### 4. Performance Optimization
- **Use `--no-database`** for faster execution with file input
- **Limit genetic algorithm generations** for large datasets
- **Process large schedules in smaller batches**

---

## Support & Contributing

### Getting Help
- 📖 **Documentation**: Check `/docs` folder for detailed guides
- 🐛 **Issues**: Report bugs on GitHub issues page
- 💡 **Features**: Suggest improvements via GitHub discussions
- 📧 **Contact**: Reach out to development team

### Contributing
- 🔧 **Code**: Submit pull requests for improvements
- 📝 **Documentation**: Help improve user guides
- 🧪 **Testing**: Add test cases for new features
- 🎨 **UI/UX**: Enhance PDF generation and visualization

---

## License & Citation

This project is licensed under the MIT License. If you use this system in academic work, please cite:

```bibtex
@software{ConflictFreeScheduling2025,
  title={Conflict-Free Class Scheduling System},
  author={Punam and Team},
  year={2025},
  url={https://github.com/punam06/ConflictFreeScheduling},
  version={2.0}
}
```

---

**🎓 Happy Scheduling! 🎓**

*For more information, visit the [GitHub repository](https://github.com/punam06/ConflictFreeScheduling) or check the `/docs` folder for additional documentation.*
