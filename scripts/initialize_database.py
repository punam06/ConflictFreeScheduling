#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Initialization Script for Conflict-Free Scheduling System

This script initializes the database with necessary tables and sample data.
Run this script before using the scheduling system with database features.
"""

import sys
import os
import argparse

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.database.database_manager import DatabaseManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies: pip install sqlalchemy pymysql")
    sys.exit(1)


def main():
    """Main database initialization function"""
    print("=" * 50)
    print("=== Database Initialization for Scheduling System ===")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(
        description="Initialize database for scheduling system",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--host', default='localhost', help='MySQL host')
    parser.add_argument('--database', default='conflict_free_scheduling', 
                     help='Database name')
    parser.add_argument('--user', default='root', help='MySQL username')
    parser.add_argument('--password', default='', help='MySQL password')
    parser.add_argument('--port', type=int, default=3306, help='MySQL port')
    parser.add_argument('--force', action='store_true', 
                     help='Force recreate tables even if they exist')
    parser.add_argument('--sample-data', action='store_true', 
                     help='Load sample data after initialization')
    
    args = parser.parse_args()
    
    # Initialize database manager
    print(f"🔄 Connecting to MySQL at {args.host}...")
    db_manager = DatabaseManager(
        host=args.host,
        database=args.database,
        user=args.user,
        password=args.password,
        port=args.port
    )
    
    # Initialize database schema
    print("📊 Creating database schema...")
    if not db_manager.initialize():
        print("❌ Failed to initialize database schema")
        return 1
    
    # Load sample data if requested
    if args.sample_data:
        print("📊 Loading sample data...")
        if not db_manager.load_sample_data():
            print("❌ Failed to load sample data")
            return 1
        
        print("✅ Sample data loaded successfully")
    
    print("\n✅ Database initialization complete!")
    print(f"Database '{args.database}' is ready for use with the scheduling system")
    return 0


if __name__ == "__main__":
    sys.exit(main())
