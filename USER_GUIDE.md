# User Guide - Conflict-Free Scheduling System

Welcome to the comprehensive user guide for the Conflict-Free Scheduling System. This guide will help you understand and effectively use all features of the system.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Command Line Interface](#command-line-interface)
3. [Algorithm Selection](#algorithm-selection)
4. [Input Data Formats](#input-data-formats)
5. [Output Generation](#output-generation)
6. [Database Integration](#database-integration)
7. [Academic Features](#academic-features)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)

## 🚀 Getting Started

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM
- **Storage**: 500MB free space
- **Optional**: MySQL for database features

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
```bash
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
    result = scheduler.graph_coloring_schedule(activities)
    return json.dumps([vars(a) for a in result])
```

#### Web Service Deployment
```python
from flask import Flask, request, jsonify
from src.scheduler import ConflictFreeScheduler

app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def create_schedule():
    data = request.get_json()
    # Process scheduling request
    return jsonify(result)
```

### Performance Optimization

#### Large Dataset Handling
```bash
# Use graph coloring for large datasets (fastest)
python main.py --algorithm graph-coloring --input large_data.csv

# Parallelize batch processing
python scripts/parallel_scheduler.py --input-dir data/ --output-dir results/
```

#### Memory Management
```python
# Process in chunks for very large datasets
def process_large_dataset(filename, chunk_size=1000):
    activities = FileParser.parse_csv(filename)
    for i in range(0, len(activities), chunk_size):
        chunk = activities[i:i+chunk_size]
        result = scheduler.graph_coloring_schedule(chunk)
        # Process chunk result
```

### Custom Output Formats

#### CSV Export
```python
from src.utils.file_parser import FileParser

# Export scheduled activities to CSV
FileParser.write_csv(scheduled_activities, 'output/schedule.csv')
```

#### JSON API Format
```python
def export_json_api(activities, filename):
    data = {
        'schedule': [vars(a) for a in activities],
        'metadata': {
            'total_activities': len(activities),
            'total_credits': sum(a.weight for a in activities),
            'generated_at': datetime.now().isoformat()
        }
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
```

## 📞 Support

### Getting Help

1. **Check Documentation**: This user guide and README.md
2. **Run Debug Tools**: `python debug_test.py --comprehensive`
3. **Check Issues**: [GitHub Issues](https://github.com/punam06/conflictFreeScheduling/issues)
4. **Contact Developer**: Through GitHub or university email

### Reporting Issues

When reporting issues, include:
- Python version (`python --version`)
- Operating system
- Complete error message
- Input data sample (if applicable)
- Steps to reproduce

### Feature Requests

Submit feature requests through GitHub Issues with:
- Clear description of desired functionality
- Use case explanation
- Expected behavior
- Any relevant academic requirements

---

**📚 Need More Help?** 
- 📖 Check the [README.md](README.md) for technical details
- 🔧 Run `python debug_test.py --help` for debugging options
- 💻 See `python main.py --help` for all CLI options
- 🎓 Contact the CSE Department for academic-specific questions

**✅ Happy Scheduling!** 🎯
