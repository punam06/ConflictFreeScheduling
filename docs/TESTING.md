# Testing Guide

Comprehensive testing strategy for the Conflict-Free Scheduling project.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Categories](#test-categories)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Performance Testing](#performance-testing)
- [Test Coverage](#test-coverage)

## Testing Philosophy

Our testing approach follows these principles:

1. **Correctness**: Algorithms produce mathematically correct results
2. **Performance**: Algorithms meet expected time/space complexity
3. **Robustness**: Graceful handling of edge cases and invalid inputs
4. **Maintainability**: Tests are clear, well-documented, and easy to update

## Test Categories

### 1. Unit Tests

Test individual functions and components in isolation.

**Location**: `tests/unit/`

**Example**:
```python
# tests/unit/test_greedy.py
import pytest
from src.algorithms.greedy import greedy_activity_selection

class TestGreedyAlgorithm:
    def test_empty_input(self):
        """Test with empty activity list."""
        result = greedy_activity_selection([])
        assert result == []
    
    def test_single_activity(self):
        """Test with single activity."""
        activities = [(1, 3)]
        result = greedy_activity_selection(activities)
        assert result == [0]
    
    def test_classic_example(self):
        """Test with textbook example."""
        activities = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]
        result = greedy_activity_selection(activities)
        expected = [0, 3, 4]  # Activities at indices 0, 3, 4
        assert result == expected
    
    @pytest.mark.parametrize("activities,expected", [
        ([(1, 2), (3, 4), (5, 6)], [0, 1, 2]),  # Non-overlapping
        ([(1, 5), (2, 4), (3, 6)], [1]),        # All overlapping
        ([(0, 1), (1, 2), (2, 3)], [0, 1, 2]),  # Adjacent activities
    ])
    def test_various_scenarios(self, activities, expected):
        """Test various activity arrangements."""
        result = greedy_activity_selection(activities)
        assert result == expected
```

### 2. Integration Tests

Test interactions between multiple components.

**Location**: `tests/integration/`

**Example**:
```python
# tests/integration/test_algorithm_comparison.py
import pytest
from src.algorithms.greedy import greedy_activity_selection
from src.algorithms.dynamic_programming import dp_activity_selection
from src.utils.data_generator import generate_random_activities

class TestAlgorithmComparison:
    def test_unweighted_consistency(self):
        """Test that greedy and DP give same results for unweighted problems."""
        activities = generate_random_activities(20, seed=42)
        
        greedy_result = greedy_activity_selection(activities)
        dp_result = dp_activity_selection(activities)
        
        # Both should select same number of activities for unweighted case
        assert len(greedy_result) == len(dp_result)
    
    def test_weighted_optimality(self):
        """Test that DP finds better solutions for weighted problems."""
        activities = [(1, 3), (2, 4)]
        weights = [1, 10]  # Second activity has much higher weight
        
        greedy_result = greedy_activity_selection(activities)
        dp_result, dp_weight = dp_activity_selection(activities, weights)
        
        # DP should select the higher-weight activity
        assert dp_weight >= sum(weights[i] for i in greedy_result)
```

### 3. Property-Based Tests

Use hypothesis to generate test cases automatically.

**Install**: `pip install hypothesis`

**Example**:
```python
# tests/property/test_properties.py
from hypothesis import given, strategies as st
from src.algorithms.greedy import greedy_activity_selection

@given(st.lists(
    st.tuples(
        st.integers(min_value=0, max_value=100),  # start time
        st.integers(min_value=1, max_value=101)   # end time
    ).filter(lambda x: x[0] < x[1])  # ensure start < end
))
def test_greedy_properties(activities):
    """Property-based test for greedy algorithm."""
    result = greedy_activity_selection(activities)
    
    # Property 1: Result should not have more activities than input
    assert len(result) <= len(activities)
    
    # Property 2: All indices should be valid
    for idx in result:
        assert 0 <= idx < len(activities)
    
    # Property 3: Selected activities should not overlap
    if len(result) > 1:
        for i in range(len(result) - 1):
            current_end = activities[result[i]][1]
            next_start = activities[result[i + 1]][0]
            assert current_end <= next_start

@given(st.integers(min_value=1, max_value=100))
def test_performance_scaling(n):
    """Test that performance scales as expected."""
    import time
    activities = [(i, i + 1) for i in range(n)]
    
    start_time = time.time()
    result = greedy_activity_selection(activities)
    execution_time = time.time() - start_time
    
    # Should complete quickly for reasonable input sizes
    assert execution_time < 1.0  # 1 second max
    assert len(result) == n  # Should select all non-overlapping activities
```

### 4. Performance Tests

Measure and verify algorithm performance characteristics.

**Location**: `tests/performance/`

**Example**:
```python
# tests/performance/test_complexity.py
import time
import pytest
from src.algorithms.greedy import greedy_activity_selection
from src.utils.data_generator import generate_random_activities

class TestPerformanceComplexity:
    @pytest.mark.performance
    def test_time_complexity_scaling(self):
        """Verify O(n log n) time complexity for greedy algorithm."""
        sizes = [100, 200, 400, 800]
        times = []
        
        for size in sizes:
            activities = generate_random_activities(size, seed=42)
            
            # Measure execution time
            start = time.time()
            result = greedy_activity_selection(activities)
            elapsed = time.time() - start
            
            times.append(elapsed)
        
        # Check scaling behavior
        # For O(n log n), doubling size should roughly double time
        for i in range(len(times) - 1):
            ratio = times[i + 1] / times[i] if times[i] > 0 else 1
            assert 1.0 < ratio < 3.0  # Allow some variance
    
    @pytest.mark.performance
    def test_memory_usage(self):
        """Test memory usage remains reasonable."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Measure memory before
        mem_before = process.memory_info().rss
        
        # Generate large dataset
        large_activities = generate_random_activities(10000)
        result = greedy_activity_selection(large_activities)
        
        # Measure memory after
        mem_after = process.memory_info().rss
        memory_used = (mem_after - mem_before) / (1024 * 1024)  # MB
        
        # Should not use excessive memory
        assert memory_used < 100  # Less than 100 MB
```

### 5. Edge Case Tests

Test boundary conditions and error cases.

**Example**:
```python
# tests/edge_cases/test_edge_cases.py
import pytest
from src.algorithms.greedy import greedy_activity_selection

class TestEdgeCases:
    def test_zero_duration_activities(self):
        """Test activities with zero duration."""
        activities = [(1, 1), (2, 2), (3, 3)]
        result = greedy_activity_selection(activities)
        # Should handle gracefully (likely select all)
        assert isinstance(result, list)
    
    def test_negative_times(self):
        """Test with negative start/end times."""
        activities = [(-5, -3), (-2, 0), (1, 3)]
        result = greedy_activity_selection(activities)
        assert len(result) <= 3
    
    def test_large_time_values(self):
        """Test with very large time values."""
        activities = [(10**9, 10**9 + 1), (10**9 + 2, 10**9 + 3)]
        result = greedy_activity_selection(activities)
        assert result == [0, 1]
    
    def test_identical_activities(self):
        """Test with multiple identical activities."""
        activities = [(1, 3), (1, 3), (1, 3)]
        result = greedy_activity_selection(activities)
        assert len(result) == 1  # Should select only one
    
    def test_floating_point_times(self):
        """Test with floating-point time values."""
        activities = [(1.5, 2.5), (2.0, 3.0), (2.5, 3.5)]
        result = greedy_activity_selection(activities)
        # Should handle floating-point comparison correctly
        assert len(result) >= 1
```

## Running Tests

### Basic Test Execution

```bash
# Build and run all tests
make test

# Or using CMake
cd build
make test
./run_tests

# Run with verbose output
./run_tests --verbose

# Run specific test file
./run_tests --filter="test_greedy"

# Run specific test category
./run_tests --filter="unit"
```

### Test Categories

```bash
# Run only unit tests
./run_tests --filter="unit"

# Run only performance tests
./run_tests --filter="performance"
pytest -m performance

# Skip performance tests
pytest -m "not performance"

# Run integration tests
pytest tests/integration/
```

### Test Configuration

Create `pytest.ini`:

```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html
testpaths = tests
markers =
    performance: marks tests as performance tests (deselect with '-m "not performance"')
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### Continuous Integration

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_example():
    # Arrange: Set up test data and conditions
    activities = [(1, 4), (3, 5), (0, 6)]
    expected_result = [1, 3]
    
    # Act: Execute the function under test
    result = greedy_activity_selection(activities)
    
    # Assert: Verify the result
    assert result == expected_result
```

### Test Naming Conventions

- Use descriptive names: `test_should_select_all_when_non_overlapping`
- Include the scenario: `test_empty_input`, `test_single_activity`
- Be specific: `test_greedy_selects_optimal_for_unweighted_case`

### Fixtures for Test Data

```python
# conftest.py
import pytest

@pytest.fixture
def sample_activities():
    """Standard test activities used across multiple tests."""
    return [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]

@pytest.fixture
def weighted_activities():
    """Activities with weights for testing weighted algorithms."""
    activities = [(1, 3), (2, 4), (3, 5)]
    weights = [10, 20, 15]
    return activities, weights

@pytest.fixture
def large_dataset():
    """Large dataset for performance testing."""
    from src.utils.data_generator import generate_random_activities
    return generate_random_activities(1000, seed=42)

# Usage in tests
def test_with_fixture(sample_activities):
    result = greedy_activity_selection(sample_activities)
    assert len(result) >= 1
```

### Parameterized Tests

```python
@pytest.mark.parametrize("activities,expected_count", [
    ([(1, 2), (3, 4), (5, 6)], 3),  # Non-overlapping
    ([(1, 5), (2, 4), (3, 6)], 1),  # All overlapping
    ([(0, 2), (1, 3), (4, 6)], 2),  # Partially overlapping
])
def test_activity_selection_scenarios(activities, expected_count):
    result = greedy_activity_selection(activities)
    assert len(result) == expected_count
```

## Test Coverage

### Measuring Coverage

```bash
# Run tests with coverage
pytest --cov=src

# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Coverage Goals

- **Line Coverage**: Aim for 90%+ line coverage
- **Branch Coverage**: Test all conditional branches
- **Function Coverage**: Every function should be tested

### Coverage Configuration

Create `.coveragerc`:

```ini
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Test Data Management

### Generating Test Data

```python
# src/utils/test_data.py
def create_course_schedule_data():
    """Generate realistic course scheduling data."""
    courses = [
        ("Data Structures", 9, 11, 50),
        ("Algorithms", 10, 12, 45),
        ("Database Systems", 13, 15, 40),
        ("Computer Networks", 14, 16, 35),
        ("Software Engineering", 16, 18, 30),
    ]
    
    activities = [(start, end) for _, start, end, _ in courses]
    weights = [students for _, _, _, students in courses]
    
    return activities, weights, courses

def create_stress_test_data(n):
    """Generate data that stresses the algorithm."""
    # All activities overlap maximally
    return [(0, n) for _ in range(n)]

def create_best_case_data(n):
    """Generate best-case data (no overlaps)."""
    return [(i, i + 1) for i in range(n)]
```

### Mock Data for Testing

```python
from unittest.mock import Mock, patch

def test_with_mocked_data():
    """Test using mocked external data source."""
    mock_data = [(1, 3), (2, 4), (5, 6)]
    
    with patch('src.utils.data_loader.load_from_file') as mock_load:
        mock_load.return_value = mock_data
        
        # Test code that uses load_from_file
        result = some_function_that_loads_data('fake_file.csv')
        assert len(result) == 3
```

## Debugging Tests

### Test Debugging Tips

1. **Use descriptive assertions**:
   ```python
   # Good
   assert len(result) == 3, f"Expected 3 activities, got {len(result)}: {result}"
   
   # Better
   assert result == expected, f"Algorithm failed. Expected: {expected}, Got: {result}"
   ```

2. **Print debugging information**:
   ```python
   def test_debug_example():
       activities = [(1, 4), (3, 5)]
       print(f"Input: {activities}")
       
       result = greedy_activity_selection(activities)
       print(f"Output: {result}")
       
       assert len(result) == 1
   ```

3. **Use pytest's debugging features**:
   ```bash
   # Drop into debugger on failure
   pytest --pdb
   
   # Drop into debugger on first failure
   pytest -x --pdb
   
   # Show local variables in traceback
   pytest -l
   ```

### Performance Debugging

```python
import cProfile
import pstats

def profile_algorithm(algorithm_func, activities):
    """Profile algorithm performance."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = algorithm_func(activities)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
    
    return result
```

## Testing Best Practices

### 1. Test Independence

Each test should be independent and not rely on other tests:

```python
# Good - independent tests
def test_empty_list():
    assert greedy_activity_selection([]) == []

def test_single_activity():
    assert greedy_activity_selection([(1, 3)]) == [0]

# Bad - tests depend on each other
class TestState:
    def __init__(self):
        self.activities = []
    
    def test_add_activity(self):
        self.activities.append((1, 3))
        assert len(self.activities) == 1
    
    def test_schedule_activities(self):  # Depends on previous test
        result = greedy_activity_selection(self.activities)
        assert result == [0]
```

### 2. Clear Test Names

```python
# Good - descriptive names
def test_greedy_selects_non_overlapping_activities()
def test_dp_handles_weighted_activities_optimally()
def test_algorithm_performance_with_large_dataset()

# Bad - unclear names
def test_1()
def test_algorithm()
def test_basic_case()
```

### 3. Test Documentation

```python
def test_complex_scheduling_scenario():
    """
    Test scheduling with mixed overlapping and non-overlapping activities.
    
    This test verifies that the greedy algorithm correctly handles a scenario
    where some activities overlap while others don't, ensuring optimal selection.
    
    Input activities represent a typical university course scheduling scenario:
    - Morning classes: 9-11, 10-12 (overlapping)
    - Afternoon classes: 13-15, 16-18 (non-overlapping)
    
    Expected: Algorithm should select 9-11, 13-15, 16-18 (3 activities total)
    """
    activities = [(9, 11), (10, 12), (13, 15), (16, 18)]
    result = greedy_activity_selection(activities)
    
    assert len(result) == 3
    assert set(result) == {0, 2, 3}
```

---

*This testing guide ensures your algorithms are correct, efficient, and robust. Follow these practices to build confidence in your implementation.*
