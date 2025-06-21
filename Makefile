# Makefile for Conflict-Free Scheduling System (Python)

.PHONY: help install test clean run demo pdf academic all lint format

# Default target
help:
	@echo "Conflict-Free Scheduling System - Available Commands:"
	@echo "===================================================="
	@echo "  install     - Install Python dependencies"
	@echo "  test        - Run unit tests"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean generated files"
	@echo "  run         - Run basic scheduling algorithm"
	@echo "  demo        - Run demonstration script"
	@echo "  pdf         - Generate PDF output"
	@echo "  academic    - Generate academic PDF schedule"
	@echo "  all         - Run all algorithms and compare"
	@echo "  sample      - Generate sample data"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make run"
	@echo "  make demo"
	@echo "  make academic"

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully"

# Run tests
test:
	@echo "🧪 Running unit tests..."
	python3 -m pytest tests/ -v || python3 -m unittest discover tests/ -v

# Lint code
lint:
	@echo "🔍 Running code linting..."
	python3 -m flake8 src/ tests/ --max-line-length=88 --exclude=__pycache__

# Format code
format:
	@echo "🎨 Formatting code..."
	python3 -m black src/ tests/ *.py

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf output/*.html output/*.pdf
	rm -rf data/sample_activities.csv data/demo_activities.*
	rm -rf __pycache__/ src/__pycache__/ src/*/__pycache__/ tests/__pycache__/
	rm -rf .pytest_cache/ *.pyc
	@echo "✅ Cleaned successfully"

# Run basic scheduling
run:
	@echo "🔄 Running basic graph coloring algorithm..."
	python3 main.py --algorithm graph-coloring

# Run demonstration
demo:
	@echo "🎭 Running demonstration script..."
	python3 demo.py

# Generate PDF
pdf:
	@echo "📄 Generating PDF output..."
	python3 main.py --algorithm graph-coloring --pdf

# Generate academic PDF
academic:
	@echo "🎓 Generating academic PDF schedule..."
	python3 main.py --algorithm graph-coloring --academic-pdf --batch BCSE24 --section A

# Run all algorithms
all:
	@echo "🚀 Running all algorithms for comparison..."
	python3 main.py --run-all --visualize

# Generate sample data
sample:
	@echo "📝 Generating sample data..."
	python3 -c "import sys; sys.path.append('src'); from utils.file_parser import FileParser; FileParser.generate_sample_data('data/sample_activities.csv', 15); print('✅ Sample data generated')"

# Setup development environment
dev-setup: install
	@echo "🔧 Setting up development environment..."
	python3 -m pip install pytest pytest-cov flake8 black
	@echo "✅ Development environment ready"

# Quick start (install + demo)
quickstart: install demo
	@echo "🚀 Quick start completed!"

# Build distribution package
build:
	@echo "📦 Building distribution package..."
	python3 setup.py sdist bdist_wheel
	@echo "✅ Package built in dist/"

# Install in development mode
dev-install:
	@echo "🔧 Installing in development mode..."
	python3 -m pip install -e .
	@echo "✅ Installed in development mode"

# Check system requirements
check:
	@echo "🔍 Checking system requirements..."
	@python3 --version
	@echo "Python: ✅"
	@which python3 >/dev/null && echo "Python3 path: $(which python3)"
	@python3 -c "import sys; print(f'Python version: {sys.version}')"
	@echo "System check completed"
