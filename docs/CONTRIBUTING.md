# Contributing Guidelines

Thank you for your interest in contributing to the Conflict-Free Scheduling project! This document provides guidelines and instructions for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Prioritize the project's educational goals

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or deliberately disruptive behavior
- Publishing private information without permission
- Any conduct inappropriate in an academic setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Git installed and configured
- C++ compiler (g++ 9.0+ or clang++ 10.0+)
- CMake 3.16+ and Make
- Code editor with C++ support (VS Code, CLion, etc.)
- Understanding of algorithm analysis concepts

### Development Environment Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/ConflictFreeScheduling.git
   cd ConflictFreeScheduling
   ```

2. **Set up Build Environment**
   ```bash
   # Create build directory
   mkdir build && cd build
   
   # Configure with CMake
   cmake ..
   
   # Build the project
   make
   ```
   git clone https://github.com/yourusername/ConflictFreeScheduling.git
   cd ConflictFreeScheduling
   ```

2. **Set Up Upstream Remote**
   ```bash
   git remote add upstream https://github.com/original/ConflictFreeScheduling.git
   git remote -v
   ```

3. **Create Development Environment**
   ```bash
   # For Python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # For Node.js
   npm install
   npm install --save-dev
   ```

4. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   python -m pytest tests/
   # or
   npm test
   ```

## Development Process

### Branching Strategy

We follow the **Feature Branch Workflow**:

```
main branch (stable)
├── feature/algorithm-optimization
├── feature/visualization-tool
├── bugfix/edge-case-handling
└── docs/performance-analysis
```

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

### Typical Workflow

1. **Create Feature Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following our standards
   - Add comprehensive tests
   - Update documentation
   - Commit regularly with descriptive messages

3. **Test Your Changes**
   ```bash
   # Run all tests
   python -m pytest tests/ -v
   
   # Run specific test categories
   python -m pytest tests/test_algorithms.py
   python -m pytest tests/test_performance.py
   
   # Check code coverage
   python -m pytest --cov=src tests/
   ```

4. **Submit Pull Request**
   - Push to your fork
   - Create PR against main branch
   - Fill out PR template completely

## Coding Standards

### General Principles

- **Clarity over Cleverness**: Write readable, maintainable code
- **Educational Focus**: Code should demonstrate algorithmic concepts clearly
- **Performance Awareness**: Consider time and space complexity
- **Comprehensive Testing**: Every function should have tests

### Python Style Guide

We follow **PEP 8** with some project-specific additions:

#### Code Formatting

```python
# Good: Clear function with type hints
def greedy_activity_selection(activities: List[Tuple[int, int]]) -> List[int]:
    """
    Implements greedy algorithm for activity selection problem.
    
    Args:
        activities: List of (start_time, end_time) tuples
        
    Returns:
        List of indices of selected activities
        
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    if not activities:
        return []
    
    # Sort by finish time for greedy selection
    sorted_indices = sorted(range(len(activities)), 
                           key=lambda i: activities[i][1])
    
    selected = [sorted_indices[0]]
    last_finish_time = activities[sorted_indices[0]][1]
    
    for i in sorted_indices[1:]:
        start_time = activities[i][0]
        if start_time >= last_finish_time:
            selected.append(i)
            last_finish_time = activities[i][1]
    
    return selected
```

#### Documentation Standards

- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Always include type hints
- **Complexity Analysis**: Document time/space complexity
- **Examples**: Include usage examples in docstrings

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.
    
    Longer description explaining the algorithm, approach, or
    important implementation details.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input is provided
        
    Example:
        >>> example_function(5, "test")
        True
        
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    pass
```

### File Organization

```
src/
├── algorithms/
│   ├── __init__.py
│   ├── greedy.py
│   ├── dynamic_programming.py
│   └── branch_bound.py
├── utils/
│   ├── __init__.py
│   ├── data_generator.py
│   └── visualization.py
└── main.py

tests/
├── test_algorithms/
│   ├── test_greedy.py
│   ├── test_dp.py
│   └── test_branch_bound.py
├── test_utils/
│   └── test_data_generator.py
└── conftest.py
```

## Testing Guidelines

### Test Categories

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test algorithm combinations
3. **Performance Tests**: Benchmark algorithms
4. **Edge Case Tests**: Handle boundary conditions

### Test Structure

```python
import pytest
from src.algorithms.greedy import greedy_activity_selection

class TestGreedyAlgorithm:
    """Test suite for greedy activity selection algorithm."""
    
    def test_empty_input(self):
        """Test algorithm with empty input."""
        result = greedy_activity_selection([])
        assert result == []
    
    def test_single_activity(self):
        """Test algorithm with single activity."""
        activities = [(1, 3)]
        result = greedy_activity_selection(activities)
        assert result == [0]
    
    def test_non_overlapping_activities(self):
        """Test with completely non-overlapping activities."""
        activities = [(1, 2), (3, 4), (5, 6)]
        result = greedy_activity_selection(activities)
        assert result == [0, 1, 2]
    
    def test_overlapping_activities(self):
        """Test with overlapping activities."""
        activities = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]
        result = greedy_activity_selection(activities)
        # Should select activities that finish earliest
        expected = [0, 3, 4]  # Activities (1,4), (5,7), (8,9)
        assert result == expected
    
    @pytest.mark.parametrize("size", [10, 100, 1000])
    def test_performance_scaling(self, size):
        """Test algorithm performance with different input sizes."""
        activities = generate_random_activities(size)
        
        import time
        start_time = time.time()
        result = greedy_activity_selection(activities)
        execution_time = time.time() - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0  # 1 second max
        assert len(result) <= size
```

### Performance Testing

```python
import pytest
from memory_profiler import profile

@pytest.mark.performance
class TestPerformance:
    """Performance benchmarks for algorithms."""
    
    def test_time_complexity(self):
        """Verify time complexity matches theoretical analysis."""
        sizes = [100, 200, 400, 800]
        times = []
        
        for size in sizes:
            activities = generate_random_activities(size)
            
            start = time.time()
            result = greedy_activity_selection(activities)
            elapsed = time.time() - start
            
            times.append(elapsed)
        
        # Check that time grows as O(n log n)
        # times[i+1] / times[i] should be roughly (2 * log(2)) ≈ 1.4
        for i in range(len(times) - 1):
            ratio = times[i+1] / times[i]
            assert 1.0 < ratio < 2.0  # Allow some variance
    
    @profile
    def test_memory_usage(self):
        """Profile memory usage of algorithms."""
        large_input = generate_random_activities(10000)
        result = greedy_activity_selection(large_input)
        # Memory profiler will show detailed usage
```

### Test Data Generation

```python
def generate_test_cases():
    """Generate comprehensive test cases."""
    return [
        # Edge cases
        ("empty", []),
        ("single", [(1, 3)]),
        
        # Normal cases
        ("non_overlapping", [(1, 2), (3, 4), (5, 6)]),
        ("all_overlapping", [(1, 5), (2, 4), (3, 6)]),
        
        # Complex cases
        ("mixed", [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]),
        
        # Stress tests
        ("large", generate_random_activities(1000)),
    ]
```

## Documentation Standards

### Code Documentation

- **Every function** must have a docstring
- **Complex algorithms** need detailed comments
- **Performance characteristics** should be documented
- **Examples** should be provided for public APIs

### README Updates

When adding new features:

1. Update the feature list
2. Add usage examples
3. Update installation instructions if needed
4. Modify performance benchmarks

### Algorithm Documentation

For new algorithms, create:

1. **Theory section** explaining the approach
2. **Implementation details** with code snippets  
3. **Complexity analysis** (time and space)
4. **Examples** showing the algorithm in action
5. **Comparison** with existing algorithms

## Pull Request Process

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Algorithm Details (if applicable)
- **Time Complexity**: O(?)
- **Space Complexity**: O(?)
- **Optimality**: Optimal/Approximation

## Testing
- [ ] Unit tests added/updated
- [ ] Performance tests added
- [ ] All tests pass
- [ ] Code coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changes are well-commented
```

### Review Process

1. **Automated Checks**
   - Code style verification
   - Test suite execution
   - Performance regression checks

2. **Peer Review**
   - Algorithm correctness
   - Code quality and clarity
   - Documentation completeness

3. **Maintainer Review**
   - Educational value
   - Project alignment
   - Final approval

### Merging Criteria

PRs will be merged when:
- All tests pass
- Code review approved
- Documentation is complete
- No merge conflicts
- Educational objectives met

## Recognition

Contributors will be:
- Listed in the project's CONTRIBUTORS.md
- Mentioned in release notes
- Credited in academic presentations (if applicable)

## Questions?

If you have questions:
1. Check existing issues and discussions
2. Create a new issue with the "question" label
3. Contact maintainers directly

Thank you for contributing to the Conflict-Free Scheduling project! Your efforts help make algorithm education more accessible and practical.
