# Enhanced Conflict-Free Scheduling System

A comprehensive academic scheduling system that automatically generates conflict-free course schedules using multiple optimization algorithms with proper time slots and modern UI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)](#features)

## 🎯 Features

- **Multiple Algorithms**: Graph Coloring, Dynamic Programming, Backtracking, Genetic Algorithm
- **Academic Routine Generator**: Comprehensive routine with proper time slots (8:30 AM - 5:30 PM)
- **Enhanced PDF Generation**: Modern, eye-catching schedules with faculty and room information
- **Database Integration**: MySQL support with realistic CSE department data
- **Interactive Faculty System**: Faculty input with automatic room allocation
- **Flexible Routine Types**: Section-wise, batch-wise, comprehensive, and academic routines
- **Realistic Data**: Authentic faculty names, department rooms, and university time slots
- **Modern UI**: Attractive table format with gradient backgrounds and responsive design

## ✨ New Academic Routine Features

- **📅 Schedule**: Sunday to Thursday, 8:30 AM - 5:30 PM
- **⏰ Time Slots**: 1.5-hour slots with 15-minute breaks
- **🍽️ Break Time**: 1:30 PM - 2:00 PM (lunch break)
- **🎓 All Batches**: BCSE22, BCSE23, BCSE24, BCSE25 
- **📚 All Sections**: A & B for each batch
- **👨‍🏫 Real Faculty**: 10 faculty members with proper designations
- **🏢 Proper Rooms**: Theory and lab room assignments
- **📱 Responsive UI**: Modern table format with attractive styling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL (optional, for database features)

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/punam06/conflictFreeScheduling.git
   cd ConflictFreeSchedulingPython
   pip install -r requirements.txt
   ```

2. **Run the system**
   ```bash
   # Interactive mode (recommended)
   python main.py
   
   # Direct command line
   python main.py --preserve-schedule --use-database
   ```

## 💻 Usage Examples

### Basic Scheduling
```bash
# Use realistic schedule without optimization
python main.py --preserve-schedule --init-db

# Run graph coloring algorithm
python main.py --algorithm graph-coloring --use-database

# Compare all algorithms
python main.py --run-all --use-database
```

### Enhanced Routine Generation
```bash
# Generate comprehensive academic routine (NEW!)
python main.py --academic-routine

# Generate section-wise routine
python main.py --enhanced --batch BCSE24 --section A

# Generate academic PDF
python main.py --input data/sample_courses.json --academic-pdf --batch BCSE24 --section A
# Generate comprehensive routine for all batches
python main.py --comprehensive --use-database

# Generate batch-specific routine
python main.py --batch-wise --batch BCSE24 --use-database

# Interactive faculty input system
python main.py --faculty-input
```

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
