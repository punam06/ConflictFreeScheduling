#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Environment Setup Script for Conflict-Free Scheduling System

This script sets up the complete environment for the scheduling system:
1. Checks and installs required dependencies
2. Validates database configuration
3. Creates and initializes the database if needed
4. Ensures all components are working correctly
"""

import sys
import os
import subprocess
import importlib
import argparse
import platform


def check_python_version() -> bool:
    """Check if Python version is compatible"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python version {python_version.major}.{python_version.minor} is not supported")
        print("Please use Python 3.8 or higher")
        return False
    
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    return True


def check_and_install_dependencies() -> bool:
    """Check and install required dependencies"""
    print("\n📦 Checking required dependencies...")
    
    # Required packages
    required_packages = [
        "pandas",
        "numpy",
        "sqlalchemy",
        "pymysql",
        "reportlab",
        "weasyprint",
        "flask",
        "pytest",
    ]
    
    # Check each package
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        
        cmd = [sys.executable, "-m", "pip", "install"] + missing_packages
        try:
            subprocess.check_call(cmd)
            print("✅ All dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install some dependencies")
            print("Please install them manually using:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True


def check_database_connection(host: str, user: str, password: str, port: int) -> bool:
    """Check database connection"""
    try:
        import pymysql
        
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        conn.close()
        
        print("✅ Database connection successful")
        return True
    except ImportError:
        print("❌ PyMySQL is not installed")
        print("Please run: pip install pymysql")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your MySQL credentials")
        return False


def create_database_if_needed(host: str, user: str, password: str, database: str, port: int) -> bool:
    """Create the database if it doesn't exist"""
    try:
        import pymysql
        
        # Connect to MySQL server
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        # Create cursor
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if database.lower() in databases:
            print(f"✅ Database '{database}' already exists")
        else:
            print(f"📊 Creating database '{database}'...")
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"✅ Database '{database}' created successfully")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False


def main():
    """Main environment setup function"""
    print("=" * 60)
    print("=== Environment Setup for Conflict-Free Scheduling System ===")
    print("=" * 60)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Set up environment for scheduling system",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Database options
    parser.add_argument('--host', default='localhost', help='MySQL host')
    parser.add_argument('--database', default='conflict_free_scheduling', 
                       help='Database name')
    parser.add_argument('--user', default='root', help='MySQL username')
    parser.add_argument('--password', default='', help='MySQL password')
    parser.add_argument('--port', type=int, default=3306, help='MySQL port')
    parser.add_argument('--no-db', action='store_true', 
                       help='Skip database setup')
    parser.add_argument('--skip-dependencies', action='store_true',
                       help='Skip dependency installation')
    
    args = parser.parse_args()
    
    # System information
    print("\n🖥️  System Information:")
    print(f"OS: {platform.platform()}")
    if not check_python_version():
        return 1
    
    # Dependency check
    if not args.skip_dependencies:
        if not check_and_install_dependencies():
            return 1
    
    # Database setup
    if not args.no_db:
        print("\n🗄️  Database Setup:")
        if not check_database_connection(args.host, args.user, args.password, args.port):
            print("⚠️  Skipping database creation due to connection issues")
        else:
            if not create_database_if_needed(args.host, args.user, args.password, args.database, args.port):
                print("⚠️  Skipping database initialization")
            else:
                # Run the database initialization script
                script_path = os.path.join(os.path.dirname(__file__), "initialize_database.py")
                if os.path.exists(script_path):
                    print("\n🔄 Running database initialization script...")
                    cmd = [
                        sys.executable, script_path,
                        "--host", args.host,
                        "--database", args.database,
                        "--user", args.user,
                        "--port", str(args.port),
                        "--sample-data"
                    ]
                    
                    if args.password:
                        cmd.extend(["--password", args.password])
                    
                    try:
                        subprocess.check_call(cmd)
                    except subprocess.CalledProcessError:
                        print("❌ Database initialization failed")
                        return 1
                else:
                    print("❌ Database initialization script not found")
                    print(f"Expected path: {script_path}")
                    return 1
    
    print("\n✅ Environment setup complete!")
    print("You can now run the scheduling system with:")
    print("python main.py --use-database")
    return 0


if __name__ == "__main__":
    sys.exit(main())
