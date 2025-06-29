# Enhanced Conflict-Free Class Scheduling System

A comprehensive academic scheduling solution designed for universities and educational institutions. This system intelligently generates conflict-free class schedules using multiple optimization algorithms, supports faculty preferences, and provides professional-quality output formats.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#features)

## 🎯 Core Features

### 🔬 Four Advanced Scheduling Algorithms
- **Graph Coloring Algorithm** - Models conflicts as graph edges, assigns time slots as colors
- **Dynamic Programming** - Optimal weighted activity selection with memoization
- **Backtracking Algorithm** - Exhaustive search with intelligent pruning
- **Genetic Algorithm** - Population-based evolutionary optimization

### 📊 Multiple Routine Generation Modes
- **Comprehensive Routine** - Single table showing all batches and sections
- **Batch-wise Routine** - Individual schedules for specific batches (e.g., BCSE24)
- **Section-wise Routine** - Targeted schedules for specific sections (e.g., BCSE24-A)
- **Faculty Input System** - Interactive preference-based scheduling with availability analysis

### 🎨 Professional Output Formats
- **Enhanced HTML Reports** - Interactive, responsive web-based schedules
- **Academic PDF Documents** - Professional printable format with university branding
- **Visual Highlighting** - Color-coded time slots and conflict detection
- **Preferred Time Analysis** - Faculty-specific availability visualization

## ✨ Enhanced Faculty Input System

### � Interactive Faculty Scheduling
The faculty input system provides a sophisticated interface for instructors to specify their teaching preferences:

- **Faculty Profile Management** - Add faculty members with contact information and department details
- **Course Assignment** - Assign courses to faculty with credit hours and batch/section information
- **Preferred Time Slots** - Faculty can specify their preferred teaching windows
- **Availability Analysis** - System shows available slots within preferred times
- **Visual Schedule Output** - Color-coded schedules highlighting preferred time matches
- **Conflict Resolution** - Automatic detection and resolution of scheduling conflicts
- **Fallback Generation** - Smart defaults when specific preferences cannot be accommodated

### 📋 Data-Driven Routine Generation
- **Comprehensive Mode** - Single table format showing all batches and sections together
- **Batch-wise Mode** - Individual schedules for specific batches (BCSE22, BCSE23, BCSE24, BCSE25)
- **Section-wise Mode** - Targeted schedules for specific sections (A, B)
- **Sample UI Format** - Modern, responsive design with professional styling

### ⏰ Schedule Configuration
- **📅 Schedule**: Monday to Friday, 8:00 AM - 6:00 PM
- **⏰ Time Slots**: Flexible periods (8:00-9:30, 9:30-11:00, 11:30-1:00, 2:00-3:30, 4:00-5:30)
- **🍽️ Break Times**: Configurable lunch and short breaks
- **🎓 Coverage**: All CSE batches with multiple sections
- **👨‍🏫 Faculty Management**: Complete faculty database with preferences
- **🏢 Room Allocation**: Smart room assignment with conflict avoidance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Required packages (automatically installed via requirements.txt)

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/punam06/conflictFreeScheduling.git
   cd ConflictFreeSchedulingPython
   pip install -r requirements.txt
   ```

2. **Quick Start Commands**
   ```bash
   # Interactive mode (recommended for beginners)
   python main.py
   
   # Generate comprehensive routine
   python main.py --comprehensive --no-database
   
   # Faculty input system
   python main.py --faculty-input --no-database
   
   # Algorithm comparison
   python main.py --run-all --no-database
   ```

## 💻 Usage Examples

### Routine Generation Modes
```bash
# Comprehensive routine (all batches/sections in single table)
python main.py --comprehensive --enhanced

# Batch-wise routine (specific batch)
python main.py --batch-wise --batch BCSE24 --no-database

# Section-wise routine (specific section)
python main.py --batch-wise --section A --no-database

# Faculty input with preference analysis
python main.py --faculty-input --no-database
```

### Algorithm Selection
```bash
# Use specific algorithm
python main.py --algorithm graph-coloring --input data/sample_activities.csv

# Compare all algorithms
python main.py --run-all --no-database

# Preserve realistic schedule
python main.py --preserve-schedule --use-database
```

### Output Formats
```bash
# Enhanced PDF and HTML (default)
python main.py --comprehensive --enhanced

# Academic PDF with university branding
python main.py --academic-pdf --batch BCSE24

# Basic PDF format
python main.py --basic-pdf --input data/sample_courses.csv
```

### Faculty Input System
```bash
# Interactive faculty input
python main.py --faculty-input --no-database

# The system will:
# - Load existing faculty data from data/faculty_data.json
# - Show available slots in preferred times
# - Generate enhanced HTML with visual highlighting
# - Create PDF output with professional formatting
```

## 🎓 Enhanced Faculty Input System

### Key Features
- **Interactive Faculty Management** - Add faculty with contact information and preferences
- **Preferred Time Analysis** - Visual highlighting of available slots in preferred times
- **Course Assignment** - Link courses to faculty with batch/section information
- **Smart Fallback** - Default schedule generation when preferences cannot be met
- **Professional Output** - Color-coded HTML and PDF generation

### Faculty Data Format
The system uses `data/faculty_data.json`:
```json
{
  "faculties": [
    {
      "name": "Dr. Ahmed Rahman",
      "email": "ahmed.rahman@university.edu", 
      "department": "CSE",
      "preferred_times": ["9:00 AM - 12:00 PM", "1:00 PM - 4:00 PM"]
    }
  ],
  "courses": [
    {
      "course_code": "CSE101",
      "course_name": "Introduction to Programming",
      "faculty": "Dr. Ahmed Rahman",
      "credits": 3,
      "batch": "BCSE24",
      "section": "A"
    }
  ]
}
```

### Output Features
- **Available Slot Count** - Shows number of free slots in preferred times
- **Visual Highlighting** - Color-coded preferred time indicators
- **Conflict Detection** - Automatic identification of scheduling issues
- **Multiple Formats** - Both HTML (interactive) and PDF (printable) outputs

## 🧮 Algorithms

| Algorithm | Best For | Time Complexity | Features |
|-----------|----------|-----------------|----------|
| **Graph Coloring** | Maximum activities | O(V + E) | Fast, conflict resolution |
| **Dynamic Programming** | Optimal weights | O(n²) | Weight optimization |
| **Backtracking** | Small datasets | O(b^d) | Guaranteed optimal |
| **Genetic Algorithm** | Large datasets | O(generations) | Evolutionary optimization |

## 🎓 Academic Features

### CSE Department Integration
- **Real Faculty**: Nazneen Akter, Sobhana Zahan, Tahmid Tarmin Sukhi, and others
- **Department Rooms**: 302, 303, 304, 504, 1003
- **Authentic Time Slots**: 08:30-10:00, 10:00-11:30, 11:30-13:00, 14:00-15:30
- **Course Codes**: Standard CSE numbering (CSE111, CSE112, etc.)

### Batch Management
- **Supported Batches**: BCSE22, BCSE23, BCSE24, BCSE25
- **Sections**: A, B (expandable)
- **Credit Hours**: Proper academic credit allocation

## 📁 Project Structure

```
ConflictFreeSchedulingPython/
├── main.py                       # Main application
├── src/
│   ├── scheduler.py              # Core scheduling engine
│   ├── algorithms/               # Four optimization algorithms
│   ├── database/                 # MySQL integration
│   └── utils/                    # PDF generation & utilities
├── data/                         # Sample data files
├── output/                       # Generated schedules
├── tests/                        # Unit tests
└── examples/                     # Usage examples
```

## 🔧 Configuration

### Database Setup (Optional)
```bash
# Initialize with realistic data
python main.py --init-db

# Or use file input
python main.py --input data/sample_courses.csv
```

## 📊 Sample Output

```
📅 SUNDAY
----------------------------------------------------------
08:30-10:00  | CSE111 | Computer Programming      | Nazneen Akter    | Room: 302
08:30-10:30  | CSE112 | Computer Programming Lab  | Sobhana Zahan    | Room: 1003
10:00-11:30  | CSE121 | Discrete Mathematics      | Tahmid Tarmin    | Room: 303
11:30-13:00  | MAT102 | Calculus II               | Iyolita Islam    | Room: 304
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Debug and performance test
python debug_test.py --comprehensive

# Quick demo
python demo.py
```

## 🔗 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)**: Comprehensive usage guide
- **[Makefile](Makefile)**: Build commands and automation

## 📝 License

This project is licensed under the MIT License.

## 👥 Author

**Punam** - CSE Department Academic Scheduling Solution

---

**✅ Status**: Complete and Production Ready  
**🎯 Version**: 2.0 (Enhanced)
