#!/bin/bash

# Conflict-Free Scheduling System - Run Script
# This script provides easy access to common operations

echo "=== Conflict-Free Scheduling System ==="
echo "======================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  basic       - Run basic graph coloring algorithm (generates academic PDF by default)"
    echo "  all         - Run all 4 algorithms and compare"
    echo "  pdf         - Generate basic PDF output instead of academic PDF"
    echo "  academic    - Generate academic PDF schedule for a specific batch"
    echo "  setup       - Set up environment (dependencies, database, etc.)"
    echo "  database    - Initialize database and run"
    echo "  demo        - Run integrated demonstration of all components"
    echo "  tutorial    - Open interactive Jupyter notebook tutorial"
    echo "  sample      - Generate sample data"
    echo "  test        - Run unit tests"
    echo "  install     - Install dependencies"
    echo "  clean       - Clean output files"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 basic"
    echo "  $0 all"
    echo "  $0 academic"
    echo "  $0 setup"
    echo "  $0 demo"
    echo "  $0 tutorial"
    echo ""
}

# Function to install dependencies
install_deps() {
    echo "📦 Installing Python dependencies..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo "✅ Dependencies installed successfully"
}

# Function to set up full environment
setup_environment() {
    echo "🔧 Setting up complete environment..."
    python3 scripts/setup_environment.py "$@"
}

# Function to run tests
run_tests() {
    echo "🧪 Running unit tests..."
    if command -v pytest &> /dev/null; then
        python3 -m pytest tests/ -v
    else
        python3 -m unittest discover tests/ -v
    fi
}

# Function to clean output files
clean_output() {
    echo "🧹 Cleaning output files..."
    rm -rf output/*.html
    rm -rf output/*.pdf
    rm -rf data/sample_activities.csv
    rm -rf __pycache__/
    rm -rf src/__pycache__/
    rm -rf src/*/__pycache__/
    rm -rf tests/__pycache__/
    echo "✅ Output files cleaned"
}

# Function to generate sample data
generate_sample() {
    echo "📝 Generating sample data..."
    python3 -c "
import sys
import os
sys.path.append('src')
from utils.file_parser import FileParser
FileParser.generate_sample_data('data/sample_activities.csv', 15)
print('✅ Sample data generated in data/sample_activities.csv')
"
}

# Main script logic
case "$1" in
    "basic")
        echo "🔄 Running basic graph coloring algorithm..."
        python3 main.py --algorithm graph-coloring
        ;;
    "all")
        echo "🚀 Running all algorithms for comparison..."
        python3 main.py --run-all --visualize
        ;;
    "setup")
        echo "🔧 Setting up complete environment..."
        shift
        setup_environment "$@" 
        ;;
    "pdf")
        echo "📄 Generating basic PDF output..."
        python3 main.py --algorithm graph-coloring --pdf
        ;;
    "academic")
        echo "🎓 Generating academic PDF schedule..."
        python3 main.py --algorithm graph-coloring --batch BCSE24 --section A
        ;;
    "database")
        echo "🗄️ Initializing database and running..."
        python3 scripts/initialize_database.py --sample-data
        echo "🔄 Running with database..."
        python3 main.py --use-database
        ;;
    "demo")
        echo "🎮 Running integrated demonstration..."
        python3 integrated_demo.py
        ;;
    "tutorial")
        echo "📘 Opening interactive tutorial..."
        jupyter notebook tutorial.ipynb
        ;;
    "sample")
        generate_sample
        ;;
    "test")
        run_tests
        ;;
    "install")
        install_deps
        ;;
    "clean")
        clean_output
        ;;
    "help"|"--help"|"-h")
        show_usage
        ;;
    "")
        echo "❓ No option provided."
        show_usage
        ;;
    *)
        echo "❌ Unknown option: $1"
        show_usage
        exit 1
        ;;
esac
