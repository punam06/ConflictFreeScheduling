#!/usr/bin/env python3
"""
Debug Test Script for Conflict-Free Scheduling System

This script provides debugging utilities and quick tests to help identify
and resolve issues in the scheduling system.

Usage:
    python debug_test.py [options]
    
Options:
    --algorithm ALGO    Test specific algorithm (graph, dp, backtrack, genetic)
    --data FILE         Use specific data file
    --verbose           Enable verbose debugging output
    --profile           Enable performance profiling
"""

import sys
import os
import time
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scheduler import ConflictFreeScheduler, Activity
from utils.file_parser import FileParser
from utils.pdf_generator import PDFGenerator

def debug_print(message, verbose=True):
    """Print debug message if verbose mode is enabled"""
    if verbose:
        print(f"[DEBUG] {message}")

def test_basic_functionality(verbose=False):
    """Test basic system functionality"""
    debug_print("Testing basic functionality...", verbose)
    
    try:
        # Test Activity creation
        activity = Activity(1, 9, 10, 1.0, "Test Course", "Room 101")
        debug_print(f"Activity created: {activity}", verbose)
        
        # Test Scheduler creation
        scheduler = ConflictFreeScheduler()
        debug_print("Scheduler created successfully", verbose)
        
        # Test basic operations
        activities = [
            Activity(1, 9, 10, 1.0, "Math", "Room 101"),
            Activity(2, 10, 11, 1.0, "Physics", "Room 102"),
            Activity(3, 9, 10, 1.0, "Chemistry", "Room 103")
        ]
        
        # Test conflict detection
        has_conflict = scheduler.has_conflict(activities[0], activities[2])
        debug_print(f"Conflict detected between Math and Chemistry: {has_conflict}", verbose)
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        if verbose:
            traceback.print_exc()
        return False

def test_algorithms(algorithm=None, verbose=False):
    """Test scheduling algorithms"""
    debug_print(f"Testing algorithms (filter: {algorithm})...", verbose)
    
    # Load sample data
    try:
        activities = FileParser.parse_csv("data/demo_activities.csv")
        debug_print(f"Loaded {len(activities)} activities from demo data", verbose)
    except FileNotFoundError:
        debug_print("Demo data not found, generating sample data...", verbose)
        FileParser.generate_sample_data("data/demo_activities.csv", 10)
        activities = FileParser.parse_csv("data/demo_activities.csv")
    
    scheduler = ConflictFreeScheduler()
    results = {}
    
    algorithms_to_test = []
    if algorithm:
        algorithms_to_test = [algorithm]
    else:
        algorithms_to_test = ['graph', 'dp', 'backtrack', 'genetic']
    
    for algo in algorithms_to_test:
        debug_print(f"Testing {algo} algorithm...", verbose)
        
        try:
            start_time = time.time()
            
            if algo == 'graph':
                result = scheduler.graph_coloring_schedule(activities)
            elif algo == 'dp':
                result = scheduler.dp_schedule(activities)
            elif algo == 'backtrack':
                result = scheduler.backtracking_schedule(activities)
            elif algo == 'genetic':
                result = scheduler.genetic_algorithm_schedule(activities)
            else:
                print(f"❌ Unknown algorithm: {algo}")
                continue
                
            end_time = time.time()
            execution_time = end_time - start_time
            
            results[algo] = {
                'success': True,
                'activities': len(result),
                'time': execution_time
            }
            
            debug_print(f"✅ {algo} completed: {len(result)} activities in {execution_time:.3f}s", verbose)
            
        except Exception as e:
            results[algo] = {
                'success': False,
                'error': str(e),
                'time': 0
            }
            print(f"❌ {algo} algorithm failed: {e}")
            if verbose:
                traceback.print_exc()
    
    return results

def test_file_operations(verbose=False):
    """Test file parsing and generation"""
    debug_print("Testing file operations...", verbose)
    
    try:
        # Test CSV parsing
        if os.path.exists("data/demo_activities.csv"):
            activities = FileParser.parse_csv("data/demo_activities.csv")
            debug_print(f"✅ CSV parsing: {len(activities)} activities loaded", verbose)
        else:
            debug_print("Demo CSV not found, skipping CSV test", verbose)
        
        # Test JSON parsing
        if os.path.exists("data/demo_activities.json"):
            activities = FileParser.parse_json("data/demo_activities.json")
            debug_print(f"✅ JSON parsing: {len(activities)} activities loaded", verbose)
        else:
            debug_print("Demo JSON not found, skipping JSON test", verbose)
        
        # Test sample data generation
        test_file = "debug_sample.csv"
        success = FileParser.generate_sample_data(test_file, 5)
        if success and os.path.exists(test_file):
            debug_print("✅ Sample data generation successful", verbose)
            os.remove(test_file)  # Cleanup
        else:
            debug_print("❌ Sample data generation failed", verbose)
            
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        if verbose:
            traceback.print_exc()
        return False

def test_pdf_generation(verbose=False):
    """Test PDF generation capabilities"""
    debug_print("Testing PDF generation...", verbose)
    
    try:
        # Create sample activities
        activities = [
            Activity(1, 9, 10, 1.0, "Mathematics I", "Room 101"),
            Activity(2, 10, 11, 1.0, "Physics I", "Room 102"),
            Activity(3, 11, 12, 1.0, "Chemistry I", "Room 103")
        ]
        
        # Test PDF generation (using HTML output since that's what's available)
        pdf_gen = PDFGenerator()
        filename = "debug_test_schedule.html"
        
        success = pdf_gen.generate_schedule_html(activities, filename, "Debug Test Schedule")
        
        if success and os.path.exists(filename):
            debug_print("✅ HTML generation successful", verbose)
            # Keep the file for inspection
            debug_print(f"Generated HTML: {filename}", verbose)
            return True
        else:
            debug_print("❌ HTML generation failed", verbose)
            return False
            
    except Exception as e:
        print(f"❌ PDF generation test failed: {e}")
        if verbose:
            traceback.print_exc()
        return False

def profile_performance(algorithm='graph', verbose=False):
    """Profile algorithm performance with different dataset sizes"""
    debug_print(f"Profiling {algorithm} algorithm performance...", verbose)
    
    sizes = [10, 25, 50, 100]
    results = {}
    
    for size in sizes:
        debug_print(f"Testing with {size} activities...", verbose)
        
        # Generate sample data
        temp_file = f"debug_profile_{size}.csv"
        FileParser.generate_sample_data(temp_file, size)
        activities = FileParser.parse_csv(temp_file)
        
        scheduler = ConflictFreeScheduler()
        
        try:
            start_time = time.time()
            
            if algorithm == 'graph':
                result = scheduler.graph_coloring_schedule(activities)
            elif algorithm == 'dp':
                result = scheduler.dp_schedule(activities)
            elif algorithm == 'backtrack':
                result = scheduler.backtracking_schedule(activities)
            elif algorithm == 'genetic':
                result = scheduler.genetic_algorithm_schedule(activities)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            results[size] = {
                'time': execution_time,
                'scheduled': len(result),
                'success': True
            }
            
            debug_print(f"Size {size}: {execution_time:.3f}s, {len(result)} scheduled", verbose)
            
        except Exception as e:
            results[size] = {
                'time': 0,
                'scheduled': 0,
                'success': False,
                'error': str(e)
            }
            debug_print(f"Size {size}: Failed - {e}", verbose)
        
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return results

def run_comprehensive_debug():
    """Run comprehensive debugging tests"""
    print("🔧 Conflict-Free Scheduling System - Debug Test Suite")
    print("=" * 60)
    
    # Test results tracking
    tests_passed = 0
    total_tests = 0
    
    # Basic functionality test
    print("\n1. Basic Functionality Test")
    print("-" * 30)
    total_tests += 1
    if test_basic_functionality(verbose=True):
        print("✅ Basic functionality: PASSED")
        tests_passed += 1
    else:
        print("❌ Basic functionality: FAILED")
    
    # Algorithm tests
    print("\n2. Algorithm Tests")
    print("-" * 20)
    total_tests += 1
    algo_results = test_algorithms(verbose=True)
    all_algo_passed = all(result['success'] for result in algo_results.values())
    
    if all_algo_passed:
        print("✅ All algorithms: PASSED")
        tests_passed += 1
    else:
        print("❌ Some algorithms: FAILED")
    
    for algo, result in algo_results.items():
        if result['success']:
            print(f"  ✅ {algo}: {result['activities']} activities in {result['time']:.3f}s")
        else:
            print(f"  ❌ {algo}: {result.get('error', 'Unknown error')}")
    
    # File operations test
    print("\n3. File Operations Test")
    print("-" * 25)
    total_tests += 1
    if test_file_operations(verbose=True):
        print("✅ File operations: PASSED")
        tests_passed += 1
    else:
        print("❌ File operations: FAILED")
    
    # PDF generation test
    print("\n4. HTML Generation Test")
    print("-" * 24)
    total_tests += 1
    if test_pdf_generation(verbose=True):
        print("✅ HTML generation: PASSED")
        tests_passed += 1
    else:
        print("❌ HTML generation: FAILED")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🎯 Debug Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All systems operational!")
        return True
    else:
        print("❌ Some issues detected - check output above")
        return False

def main():
    """Main debug script entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Debug Test Script for Scheduling System")
    parser.add_argument('--algorithm', choices=['graph', 'dp', 'backtrack', 'genetic'],
                      help='Test specific algorithm')
    parser.add_argument('--data', help='Use specific data file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--profile', action='store_true', help='Enable performance profiling')
    parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive test suite')
    
    args = parser.parse_args()
    
    if args.comprehensive or len(sys.argv) == 1:
        # Run comprehensive tests if no specific options or --comprehensive flag
        return run_comprehensive_debug()
    
    if args.algorithm:
        print(f"Testing {args.algorithm} algorithm...")
        results = test_algorithms(args.algorithm, args.verbose)
        return all(result['success'] for result in results.values())
    
    if args.profile:
        algo = args.algorithm or 'graph'
        print(f"Profiling {algo} algorithm...")
        results = profile_performance(algo, args.verbose)
        
        print("\nPerformance Profile:")
        for size, result in results.items():
            if result['success']:
                print(f"  {size} activities: {result['time']:.3f}s ({result['scheduled']} scheduled)")
            else:
                print(f"  {size} activities: FAILED")
        
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Debug test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
