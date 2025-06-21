# Conflict-Free Scheduling System (Python)

✅ **Conversion Complete: This project has been fully converted from C++ to Python with al## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 2 minutes
- **[Complete User Guide](USER_GUIDE.md)** - Detailed instructions and troubleshooting
- **[Data Format Specification](docs/DATA_FORMAT.md)** - Details on input/output data formats
- **Tutorial Notebook** - Interactive guide (run `./run.sh tutorial`)
- **Command Line Interface** - Comprehensive CLI options belowtures implemented!**

A comprehensive Python implementation of a conflict-free scheduling system for academic institutions, specifically designed for the Bangladesh University of Professionals (BUP) Computer Science & Engineering Department.

## 🎯 Features

### 🔬 Four Core Scheduling Algorithms
1. **Graph Coloring** - Models conflicts as graph edges, assigns time slots as colors
2. **Dynamic Programming** - Optimal weighted activity selection with memoization
3. **Backtracking** - Exhaustive search with pruning for optimal solutions
4. **Genetic Algorithm** - Population-based evolutionary optimization

### 📊 Academic Features
- Professional PDF generation with university branding
- Section-wise schedules (BCSE22-25, Sections A & B)
- Faculty schedules with contact information
- Room utilization reports
- Credit-hour based session durations
- External faculty scheduling support

### 🗄️ Database Integration
- MySQL database support with SQLAlchemy ORM
- Sample data initialization
- Multi-batch course management
- Teacher and classroom management

### 📄 Multiple Output Formats
- HTML schedules with modern styling
- Academic PDF reports
- CSV/JSON data export
- Visualization support

### 📚 Documentation
- Interactive Jupyter notebook tutorial
- Comprehensive data format specifications
- Command-line interface documentation
- API reference

## 🚀 Quick Start

### Fastest Way to Start (Recommended for New Users)

1. **Interactive Quick Start**
   ```bash
   python quick_start.py
   ```
   Choose from easy options: demo, interactive mode, or setup.

2. **Direct Interactive Mode**
   ```bash
   python main.py
   ```
   The system will ask you what you want to do step by step.

3. **One-Command Generation**
   ```bash
   python main.py --algorithm graph-coloring
   ```
   Immediately generates a professional academic PDF schedule.

### Prerequisites
- Python 3.8 or higher
- MySQL server (optional, for database features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ConflictFreeSchedulingPython
   ```

2. **Run the setup script to automatically install dependencies and configure the database**
   ```bash
   ./run.sh setup
   ```
   
   Or, to manually install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database (optional, if not using setup script)**
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE conflict_free_scheduling;
   exit
   
   # Initialize the database with sample data
   ./scripts/initialize_database.py --sample-data
   ```

### Basic Usage

1. **Use the run script for common operations**
   ```bash
   # Run with basic graph coloring algorithm
   ./run.sh basic
   
   # Run all algorithms and compare them
   ./run.sh all
   
   # Generate academic PDF schedule
   ./run.sh academic
   
   # Initialize database and run with it
   ./run.sh database
   
   # Run integrated demonstration of all components
   ./run.sh demo
   
   # Open interactive Jupyter notebook tutorial
   ./run.sh tutorial
   ```

2. **Or use the main script directly**
   ```bash
   # Run with sample data (automatically generates academic PDF)
   python main.py --algorithm graph-coloring
   
   # Initialize database and run
   python main.py --init-db
   
   # Compare all algorithms
   python main.py --run-all --visualize
   
   # Generate academic schedule for a specific batch
   python main.py --batch BCSE24 --section A
   ```

## � Documentation

- [Data Format Specification](docs/DATA_FORMAT.md) - Details on input/output data formats
- Tutorial Notebook - Interactive guide (run `./run.sh tutorial`)
- Command Line Interface - Comprehensive CLI options below

## �📋 Command Line Options

### Algorithm Selection
- `--algorithm <type>` - Choose algorithm: `graph-coloring`, `dynamic-prog`, `backtracking`, `genetic`
- `--run-all` - Run all 4 algorithms and compare results

### Input/Output
- `--input <file>` - Input file with activities data (CSV/JSON/TXT)
- `--output <file>` - Output file for results
- `--pdf` - Generate basic PDF output instead of academic PDF
- `--academic-pdf` - Generate professional academic schedule PDF (default behavior)

### Database Options
- `--use-database` - Use database for input
- `--init-db` - Initialize/reset database with sample data
- `--no-database` - Disable database integration

### Academic Options
- `--batch <code>` - Specify batch code (e.g., BCSE23)
- `--section <name>` - Specify section name (A or B)
- `--semester <sem>` - Semester information

### Examples

```bash
# Basic scheduling with graph coloring (academic PDF is generated by default)
python main.py --algorithm graph-coloring

# Compare all algorithms with visualization
python main.py --run-all --visualize

# Generate academic PDF for specific batch
python main.py --batch BCSE24 --section A

# Use custom input file to generate a basic PDF instead
python main.py --input data/courses.csv --pdf

# Initialize database and generate comprehensive schedule
python main.py --init-db --comprehensive-routine
```

## 📁 Project Structure

```
ConflictFreeSchedulingPython/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── src/                           # Source code
│   ├── __init__.py
│   ├── scheduler.py               # Main scheduler class
│   ├── algorithms/                # Scheduling algorithms
│   │   ├── __init__.py
│   │   ├── graph_coloring.py      # Graph coloring algorithm
│   │   ├── dynamic_programming.py # Dynamic programming
│   │   ├── backtracking.py        # Backtracking algorithm
│   │   └── genetic_algorithm.py   # Genetic algorithm
│   ├── database/                  # Database management
│   │   ├── __init__.py
│   │   └── database_manager.py    # SQLAlchemy database interface
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       ├── file_parser.py         # File I/O utilities
│       └── pdf_generator.py       # PDF generation
├── data/                          # Data files
├── output/                        # Generated outputs
├── tests/                         # Unit tests
└── scripts/                       # Utility scripts
```

## 🔧 Configuration

### Database Configuration
The system uses MySQL by default. Configure your database connection in the `DatabaseManager` class:

```python
db = DatabaseManager(
    host="localhost",
    database="conflict_free_scheduling",
    user="root",
    password="your_password",
    port=3306
)
```

### Algorithm Parameters
Each algorithm can be configured:

```python
# Genetic Algorithm Configuration
config = GAConfig(
    population_size=50,
    generations=100,
    crossover_rate=0.8,
    mutation_rate=0.1,
    elite_size=5
)
```

## 📊 Input Data Formats

### CSV Format
```csv
id,start,end,weight,name,room
1,0,90,3.0,Programming Fundamentals,CSE-101
2,100,190,3.0,Data Structures,CSE-102
```

### JSON Format
```json
{
    "activities": [
        {
            "id": 1,
            "start": 0,
            "end": 90,
            "weight": 3.0,
            "name": "Programming Fundamentals",
            "room": "CSE-101"
        }
    ]
}
```

### Text Format
```
# Comments start with #
id start end weight name room
1 0 90 3.0 Programming_Fundamentals CSE-101
2 100 190 3.0 Data_Structures CSE-102
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest tests/ --cov=src/
```

## 🎨 Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Graph Coloring | O(V²) | O(V) | General conflict resolution |
| Dynamic Programming | O(n log n) | O(n) | Optimal weighted selection |
| Backtracking | O(2ⁿ) | O(n) | Small datasets, optimal solutions |
| Genetic Algorithm | O(g × p × n) | O(p × n) | Large datasets, good solutions |

Where:
- V = number of vertices (activities)
- n = number of activities
- g = generations
- p = population size

## 🔄 Migration from C++

This Python version maintains API compatibility with the original C++ implementation while providing:
- Easier dependency management
- Better cross-platform support
- Simpler database integration
- Enhanced PDF generation
- More flexible file I/O

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏫 Academic Context

Designed for the Bangladesh University of Professionals (BUP) Computer Science & Engineering Department to handle:
- 4 Batches: BCSE22, BCSE23, BCSE24, BCSE25
- 8 Sections: A & B for each batch
- 36+ Courses across all semesters
- Faculty scheduling with constraints
- Room allocation optimization

## 🛠️ Development

### Setting up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Style
The project follows PEP 8 guidelines. Use `black` for formatting:
```bash
black src/ tests/
```

### Database Schema
The system uses the following main tables:
- `batches` - Academic batches (BCSE22-25)
- `teachers` - Faculty information
- `classrooms` - Room details
- `courses` - Course information
- `course_sections` - Section assignments

## 📧 Support

For questions or issues:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Contact the development team

## 🔮 Future Enhancements

- [ ] Web-based interface
- [ ] Real-time scheduling updates
- [ ] Mobile app support
- [ ] Advanced visualization
- [ ] Integration with university systems
- [ ] Multi-language support
- [ ] Advanced reporting features
# conflictFreeScheduling
