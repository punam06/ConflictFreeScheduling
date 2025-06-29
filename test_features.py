#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify all 4 core features are working
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and capture output"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Test all 4 core features"""
    print("🧪 Testing Conflict-Free Scheduling System Features")
    print("=" * 60)
    
    # Change to the project directory
    os.chdir("d:\\Code\\Projects\\Punam\\conflictFreeScheduling")
    
    features = [
        ("python main.py --algorithm graph-coloring", "Feature 1: Graph Coloring Algorithm"),
        ("python main.py --algorithm dynamic-prog", "Feature 1: Dynamic Programming Algorithm"),
        ("python main.py --algorithm backtracking", "Feature 1: Backtracking Algorithm"),
        ("python main.py --algorithm genetic", "Feature 1: Genetic Algorithm"),
        ("python main.py --run-all", "Feature 2: Run All Algorithms"),
        ("python main.py --comprehensive --no-database", "Feature 3: Comprehensive Routine"),
        ("python main.py --academic-routine", "Feature 4: Academic Routine"),
    ]
    
    results = []
    
    for cmd, description in features:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY OF TESTS")
    print("="*60)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Check if output files were generated
    output_dir = "output"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"\nGenerated files in output directory: {len(files)}")
        for file in files:
            print(f"  📄 {file}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
