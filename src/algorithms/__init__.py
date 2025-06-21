"""
Scheduling Algorithms Module

This module contains various algorithms for conflict-free scheduling:
- Graph Coloring: Models conflicts as graph edges, assigns time slots as colors
- Dynamic Programming: Optimal weighted activity selection with memoization
- Backtracking: Exhaustive search with pruning for optimal solutions
- Genetic Algorithm: Population-based evolutionary optimization
"""

from .graph_coloring import GraphColoringScheduler
from .dynamic_programming import DynamicProgrammingScheduler
from .backtracking import BacktrackingScheduler
from .genetic_algorithm import GeneticAlgorithmScheduler, GAConfig

# Available algorithms
ALGORITHMS = {
    'graph-coloring': GraphColoringScheduler,
    'dynamic-prog': DynamicProgrammingScheduler,
    'backtracking': BacktrackingScheduler,
    'genetic': GeneticAlgorithmScheduler
}
