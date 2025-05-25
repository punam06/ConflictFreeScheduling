#!/bin/bash
# Run script for Enhanced Routine Generator

# Define base directory
BASE_DIR="/Users/punam/Desktop/Varsity/2-2/Algo/project/git new deploy/ConflictFreeScheduling"

# Create output directory if it doesn't exist
mkdir -p "$BASE_DIR/output"
chmod 755 "$BASE_DIR/output"

# Navigate to build directory
cd "$BASE_DIR/build"

# Initialize database with fresh sample data
echo "Initializing database with sample data..."
./scheduler --init-db

# Run enhanced generator with comprehensive routine output
echo "Running enhanced generator with comprehensive routine output..."
./scheduler --enhanced-generator --comprehensive-routine --output "$BASE_DIR/output/enhanced_schedule"

echo "Process complete! Check the output directory for the generated PDF files."
