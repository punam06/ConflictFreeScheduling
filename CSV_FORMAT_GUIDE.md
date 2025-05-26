# CSV Input Format for Enhanced Routine Generator

## Updated Format (Teacher Names)

The Enhanced Routine Generator now uses teacher names instead of student counts in the CSV input format.

### New Format:
```
Course Name,Start Time,End Time,Teacher Name
```

### Example:
```
Data Structures,9,11,Dr. Ahmed Rahman
Algorithms,10,12,Prof. Sarah Khan
Database Systems,13,15,Dr. Mohammad Ali
Computer Networks,14,16,Ms. Fatima Sheikh
Software Engineering,16,18,Dr. Hassan Ahmed
Operating Systems,11,13,Prof. Nadia Alam
Machine Learning,15,17,Dr. Tariq Mahmud
```

### Usage:
```bash
# Generate PDF with custom CSV data
./build/scheduler --input data/your_courses.csv --no-database --pdf

# Use with different algorithms
./build/scheduler --input data/your_courses.csv --no-database --algorithm dynamic-prog --pdf
```

### Features:
- **Teacher Names**: Display teacher names instead of student counts
- **PDF Generation**: Automatically generates professional PDFs
- **Multiple Algorithms**: Support for graph-coloring, dynamic-prog, backtracking, and genetic algorithms
- **Timeline View**: Visual timeline showing when each teacher is scheduled
- **Statistics**: Shows total courses and teachers involved

### Sample Files:
- `data/courses_with_teachers.csv` - Simple 7-course example
- `data/comprehensive_courses.csv` - Comprehensive 15-course example

The system automatically uses weight=1.0 for all courses, focusing on conflict resolution rather than capacity optimization.
