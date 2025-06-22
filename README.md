# Conflict-Free Scheduling System

A comprehensive academic scheduling system that automatically generates conflict-free course schedules using multiple optimization algorithms.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing)

## 🎯 Features

- **Multiple Algorithms**: Backtracking, Dynamic Programming, Genetic Algorithm, Graph Coloring
- **Database Integration**: MySQL support for course and schedule management
- **PDF Generation**: Automatic creation of formatted academic schedules
- **Web Interface**: HTML output for easy viewing and sharing
- **Conflict Detection**: Automatic detection and resolution of scheduling conflicts
- **Academic Focus**: Designed specifically for educational institutions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- MySQL (optional, for database features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/punam06/conflictFreeScheduling.git
   cd ConflictFreeSchedulingPython
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the system**
   ```bash
   python main.py
   ```

## 💻 Usage

### Command Line Interface

**Basic usage:**
```bash
python main.py
```

**With specific algorithm:**
```bash
python main.py --algorithm genetic
```

**Available algorithms:**
- `backtracking` - Systematic search approach
- `dynamic_programming` - Optimization-based solution
- `genetic` - Evolutionary algorithm
- `graph_coloring` - Graph theory approach

### Python API

```python
from src.scheduler import ConflictFreeScheduler

# Initialize scheduler
scheduler = ConflictFreeScheduler()

# Load course data
courses = scheduler.load_courses('data/sample_courses.json')

# Generate schedule using genetic algorithm
schedule = scheduler.generate_schedule(courses, algorithm='genetic')

# Export to PDF
scheduler.export_pdf(schedule, 'output/my_schedule.pdf')
```

### Database Integration

```python
from examples.database_example import DatabaseSchedulerExample

# Initialize with database
db_example = DatabaseSchedulerExample()
db_example.setup_database()
db_example.run_complete_workflow()
```

## 🧮 Algorithms

### 1. Backtracking Algorithm
- **Approach**: Systematic exploration of scheduling possibilities
- **Best for**: Small to medium course sets
- **Time Complexity**: O(b^d) where b is branching factor, d is depth

### 2. Dynamic Programming
- **Approach**: Optimal substructure with memoization
- **Best for**: Courses with clear dependency structures
- **Time Complexity**: O(n²) where n is number of courses

### 3. Genetic Algorithm
- **Approach**: Evolutionary optimization
- **Best for**: Large course sets with complex constraints
- **Features**: Population-based, mutation, crossover operations

### 4. Graph Coloring
- **Approach**: Treats scheduling as graph vertex coloring
- **Best for**: Courses with clear conflict patterns
- **Time Complexity**: O(V + E) where V is vertices, E is edges

## 📊 Data Formats

### JSON Course Format
```json
{
  "courses": [
    {
      "id": "CS101",
      "name": "Introduction to Computer Science",
      "instructor": "Dr. Smith",
      "duration": 60,
      "preferred_times": ["09:00", "11:00"],
      "conflicts": ["CS102"]
    }
  ]
}
```

### CSV Course Format
```csv
id,name,instructor,duration,preferred_times,conflicts
CS101,Introduction to Computer Science,Dr. Smith,60,"09:00,11:00",CS102
```

## 🗄️ Database Setup

1. **Install MySQL**
2. **Create database**
   ```sql
   CREATE DATABASE scheduling_system;
   ```
3. **Configure connection**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```
4. **Run database example**
   ```bash
   python examples/database_example.py
   ```

## 📁 Project Structure

```
ConflictFreeSchedulingPython/
├── src/
│   ├── scheduler.py              # Main scheduler class
│   ├── algorithms/               # Algorithm implementations
│   │   ├── backtracking.py
│   │   ├── dynamic_programming.py
│   │   ├── genetic_algorithm.py
│   │   └── graph_coloring.py
│   ├── database/                 # Database management
│   │   └── database_manager.py
│   └── utils/                    # Utility functions
│       ├── file_parser.py
│       └── pdf_generator.py
├── data/                         # Sample data files
├── examples/                     # Usage examples
├── tests/                        # Unit tests
├── output/                       # Generated schedules
├── main.py                       # Main application
├── demo.py                       # Demonstration script
└── requirements.txt              # Dependencies
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=scheduling_system
```

### Algorithm Parameters
Configure algorithm parameters in the scheduler:
```python
scheduler = ConflictFreeScheduler(
    genetic_params={
        'population_size': 100,
        'generations': 50,
        'mutation_rate': 0.1
    }
)
```

## 📈 Performance

| Algorithm | Small Dataset (10 courses) | Medium Dataset (50 courses) | Large Dataset (100+ courses) |
|-----------|---------------------------|----------------------------|------------------------------|
| Backtracking | ~0.1s | ~2.5s | ~15s |
| Dynamic Programming | ~0.05s | ~1.2s | ~8s |
| Genetic Algorithm | ~0.2s | ~3.0s | ~12s |
| Graph Coloring | ~0.03s | ~0.8s | ~5s |

## 🛠️ Development

### Adding New Algorithms
1. Create algorithm file in `src/algorithms/`
2. Implement the `SchedulingAlgorithm` interface
3. Register in `scheduler.py`
4. Add tests in `tests/`

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Punam** - *Initial work* - [punam06](https://github.com/punam06)

## 🙏 Acknowledgments

- Academic scheduling research papers
- Python optimization libraries
- Open source scheduling algorithms
- Educational institution requirements

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the [USER_GUIDE.md](USER_GUIDE.md) for detailed documentation
- Review the examples in the `examples/` directory

---

**Built with ❤️ for academic institutions**
