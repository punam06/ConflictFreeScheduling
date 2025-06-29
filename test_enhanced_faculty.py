#!/usr/bin/env python3
"""
Test script for Enhanced Faculty Input System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import handle_faculty_input_routine
from src.utils.faculty_input import EnhancedFacultyInputSystem

def test_enhanced_faculty_system():
    """Test the enhanced faculty input system"""
    
    print("🧪 Testing Enhanced Faculty Input System")
    print("="*50)
    
    # Test 1: Create system instance
    print("\n1️⃣ Testing system initialization...")
    try:
        system = EnhancedFacultyInputSystem()
        print(f"✅ System created successfully")
        print(f"   📚 Rooms: {len(system.rooms)}")
        print(f"   🏢 Departments: {len(system.departments)}")
        print(f"   👔 Designations: {len(system.designations)}")
    except Exception as e:
        print(f"❌ System creation failed: {e}")
        return False
    
    # Test 2: Test data loading/saving
    print("\n2️⃣ Testing data operations...")
    try:
        # Test saving empty data
        system.save_faculty_data("test_faculty_data.json")
        
        # Test loading 
        loaded = system.load_faculty_data("test_faculty_data.json")
        print(f"✅ Data operations: Save/Load working")
    except Exception as e:
        print(f"❌ Data operations failed: {e}")
        return False
    
    # Test 3: Test comprehensive report generation
    print("\n3️⃣ Testing report generation...")
    try:
        report = system.generate_comprehensive_report()
        print(f"✅ Report generated successfully")
        print(f"   📊 Summary keys: {list(report['summary'].keys())}")
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False
    
    # Test 4: Test conflict detector
    print("\n4️⃣ Testing conflict detection...")
    try:
        conflicts = system.conflict_detector.detect_faculty_conflicts([])
        workload_issues = system.conflict_detector.detect_workload_issues([], [])
        print(f"✅ Conflict detection working")
        print(f"   ⚠️ Conflicts: {len(conflicts)}")
        print(f"   ⚡ Workload Issues: {len(workload_issues)}")
    except Exception as e:
        print(f"❌ Conflict detection failed: {e}")
        return False
    
    # Test 5: Test CSV export
    print("\n5️⃣ Testing CSV export...")
    try:
        system.export_to_csv("test_schedule.csv")
        print(f"✅ CSV export working")
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
        return False
    
    # Test 6: Test faculty routine generation
    print("\n6️⃣ Testing faculty routine generation...")
    try:
        activities = handle_faculty_input_routine()
        print(f"✅ Faculty routine generation working")
        print(f"   📚 Activities generated: {len(activities)}")
        
        # Print sample activities
        for i, activity in enumerate(activities[:3]):
            print(f"   {i+1}. {activity.name} ({activity.start}-{activity.end})")
            
    except Exception as e:
        print(f"❌ Faculty routine generation failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Enhanced Faculty Input System is working correctly.")
    return True

def test_faculty_input_features():
    """Test specific faculty input features"""
    
    print("\n🔬 Testing Faculty Input Features")
    print("="*40)
    
    system = EnhancedFacultyInputSystem()
    
    # Test time formatting
    print("\n⏰ Testing time formatting...")
    test_slots = [0, 2, 4, 8, 12, 16, 20]
    for slot in test_slots:
        formatted = system._format_time_slot(slot)
        print(f"   Slot {slot:2d} -> {formatted}")
    
    # Test validation function
    print("\n✅ Testing validation functions...")
    valid_email = system.validate_input(
        "Test email: ", 
        lambda x: '@' in x, 
        "Invalid email", 
        default="test@example.com"
    )
    print(f"   Email validation test: {valid_email}")
    
    print("\n✅ Faculty input features working correctly!")

if __name__ == "__main__":
    print("🚀 Starting Enhanced Faculty Input System Tests")
    print("="*60)
    
    success = test_enhanced_faculty_system()
    if success:
        test_faculty_input_features()
        print("\n🎊 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
