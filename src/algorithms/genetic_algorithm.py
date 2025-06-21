#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Genetic Algorithm for Conflict-Free Scheduling

This module implements a genetic algorithm for evolutionary optimization
of activity scheduling problems.
"""

from typing import List, Tuple
from dataclasses import dataclass
import random
import copy


@dataclass
class Activity:
    """Class representing an activity/task with start and end times"""
    id: int
    start: int
    end: int
    weight: float = 1.0  # Default weight for unweighted problems
    name: str = ""
    room: str = ""


@dataclass
class GAConfig:
    """Configuration for Genetic Algorithm"""
    population_size: int = 50
    generations: int = 100
    crossover_rate: float = 0.8
    mutation_rate: float = 0.1
    elite_size: int = 5


class Individual:
    """Represents an individual in the genetic algorithm population"""
    
    def __init__(self, activities: List[Activity], chromosome: List[bool] = None):
        """
        Initialize individual
        
        Args:
            activities: List of all activities
            chromosome: Binary representation (True = selected, False = not selected)
        """
        self.activities = activities
        if chromosome is None:
            # Random initialization
            self.chromosome = [random.choice([True, False]) for _ in activities]
        else:
            self.chromosome = chromosome
        
        self.fitness = 0.0
        self.is_valid = False
        self._evaluate()
    
    def _evaluate(self) -> None:
        """Evaluate fitness of this individual"""
        selected_activities = []
        for i, selected in enumerate(self.chromosome):
            if selected:
                selected_activities.append(self.activities[i])
        
        # Check if the selection is conflict-free
        self.is_valid = self._is_conflict_free(selected_activities)
        
        if self.is_valid:
            # Fitness is total weight of selected activities
            self.fitness = sum(act.weight for act in selected_activities)
        else:
            # Penalty for invalid solutions
            total_weight = sum(act.weight for act in selected_activities)
            conflicts = self._count_conflicts(selected_activities)
            self.fitness = total_weight - (conflicts * 10)  # Heavy penalty for conflicts
    
    def _is_conflict_free(self, activities: List[Activity]) -> bool:
        """Check if selected activities are conflict-free"""
        if len(activities) <= 1:
            return True
        
        # Sort by start time
        activities = sorted(activities, key=lambda a: a.start)
        
        for i in range(len(activities) - 1):
            if activities[i].end > activities[i + 1].start:
                return False
        
        return True
    
    def _count_conflicts(self, activities: List[Activity]) -> int:
        """Count number of conflicts in the selection"""
        conflicts = 0
        n = len(activities)
        
        for i in range(n):
            for j in range(i + 1, n):
                if not (activities[i].end <= activities[j].start or 
                       activities[j].end <= activities[i].start):
                    conflicts += 1
        
        return conflicts
    
    def get_selected_activities(self) -> List[Activity]:
        """Get list of selected activities"""
        return [self.activities[i] for i, selected in enumerate(self.chromosome) if selected]


class GeneticAlgorithmScheduler:
    """Genetic Algorithm for Evolutionary Optimization"""
    
    @staticmethod
    def evolve_schedule(activities: List[Activity], config: GAConfig) -> List[Activity]:
        """
        Evolve optimal schedule using genetic algorithm
        
        Args:
            activities: List of activities to schedule
            config: GA configuration parameters
            
        Returns:
            List of activities in evolved optimal schedule
        """
        if not activities:
            return []
        
        # Initialize population
        population = []
        for _ in range(config.population_size):
            individual = Individual(activities)
            population.append(individual)
        
        best_individual = None
        best_fitness = float('-inf')
        
        # Evolution loop
        for generation in range(config.generations):
            # Evaluate population
            for individual in population:
                if individual.fitness > best_fitness and individual.is_valid:
                    best_fitness = individual.fitness
                    best_individual = copy.deepcopy(individual)
            
            # Selection, crossover, and mutation
            new_population = []
            
            # Elite selection (keep best individuals)
            population.sort(key=lambda x: x.fitness, reverse=True)
            for i in range(config.elite_size):
                if i < len(population):
                    new_population.append(copy.deepcopy(population[i]))
            
            # Generate rest of population through crossover and mutation
            while len(new_population) < config.population_size:
                # Selection
                parent1 = GeneticAlgorithmScheduler._tournament_selection(population)
                parent2 = GeneticAlgorithmScheduler._tournament_selection(population)
                
                # Crossover
                if random.random() < config.crossover_rate:
                    child1, child2 = GeneticAlgorithmScheduler._crossover(parent1, parent2, activities)
                else:
                    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
                
                # Mutation
                if random.random() < config.mutation_rate:
                    GeneticAlgorithmScheduler._mutate(child1)
                if random.random() < config.mutation_rate:
                    GeneticAlgorithmScheduler._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Trim population to exact size
            population = new_population[:config.population_size]
        
        # Return best solution found
        if best_individual and best_individual.is_valid:
            return best_individual.get_selected_activities()
        else:
            # Fallback: return greedy solution
            return GeneticAlgorithmScheduler._greedy_fallback(activities)
    
    @staticmethod
    def _tournament_selection(population: List[Individual], tournament_size: int = 3) -> Individual:
        """
        Tournament selection for parent selection
        
        Args:
            population: Current population
            tournament_size: Size of tournament
            
        Returns:
            Selected individual
        """
        tournament = random.sample(population, min(tournament_size, len(population)))
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        return tournament[0]
    
    @staticmethod
    def _crossover(parent1: Individual, parent2: Individual, 
                  activities: List[Activity]) -> Tuple[Individual, Individual]:
        """
        Single-point crossover
        
        Args:
            parent1: First parent
            parent2: Second parent
            activities: List of activities
            
        Returns:
            Tuple of two children
        """
        crossover_point = random.randint(1, len(parent1.chromosome) - 1)
        
        child1_chromosome = (parent1.chromosome[:crossover_point] + 
                           parent2.chromosome[crossover_point:])
        child2_chromosome = (parent2.chromosome[:crossover_point] + 
                           parent1.chromosome[crossover_point:])
        
        child1 = Individual(activities, child1_chromosome)
        child2 = Individual(activities, child2_chromosome)
        
        return child1, child2
    
    @staticmethod
    def _mutate(individual: Individual) -> None:
        """
        Bit-flip mutation
        
        Args:
            individual: Individual to mutate
        """
        mutation_point = random.randint(0, len(individual.chromosome) - 1)
        individual.chromosome[mutation_point] = not individual.chromosome[mutation_point]
        individual._evaluate()  # Re-evaluate after mutation
    
    @staticmethod
    def _greedy_fallback(activities: List[Activity]) -> List[Activity]:
        """
        Greedy fallback solution when GA fails
        
        Args:
            activities: List of activities
            
        Returns:
            Greedy solution
        """
        if not activities:
            return []
        
        # Sort by weight/duration ratio for better greedy selection
        activities = sorted(activities, key=lambda a: a.weight / max(a.end - a.start, 1), reverse=True)
        
        selected = []
        for activity in activities:
            # Check if this activity conflicts with any selected activity
            conflicts = False
            for selected_activity in selected:
                if not (activity.end <= selected_activity.start or 
                       selected_activity.end <= activity.start):
                    conflicts = True
                    break
            
            if not conflicts:
                selected.append(activity)
        
        return selected
    
    @staticmethod
    def evolve_with_multiple_runs(activities: List[Activity], config: GAConfig, 
                                runs: int = 5) -> List[Activity]:
        """
        Run GA multiple times and return best result
        
        Args:
            activities: List of activities to schedule
            config: GA configuration
            runs: Number of independent runs
            
        Returns:
            Best schedule found across all runs
        """
        best_schedule = []
        best_weight = 0.0
        
        for _ in range(runs):
            schedule = GeneticAlgorithmScheduler.evolve_schedule(activities, config)
            weight = sum(act.weight for act in schedule)
            
            if weight > best_weight:
                best_weight = weight
                best_schedule = schedule
        
        return best_schedule
