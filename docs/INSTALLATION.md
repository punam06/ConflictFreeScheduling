# Installation Guide

Complete installation guide for the Conflict-Free Scheduling project.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Development Setup](#development-setup)
- [Troubleshooting](#troubleshooting)

## System Requirements

## System Requirements

### Minimum Requirements
- **C++ Compiler**: g++ 9.0+ or clang++ 10.0+
- **CMake**: 3.16 or higher
- **Memory**: 2GB RAM
- **Storage**: 100MB free space
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)

### Recommended Requirements
- **C++ Compiler**: g++ 11+ or clang++ 12+
- **CMake**: 3.20+
- **Memory**: 4GB+ RAM
- **Storage**: 500MB free space
- **CPU**: Multi-core processor for better performance

## Quick Start

### Option 1: CMake Build (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/ConflictFreeScheduling.git
cd ConflictFreeScheduling

# Create build directory
mkdir build && cd build

# Configure and build
cmake ..
make

# Run the program
./scheduler

# Run tests
make test
```

### Option 2: Direct Makefile Build

```bash
# Clone the repository
git clone https://github.com/yourusername/ConflictFreeScheduling.git
cd ConflictFreeScheduling

# Build using Makefile
make

# Run the program
./bin/scheduler

# Run tests
make test
```

### Option 2: Direct Download

1. Download ZIP from GitHub
2. Extract to desired location
3. Follow installation steps above

## Detailed Installation

### Step 1: Python Installation

**Windows:**
```bash
# Download Python from python.org
# Or use Chocolatey
choco install python

# Verify installation
python --version
pip --version
```

**macOS:**
```bash
# Using Homebrew
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### Step 2: Project Setup

```bash
# Navigate to project directory
cd ConflictFreeScheduling

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Verify Installation

```bash
# Run test suite
python -m pytest tests/ -v

# Check if all modules import correctly
python -c "import matplotlib, numpy, pytest; print('All dependencies installed successfully!')"
```

## Development Setup

### Additional Development Tools

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Or install individually
pip install black flake8 mypy jupyter notebook
```

### IDE Configuration

#### VS Code Setup

1. Install Python extension
2. Open project folder
3. Select Python interpreter from virtual environment
4. Configure linting and formatting:

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "editor.formatOnSave": true
}
```

#### PyCharm Setup

1. Open project
2. Configure Python interpreter: Settings → Project → Python Interpreter
3. Select existing environment: venv/bin/python
4. Enable code style: Settings → Editor → Code Style → Python

### Git Hooks (Optional)

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Optional Dependencies

### For Advanced Visualization

```bash
# Interactive plots
pip install plotly dash

# Statistical visualization
pip install seaborn

# Network graphs
pip install networkx
```

### For Performance Analysis

```bash
# Memory profiling
pip install memory-profiler psutil

# Performance monitoring
pip install line-profiler

# Benchmarking
pip install pyperf
```

### For Web Interface

```bash
# Flask web framework
pip install flask flask-cors

# Or Streamlit for quick demos
pip install streamlit
```

## Troubleshooting

### Common Issues

#### Issue 1: Permission Denied (Windows)

**Error**: `Permission denied` when installing packages

**Solution**:
```bash
# Run as administrator or use --user flag
pip install --user -r requirements.txt
```

#### Issue 2: Virtual Environment Not Activating

**Error**: Virtual environment commands not recognized

**Solution**:
```bash
# Windows - try different activation script
venv\Scripts\activate.bat
# or
venv\Scripts\Activate.ps1

# macOS/Linux - check shell
which python
source venv/bin/activate
```

#### Issue 3: Module Not Found Errors

**Error**: `ModuleNotFoundError` when running code

**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt

# Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Issue 4: Matplotlib Display Issues

**Error**: Plots not displaying properly

**Solution**:
```bash
# Install GUI backend
pip install PyQt5

# Or for headless environments
import matplotlib
matplotlib.use('Agg')
```

### Platform-Specific Issues

#### macOS

```bash
# If experiencing SSL certificate issues
/Applications/Python\ 3.x/Install\ Certificates.command

# If Xcode command line tools missing
xcode-select --install
```

#### Linux

```bash
# Install additional dependencies
sudo apt install python3-dev python3-tk

# For numerical computing
sudo apt install libblas-dev liblapack-dev gfortran
```

#### Windows

```bash
# If Microsoft Visual C++ 14.0 required
# Download and install Microsoft C++ Build Tools
# Or install Visual Studio with C++ support
```

### Verification Commands

```bash
# Check Python path
python -c "import sys; print(sys.executable)"

# Check installed packages
pip list

# Check project structure
ls -la  # Linux/macOS
dir     # Windows

# Test import of main modules
python -c "
try:
    import numpy
    import matplotlib
    import pytest
    print('✓ Core dependencies working')
except ImportError as e:
    print(f'✗ Import error: {e}')
"
```

## Environment Variables

Create a `.env` file for configuration:

```bash
# .env file
DEBUG=True
LOG_LEVEL=INFO
OUTPUT_DIR=./output
PLOT_BACKEND=Qt5Agg
```

Load in your code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

## Docker Setup (Advanced)

For containerized development:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "pytest", "tests/"]
```

```bash
# Build and run
docker build -t conflict-free-scheduling .
docker run -v $(pwd):/app conflict-free-scheduling
```

## Next Steps

After successful installation:

1. **Read the documentation**: Start with [README.md](../README.md)
2. **Run examples**: Check [EXAMPLES.md](./EXAMPLES.md)
3. **Understand algorithms**: Read [ALGORITHMS.md](./ALGORITHMS.md)
4. **Start developing**: See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [GitHub issues](https://github.com/yourusername/ConflictFreeScheduling/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Complete error message
   - Steps to reproduce

---

*This installation guide should get you up and running quickly. For development contributions, see the [Contributing Guidelines](./CONTRIBUTING.md).*
