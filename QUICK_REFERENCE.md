# 🚀 Quick Reference Guide - Conflict-Free Scheduling

## Essential Commands

### 🔥 Most Common Usage
```bash
# Create your course file
echo "Course Name,Start,End,Students" > my_courses.txt
echo "Data Structures,9,11,50" >> my_courses.txt
echo "Algorithms,10,12,45" >> my_courses.txt

# Generate PDF schedule
./bin/scheduler --input my_courses.txt --algorithm dynamic-prog --pdf --no-database
```

### 📊 Compare All Algorithms
```bash
./bin/scheduler --input my_courses.txt --run-all --visualize --no-database
```

### 🎯 Algorithm Quick Select

| Need | Use | Command |
|------|-----|---------|
| **Schedule ALL courses** | Graph Coloring | `--algorithm graph-coloring` |
| **Maximum students served** | Dynamic Programming | `--algorithm dynamic-prog` |
| **Perfect optimization** | Backtracking | `--algorithm backtracking` |
| **Large/complex schedules** | Genetic Algorithm | `--algorithm genetic` |

## Input File Format
```csv
# Comments start with #
Course Name,Start Time,End Time,Students
Data Structures,9,11,50
Algorithms,10,12,45
Database Systems,13,15,40
```

## Essential Flags
- `--pdf` → Generate PDF output
- `--visualize` → Show timeline
- `--no-database` → Use file input only
- `--run-all` → Compare all algorithms
- `--help` → Show full help

## Troubleshooting
```bash
# Build issues
make clean && make

# File format issues
cat your_file.txt  # Check format

# Test with simple example
echo "Test,9,10,20" > test.txt
./bin/scheduler --input test.txt --no-database
```

## Example Results
```
Input: 10 courses with conflicts
├── Graph Coloring: 10/10 scheduled (all courses)
├── Dynamic Programming: 4/10 scheduled (optimal students)
├── Backtracking: 4/10 scheduled (optimal)
└── Genetic Algorithm: 4/10 scheduled (evolutionary)
```

**📱 PDF Output**: Professional university-branded schedules ready for printing!

---
For detailed guide: See `USER_GUIDE.md` | For help: `./bin/scheduler --help`
