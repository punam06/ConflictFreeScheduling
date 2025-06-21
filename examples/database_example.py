#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Integration Example for Conflict-Free Scheduling System

This example demonstrates how to use the database functionality
of the scheduling system.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from database.database_manager import DatabaseManager, Activity
    from scheduler import ConflictFreeScheduler
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies: pip install sqlalchemy pymysql")
    sys.exit(1)


def main():
    """Main database example function"""
    print("=== Database Integration Example ===")
    
    # Initialize database manager
    print("🔄 Initializing database...")
    db_manager = DatabaseManager(
        host="localhost",
        database="conflict_free_scheduling",
        user="root",
        password=""  # Update with your MySQL password
    )
    
    # Initialize database with sample data
    print("📊 Setting up database with sample data...")
    if not db_manager.initialize_with_sample_data():
        print("❌ Failed to initialize database")
        print("Make sure MySQL is running and you have the correct credentials")
        return 1
    
    print("✅ Database initialized successfully")
    
    # Get database statistics
    print("\n=== Database Statistics ===")
    try:
        session = db_manager.Session()
        
        # Count records
        from database.database_manager import Batch, Teacher, Classroom, Course
        
        batch_count = session.query(Batch).count()
        teacher_count = session.query(Teacher).count()
        room_count = session.query(Classroom).count()
        course_count = session.query(Course).count()
        
        print(f"Total Batches: {batch_count}")
        print(f"Total Teachers: {teacher_count}")
        print(f"Total Rooms: {room_count}")
        print(f"Total Courses: {course_count}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return 1
    
    # Get all courses as activities
    print("\n=== Course List ===")
    activities = db_manager.get_all_courses()
    
    if activities:
        print(f"Found {len(activities)} courses:")
        for i, activity in enumerate(activities[:5]):  # Show first 5
            print(f"  {i+1}. {activity.name} (Weight: {activity.weight}, Duration: {activity.end - activity.start})")
        
        if len(activities) > 5:
            print(f"  ... and {len(activities) - 5} more courses")
    else:
        print("No courses found in database")
        return 1
    
    # Test scheduling with database data
    print("\n=== Scheduling with Database Data ===")
    scheduler = ConflictFreeScheduler()
    
    # Run graph coloring algorithm
    print("🔄 Running Graph Coloring algorithm...")
    scheduled = scheduler.graph_coloring_schedule(activities)
    
    if scheduled:
        total_weight = scheduler.calculate_total_weight(scheduled)
        efficiency = (len(scheduled) / len(activities)) * 100
        
        print(f"✅ Scheduled {len(scheduled)}/{len(activities)} courses")
        print(f"📊 Total credit hours: {total_weight:.1f}")
        print(f"📈 Efficiency: {efficiency:.1f}%")
        
        # Show first few scheduled courses
        print("\nScheduled courses:")
        for i, activity in enumerate(scheduled[:3]):
            print(f"  {i+1}. {activity.name} - Time: {activity.start}-{activity.end}")
        
        if len(scheduled) > 3:
            print(f"  ... and {len(scheduled) - 3} more")
    else:
        print("❌ No courses could be scheduled")
    
    # Test batch-specific scheduling
    print("\n=== Batch-Specific Scheduling ===")
    batch_activities = db_manager.get_courses_by_batch("BCSE24")
    
    if batch_activities:
        print(f"Found {len(batch_activities)} courses for BCSE24")
        batch_scheduled = scheduler.graph_coloring_schedule(batch_activities)
        batch_weight = scheduler.calculate_total_weight(batch_scheduled)
        
        print(f"✅ Scheduled {len(batch_scheduled)} BCSE24 courses")
        print(f"📊 Total credit hours: {batch_weight:.1f}")
    else:
        print("No courses found for BCSE24")
    
    # Close database connection
    db_manager.close()
    print("\n✅ Database example completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
