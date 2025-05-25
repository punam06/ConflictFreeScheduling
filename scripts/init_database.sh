#!/bin/bash

# Database Initialization Script for Conflict-Free Scheduling System
# This script sets up the SQLite database with schema and sample data

DB_PATH="data/scheduling.db"
SCHEMA_FILE="data/schema.sql"
SAMPLE_DATA_FILE="data/updated_sample_data.sql"

echo "=== Conflict-Free Scheduling Database Setup ==="

# Check if required files exist
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Error: Schema file not found: $SCHEMA_FILE"
    exit 1
fi

if [ ! -f "$SAMPLE_DATA_FILE" ]; then
    echo "Error: Sample data file not found: $SAMPLE_DATA_FILE"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

# Remove existing database if it exists
if [ -f "$DB_PATH" ]; then
    echo "Removing existing database..."
    rm "$DB_PATH"
fi

# Create new database with schema
echo "Creating database schema..."
sqlite3 "$DB_PATH" < "$SCHEMA_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Database schema created successfully"
else
    echo "✗ Failed to create database schema"
    exit 1
fi

# Load sample data
echo "Loading sample data..."
sqlite3 "$DB_PATH" < "$SAMPLE_DATA_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Sample data loaded successfully"
else
    echo "✗ Failed to load sample data"
    exit 1
fi

# Display database statistics
echo ""
echo "=== Database Statistics ==="
echo -n "Courses: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM courses;"

echo -n "Rooms: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM classrooms;"

echo -n "Time Slots: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM time_slots;"

echo -n "Schedule Assignments: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM schedule;"

echo ""
echo "✓ Database setup complete!"
echo "Database location: $DB_PATH"
echo ""
echo "You can now run the scheduler with:"
echo "  ./build/scheduler --algorithm greedy"
echo "  ./build/scheduler --init-db"
