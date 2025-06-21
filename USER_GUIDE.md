# Conflict-Free Scheduling System - User Guide

This guide provides detailed instructions on how to install, configure, and use the Conflict-Free Scheduling System for academic class scheduling.

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Interactive Mode](#interactive-mode)
5. [Command Line Usage](#command-line-usage)
6. [Input Data Formats](#input-data-formats)
7. [Output Types](#output-types)
8. [Algorithm Selection](#algorithm-selection)
9. [Database Integration](#database-integration)
10. [Advanced Features](#advanced-features)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

## Overview

The Conflict-Free Scheduling System is designed to generate optimal academic schedules for educational institutions. It uses various algorithms to create non-conflicting timetables while considering factors like room availability, faculty constraints, and course priorities.

### Key Features
- Four distinct scheduling algorithms
- PDF generation (academic and basic formats)
- Database integration for storing course and schedule data
- Interactive and command-line interfaces
- Batch processing capabilities
- Visualization options

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL server (optional, for database features)
- pip (Python package manager)

### Steps

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd ConflictFreeSchedulingPython
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Alternatively, use the setup script:
   ```bash
   chmod +x run.sh
   ./run.sh install
   ```

3. **Database setup (optional)**
   - Create a MySQL database:
     ```bash
     mysql -u root -p
     CREATE DATABASE conflict_free_scheduling;
     exit
     ```
   - Initialize the database:
     ```bash
     ./run.sh database
     ```
     or
     ```bash
     python scripts/initialize_database.py --sample-data
     ```

## Quick Start

The fastest way to get started is to use the run script:

```bash
# Run with default settings (academic PDF output)
./run.sh basic

# Run all algorithms and compare
./run.sh all

# Generate professional academic PDF
./run.sh academic

# Run interactive demo
./run.sh demo
```

For a completely interactive experience, simply run:

```bash
python main.py
```

This will prompt you for all necessary inputs and generate a PDF schedule.

## Interactive Mode

When you run `main.py` without any arguments, the system enters interactive mode, guiding you through the scheduling process step by step.

1. **Launch interactive mode**
   ```bash
   python main.py
   ```

2. **Select algorithm**
   Choose from:
   - Graph Coloring (fastest)
   - Dynamic Programming (optimal for weighted activities)
   - Backtracking (complete solution)
   - Genetic Algorithm (evolutionary approach)
   - Run All (compares all algorithms)

3. **Input data**
   - Use sample data, custom file, or database

4. **Batch information**
   - Specify academic batch code (e.g., BCSE24)
   - Choose section (A/B)

5. **Output preferences**
   - Academic PDF (professional format with university branding)
   - Basic PDF (simple schedule layout)

6. **Database options**
   - Use existing database data
   - Initialize database with sample data

The system will process your selections and generate a PDF schedule based on your preferences.

## Command Line Usage

For automation or advanced usage, you can provide command-line arguments:

### Basic Examples

```bash
# Generate academic PDF using graph coloring (default)
python main.py

# Use specific algorithm
python main.py --algorithm dynamic-prog

# Run all algorithms and compare
python main.py --run-all

# Use custom input file
python main.py --input data/custom_courses.csv

# Generate basic PDF instead of academic
python main.py --pdf

# Specify batch and section
python main.py --batch BCSE23 --section B
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--algorithm TYPE` | Algorithm: `graph-coloring`, `dynamic-prog`, `backtracking`, `genetic` |
| `--run-all` | Run all algorithms and compare results |
| `--input FILE` | Input file with activities data |
| `--output FILE` | Output file for results |
| `--pdf` | Generate basic PDF output |
| `--batch CODE` | Specify batch code (e.g., BCSE24) |
| `--section NAME` | Specify section (default: A) |
| `--use-database` | Use database for input |
| `--init-db` | Initialize database with sample data |
| `--visualize` | Enable visualization output |

## Input Data Formats

The system supports multiple input formats:

### CSV Format
```csv
id,start,end,weight,name,code
1,0,90,3.0,Programming Fundamentals,CSE-101
2,100,190,3.0,Data Structures,CSE-102
```

### JSON Format
```json
[
  {
    "id": 1,
    "start": 0,
    "end": 90,
    "weight": 3.0,
    "name": "Programming Fundamentals",
    "code": "CSE-101"
  },
  {
    "id": 2,
    "start": 100,
    "end": 190,
    "weight": 3.0,
    "name": "Data Structures",
    "code": "CSE-102"
  }
]
```

## Output Types

### Academic PDF
- Professional format with university branding
- Organized by day and time slots
- Includes course details, instructor information, and room assignments
- Default output format

### Basic PDF
- Simple tabular format
- Lists activities with time slots
- Generated when using `--pdf` flag

## Algorithm Selection

### Graph Coloring
- Models conflicts as graph edges
- Fast performance
- Good for large datasets
- Command: `--algorithm graph-coloring`

### Dynamic Programming
- Optimal weighted activity selection
- Uses memoization for efficiency
- Best for weight optimization
- Command: `--algorithm dynamic-prog`

### Backtracking
- Exhaustive search with pruning
- Most thorough solution
- Can be slow for large datasets
- Command: `--algorithm backtracking`

### Genetic Algorithm
- Population-based evolutionary approach
- Good balance of speed and optimization
- Randomized, may give different results each run
- Command: `--algorithm genetic`

## Database Integration

The system can store and retrieve scheduling data from a MySQL database:

### Setup Database
```bash
# Initialize database with sample data
python main.py --init-db
```

### Use Database Data
```bash
# Use database for input
python main.py --use-database
```

### Batch-Specific Schedules
```bash
# Generate schedule for specific batch
python main.py --use-database --batch BCSE24
```

## Advanced Features

### Comprehensive Routine
Generate a complete department routine:
```bash
python main.py --comprehensive-routine
```

### Enhanced Generator
Use the enhanced routine generator with advanced conflict resolution:
```bash
python main.py --enhanced-generator
```

### University-Wide Schedule
Generate a complete university schedule (requires database):
```bash
python main.py --university-schedule
```

## Troubleshooting

### Common Issues

1. **No PDF is generated**
   - Ensure you have write permissions in the `output` directory
   - Try running with basic PDF: `python main.py --pdf`

2. **Database connection fails**
   - Check that MySQL is running: `service mysql status`
   - Verify credentials in `src/database/database_manager.py`
   - Try initializing: `python main.py --init-db`

3. **Import errors**
   - Ensure you're running from the project root directory
   - Verify all dependencies are installed: `pip install -r requirements.txt`

4. **No activities loaded**
   - Check input file path if using custom input
   - Try with sample data: `python main.py`

## FAQ

**Q: How do I view the generated PDF?**
A: PDF files are saved in the `output` directory. You can open them with any PDF viewer.

**Q: How can I create my own activity data?**
A: Create a CSV or JSON file following the format shown in the [Input Data Formats](#input-data-formats) section.

**Q: Which algorithm should I choose?**
A: For most cases, graph coloring (default) works well. For optimal solutions, try running all algorithms with `--run-all`.

**Q: Can I schedule multiple batches at once?**
A: Yes, use the `--comprehensive-routine` flag with database integration.

**Q: How can I extend or customize the system?**
A: The modular code structure allows for easy extension. See the project structure in README.md for guidance.

---

For additional help or to report issues, please contact the development team or open an issue on the project repository.
