# Enhanced Conflict-Free Class Scheduling System - User Guide

Welcome to the comprehensive user guide for the Enhanced Conflict-Free Class Scheduling System. This advanced academic scheduling solution provides powerful tools for generating conflict-free schedules with faculty preferences and professional output formats.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [System Overview](#system-overview)
3. [Installation and Setup](#installation-and-setup)
4. [Usage Modes](#usage-modes)
5. [Routine Generation Types](#routine-generation-types)
6. [Faculty Input System](#faculty-input-system)
7. [Algorithm Selection](#algorithm-selection)
8. [Output Formats](#output-formats)
9. [Command Line Interface](#command-line-interface)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Features](#advanced-features)

## 🚀 Getting Started

### What is the Enhanced Conflict-Free Class Scheduling System?

This system is a comprehensive academic scheduling solution that automatically generates conflict-free class schedules for universities and educational institutions. It uses advanced algorithms to optimize schedules while respecting faculty preferences, room availability, and institutional constraints.

### Key Benefits
- **Automated Scheduling** - No more manual schedule creation
- **Conflict Detection** - Automatic identification and resolution of scheduling conflicts
- **Faculty Preferences** - Respects instructor preferred teaching times
- **Professional Output** - High-quality HTML and PDF reports
- **Multiple Algorithms** - Choose the best optimization approach for your needs
- **Flexible Input** - Support for CSV, JSON, and database sources

## 🏗️ System Overview

### Core Components
1. **Scheduling Engine** - Core algorithm processing
2. **Faculty Input System** - Interactive preference management
3. **Output Generator** - Professional HTML/PDF creation
4. **Database Manager** - Optional data persistence
5. **CLI Interface** - Command-line interaction

### Supported Routine Types
- **Comprehensive** - All batches and sections in one table
- **Batch-wise** - Individual schedules for specific batches
- **Section-wise** - Targeted schedules for specific sections
- **Faculty-based** - Generated from faculty preferences

### Installation Steps

1. **Download and Setup**
   ```bash
   git clone https://github.com/punam06/conflictFreeScheduling.git
   cd conflictFreeScheduling
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python main.py --help
   ```

### First Run

Test the system with sample data:
```bash
python demo.py
```

This will:
- Create sample activities
- Run all algorithms
- Generate HTML and PDF output
- Show performance comparisons

## 💻 Command Line Interface

### Basic Syntax
```bash
python main.py [OPTIONS]
```

### Essential Options

#### Algorithm Selection
```bash
--algorithm ALGO          # Choose algorithm: graph-coloring, dynamic-prog, backtracking, genetic
--run-all                 # Run all algorithms and compare results
```

#### Input/Output
```bash
--input FILE              # Input data file (CSV or JSON)
--output DIR              # Output directory (default: output/)
--pdf                     # Generate basic PDF
--academic-pdf            # Generate university-branded PDF
```

#### Academic Settings
```bash
--batch CODE              # Batch code (e.g., BCSE24)
--section SECTION         # Section (A or B)
--semester SEMESTER       # Semester information
```

#### Database Options
```bash
--use-database            # Use database instead of file input
--init-db                 # Initialize database with sample data
--no-database            # Force file input mode
```

### Complete Example Commands

#### Basic Scheduling
```bash
# Run graph coloring with demo data
python main.py --algorithm graph-coloring --input data/demo_activities.csv

# Compare all algorithms
python main.py --run-all --input data/sample_courses.csv
```

#### Academic PDF Generation
```bash
# Generate academic PDF for BCSE24 Section A
python main.py --algorithm graph-coloring --academic-pdf --batch BCSE24 --section A

# Use custom semester information
python main.py --algorithm dynamic-prog --academic-pdf --batch BCSE25 --section B --semester "Fall 2025"
```

#### Database Operations
```bash
# Initialize database and run scheduling
python main.py --init-db --use-database --algorithm graph-coloring

# Schedule specific batch from database
python main.py --use-database --batch BCSE24 --section A --academic-pdf
```

## 🧠 Algorithm Selection

### Graph Coloring Algorithm
**Best for**: Maximum activity scheduling, minimal conflicts

**Usage**:
```bash
python main.py --algorithm graph-coloring --input data/demo_activities.csv
```

**Characteristics**:
- ✅ **Strengths**: Fast execution, maximum activities scheduled
- ⚠️ **Limitations**: May not optimize for weights/credits
- 🎯 **Use Case**: When you want to fit as many activities as possible

### Dynamic Programming Algorithm  
**Best for**: Optimizing total credits/weights

**Usage**:
```bash
python main.py --algorithm dynamic-prog --input data/demo_activities.csv
```

**Characteristics**:
- ✅ **Strengths**: Optimal weight/credit maximization
- ⚠️ **Limitations**: May schedule fewer activities
- 🎯 **Use Case**: When credit hours are priority

### Backtracking Algorithm
**Best for**: Small datasets, guaranteed optimal solutions

**Usage**:
```bash
python main.py --algorithm backtracking --input data/demo_activities.csv
```

**Characteristics**:
- ✅ **Strengths**: Explores all possibilities, finds optimal solution
- ⚠️ **Limitations**: Slow for large datasets (>50 activities)
- 🎯 **Use Case**: Small schedules where optimality is crucial

### Genetic Algorithm
**Best for**: Large datasets, complex constraints

**Usage**:
```bash
python main.py --algorithm genetic --input data/demo_activities.csv
```

**Characteristics**:
- ✅ **Strengths**: Handles large datasets, customizable fitness
- ⚠️ **Limitations**: Approximate solutions, longer execution time
- 🎯 **Use Case**: Complex scheduling with multiple objectives

### Algorithm Comparison
Run all algorithms to compare results:
```bash
python main.py --run-all --input data/demo_activities.csv
```

This generates a comparison table showing:
- Number of activities scheduled
- Total weight/credits
- Execution time
- Efficiency percentage

## 📝 Input Data Formats

### CSV Format
**File**: `data/sample_courses.csv`

```csv
id,start,end,weight,name,room
1,540,630,3.0,Programming Fundamentals,CSE-101
2,640,730,1.0,Programming Lab,CSE-Lab1
3,750,840,3.0,Data Structures,CSE-102
```

**Field Descriptions**:
- `id`: Unique activity identifier
- `start`: Start time in minutes from midnight
- `end`: End time in minutes from midnight  
- `weight`: Credit hours or priority weight
- `name`: Course/activity name
- `room`: Room assignment

### JSON Format
**File**: `data/sample_courses.json`

```json
{
  "activities": [
    {
      "id": 1,
      "start": 540,
      "end": 630,
      "weight": 3.0,
      "name": "Programming Fundamentals",
      "room": "CSE-101"
    }
  ],
  "metadata": {
    "total_activities": 1,
    "total_weight": 3.0,
    "generated_at": "2025-06-23T10:30:00"
  }
}
```

### Time Format Reference
Times are represented in minutes from midnight:

| Time | Minutes | Calculation |
|------|---------|-------------|
| 8:00 AM | 480 | 8 × 60 = 480 |
| 9:00 AM | 540 | 9 × 60 = 540 |
| 12:00 PM | 720 | 12 × 60 = 720 |
| 3:00 PM | 900 | 15 × 60 = 900 |

### Creating Custom Data

1. **Generate Sample Data**:
   ```bash
   python -c "
   from src.utils.file_parser import FileParser
   FileParser.generate_sample_data('my_courses.csv', 20)
   "
   ```

2. **Convert Formats**:
   ```bash
   python -c "
   from src.utils.file_parser import FileParser
   activities = FileParser.parse_csv('my_courses.csv')
   FileParser.write_json(activities, 'my_courses.json')
   "
   ```

## 📄 Output Generation

### HTML Output
**Generated automatically** for all runs

**Features**:
- Interactive web format
- Modern responsive design
- Schedule summary statistics
- Printable layout

**Example**:
```bash
python main.py --algorithm graph-coloring --input data/demo_activities.csv
# Generates: output/schedule_YYYYMMDD_HHMMSS.html
```

### Basic PDF Output
**Flag**: `--pdf`

**Features**:
- Simple PDF format
- Table-based layout
- Basic statistics

**Example**:
```bash
python main.py --algorithm graph-coloring --input data/demo_activities.csv --pdf
```

### Academic PDF Output
**Flag**: `--academic-pdf`

**Features**:
- University branding (BUP)
- Department headers
- Course codes and credits
- Signature sections
- Professional formatting

**Example**:
```bash
python main.py --algorithm graph-coloring --academic-pdf --batch BCSE24 --section A
# Generates: output/academic_schedule_BCSE24_A.pdf
```

### Customizing Output

#### Output Directory
```bash
python main.py --algorithm graph-coloring --output my_schedules/
```

#### Custom Batch/Section
```bash
python main.py --academic-pdf --batch BCSE25 --section B --semester "Summer 2025"
```

## 🗄️ Database Integration

### Database Setup

1. **Install MySQL** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   
   # macOS
   brew install mysql
   
   # Windows
   # Download from: https://dev.mysql.com/downloads/mysql/
   ```

2. **Create Database**:
   ```sql
   CREATE DATABASE conflict_free_scheduling;
   CREATE USER 'scheduler'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON conflict_free_scheduling.* TO 'scheduler'@'localhost';
   ```

3. **Initialize Schema**:
   ```bash
   python scripts/initialize_database.py
   ```

### Database Configuration

Create `.env` file:
```env
DB_HOST=localhost
DB_USER=scheduler
DB_PASSWORD=password
DB_NAME=conflict_free_scheduling
DB_PORT=3306
```

### Database Operations

#### Initialize with Sample Data
```bash
python main.py --init-db
```

#### Run Database-Driven Scheduling
```bash
python main.py --use-database --algorithm graph-coloring
```

#### Batch-Specific Scheduling
```bash
python main.py --use-database --batch BCSE24 --section A
```

### Database Schema

**Tables Created**:
- `batches`: Student batch information
- `teachers`: Faculty data
- `rooms`: Classroom information  
- `courses`: Course catalog
- `schedules`: Generated schedule storage

**Example Queries**:
```python
# Load courses for specific batch
python examples/database_example.py
```

## 🎓 Academic Features

### University Integration

**Supported Institution**: Bangladesh University of Professionals (BUP)
**Department**: Computer Science & Engineering

### Batch Management

**Supported Batches**:
- BCSE22 (Computer Science & Engineering 2022)
- BCSE23 (Computer Science & Engineering 2023)  
- BCSE24 (Computer Science & Engineering 2024)
- BCSE25 (Computer Science & Engineering 2025)

**Sections**: A, B (expandable)

### Course Code Generation

The system automatically generates course codes:
```
CSE001 - Programming Fundamentals
CSE002 - Programming Lab
CSE003 - Data Structures
...
```

### Credit Hour Management

**Weight Interpretation**:
- `1.0` = 1 Credit Hour (typically labs)
- `3.0` = 3 Credit Hours (typical theory course)
- `4.0` = 4 Credit Hours (major courses)

**Class Type Detection**:
- Weight < 2.0 → Lab
- Weight ≥ 2.0 → Theory

### Academic Calendar Integration

**Semester Support**:
- Spring (January - May)
- Summer (June - August)  
- Fall (September - December)

**Example**:
```bash
python main.py --academic-pdf --batch BCSE24 --section A --semester "Spring 2025"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ImportError: No module named 'src'`
**Solution**:
```bash
# Ensure you're in the project root directory
cd /path/to/ConflictFreeSchedulingPython
python main.py --help
```

#### 2. PDF Generation Issues
**Problem**: WeasyPrint library errors
**Solution**: System uses ReportLab as fallback automatically
```bash
# Force ReportLab usage (automatic fallback)
python main.py --academic-pdf --batch BCSE24 --section A
```

#### 3. Database Connection Issues
**Problem**: `Can't connect to MySQL server`
**Solutions**:
```bash
# Check MySQL service
sudo systemctl status mysql  # Linux
brew services list mysql     # macOS

# Test connection
mysql -u scheduler -p -h localhost

# Use file input instead
python main.py --no-database --input data/demo_activities.csv
```

#### 4. Empty Output
**Problem**: No activities scheduled
**Possible Causes**:
- Input file format issues
- All activities have conflicts
- Wrong algorithm for dataset

**Solutions**:
```bash
# Debug data loading
python debug_test.py --comprehensive

# Try different algorithm
python main.py --run-all --input data/demo_activities.csv

# Check input format
head -5 data/demo_activities.csv
```

#### 5. Performance Issues
**Problem**: Slow execution
**Solutions**:
```bash
# Use faster algorithm for large datasets
python main.py --algorithm graph-coloring --input large_dataset.csv

# Profile performance
python debug_test.py --profile --algorithm graph-coloring
```

### Debug Tools

#### Comprehensive Testing
```bash
python debug_test.py --comprehensive
```

#### Algorithm-Specific Testing
```bash
python debug_test.py --algorithm graph-coloring --verbose
```

#### Performance Profiling
```bash
python debug_test.py --profile --algorithm genetic
```

### Log Analysis

**Check Output Files**:
```bash
ls -la output/
file output/academic_schedule_BCSE24_A.pdf
```

**Validate Data**:
```python
python -c "
from src.utils.file_parser import FileParser
activities = FileParser.parse_csv('data/demo_activities.csv')
print(f'Loaded {len(activities)} activities')
for a in activities[:3]:
    print(a)
"
```

## 🔧 Advanced Usage

### Custom Algorithm Parameters

#### Genetic Algorithm Tuning
```python
from src.algorithms.genetic_algorithm import GeneticScheduler

scheduler = GeneticScheduler(
    population_size=100,
    generations=50,
    mutation_rate=0.1,
    crossover_rate=0.8
)
```

#### Graph Coloring Optimization
```python
from src.algorithms.graph_coloring import GraphColoringScheduler

scheduler = GraphColoringScheduler(
    color_strategy='largest_first',
    conflict_threshold=0.1
)
```

### Batch Processing

**Process Multiple Files**:
```bash
for file in data/*.csv; do
    python main.py --algorithm graph-coloring --input "$file" --pdf
done
```

**Automated Batch Scheduling**:
```bash
for batch in BCSE22 BCSE23 BCSE24 BCSE25; do
    for section in A B; do
        python main.py --use-database --academic-pdf --batch "$batch" --section "$section"
    done
done
```

### Integration with External Systems

#### API Integration
```python
from src.scheduler import ConflictFreeScheduler
import json

def schedule_api(activities_json):
    activities = json.loads(activities_json)
    scheduler = ConflictFreeScheduler()
    result = scheduler.graph_color
