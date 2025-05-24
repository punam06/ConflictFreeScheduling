// filepath: /Users/punam/Desktop/Varsity/2-2/Algo/project/github deployment/ConflictFreeScheduling/src/algorithms/genetic_algorithm.cpp
#include "genetic_algorithm.h"
#include <random>
#include <algorithm>
#include <numeric>
#include <iostream>

std::vector<Activity> GeneticAlgorithmScheduler::evolveSchedule(std::vector<Activity> activities, const GAConfig& config) {
    if (activities.empty()) return {};
    
    std::mt19937 rng(std::random_device{}());
    
    // Initialize population
    auto population = initializePopulation(config.populationSize, activities.size(), rng);
    
    // Evaluate initial population
    for (auto& individual : population) {
        individual.fitness = calculateFitness(individual, activities);
    }
    
    // Evolution loop
    for (size_t generation = 0; generation < config.generations; ++generation) {
        // Sort by fitness (descending)
        std::sort(population.begin(), population.end(), 
                  [](const Individual& a, const Individual& b) { 
                      return a.fitness > b.fitness; 
                  });
        
        // Create new generation
        std::vector<Individual> newPopulation;
        
        // Keep elite individuals
        for (size_t i = 0; i < config.eliteSize && i < population.size(); ++i) {
            newPopulation.push_back(population[i]);
        }
        
        // Generate offspring
        while (newPopulation.size() < config.populationSize) {
            auto parents = selectParents(population, rng);
            auto offspring = crossover(parents.first, parents.second, config.crossoverRate, rng);
            
            mutate(offspring.first, config.mutationRate, rng);
            mutate(offspring.second, config.mutationRate, rng);
            
            offspring.first.fitness = calculateFitness(offspring.first, activities);
            offspring.second.fitness = calculateFitness(offspring.second, activities);
            
            newPopulation.push_back(offspring.first);
            if (newPopulation.size() < config.populationSize) {
                newPopulation.push_back(offspring.second);
            }
        }
        
        population = std::move(newPopulation);
        
        // Optional: Print progress every 100 generations
        if (generation % 100 == 0) {
            std::cout << "Generation " << generation << ", Best fitness: " << population[0].fitness << std::endl;
        }
    }
    
    // Return best solution
    std::sort(population.begin(), population.end(), 
              [](const Individual& a, const Individual& b) { 
                  return a.fitness > b.fitness; 
              });
    
    return individualToActivities(population[0], activities);
}

std::vector<GeneticAlgorithmScheduler::Individual> GeneticAlgorithmScheduler::initializePopulation(
    size_t populationSize, size_t numActivities, std::mt19937& rng) {
    
    std::vector<Individual> population;
    std::uniform_real_distribution<double> prob(0.0, 1.0);
    
    for (size_t i = 0; i < populationSize; ++i) {
        Individual individual(numActivities);
        
        // Random initialization with 30% probability for each gene
        for (size_t j = 0; j < individual.genes.size(); ++j) {
            individual.genes[j] = prob(rng) < 0.3;
        }
        
        population.push_back(individual);
    }
    
    return population;
}

double GeneticAlgorithmScheduler::calculateFitness(Individual& individual, const std::vector<Activity>& activities) {
    auto schedule = individualToActivities(individual, activities);
    
    if (schedule.empty()) return 0.0;
    
    // Calculate total weight
    double totalWeight = 0.0;
    for (const auto& activity : schedule) {
        totalWeight += activity.weight;
    }
    
    // Calculate conflict penalty
    double conflictPenalty = calculateConflictPenalty(schedule);
    
    // Fitness = total weight - heavy penalty for conflicts
    return totalWeight - (conflictPenalty * 1000.0);
}

std::pair<GeneticAlgorithmScheduler::Individual, GeneticAlgorithmScheduler::Individual> 
GeneticAlgorithmScheduler::selectParents(const std::vector<Individual>& population, std::mt19937& rng) {
    // Tournament selection
    std::uniform_int_distribution<size_t> dist(0, population.size() - 1);
    
    auto tournamentSelect = [&]() -> const Individual& {
        const size_t tournamentSize = 3;
        size_t bestIdx = dist(rng);
        double bestFitness = population[bestIdx].fitness;
        
        for (size_t i = 1; i < tournamentSize; ++i) {
            size_t idx = dist(rng);
            if (population[idx].fitness > bestFitness) {
                bestFitness = population[idx].fitness;
                bestIdx = idx;
            }
        }
        return population[bestIdx];
    };
    
    return {tournamentSelect(), tournamentSelect()};
}

std::pair<GeneticAlgorithmScheduler::Individual, GeneticAlgorithmScheduler::Individual> 
GeneticAlgorithmScheduler::crossover(const Individual& parent1, const Individual& parent2, 
                                    double crossoverRate, std::mt19937& rng) {
    Individual child1 = parent1;
    Individual child2 = parent2;
    
    std::uniform_real_distribution<double> prob(0.0, 1.0);
    
    if (prob(rng) < crossoverRate) {
        // Single-point crossover
        std::uniform_int_distribution<size_t> pointDist(1, parent1.genes.size() - 1);
        size_t crossoverPoint = pointDist(rng);
        
        for (size_t i = crossoverPoint; i < parent1.genes.size(); ++i) {
            child1.genes[i] = parent2.genes[i];
            child2.genes[i] = parent1.genes[i];
        }
    }
    
    return {child1, child2};
}

void GeneticAlgorithmScheduler::mutate(Individual& individual, double mutationRate, std::mt19937& rng) {
    std::uniform_real_distribution<double> prob(0.0, 1.0);
    
    for (size_t i = 0; i < individual.genes.size(); ++i) {
        if (prob(rng) < mutationRate) {
            individual.genes[i] = !individual.genes[i];
        }
    }
}

std::vector<Activity> GeneticAlgorithmScheduler::individualToActivities(
    const Individual& individual, const std::vector<Activity>& activities) {
    
    std::vector<Activity> result;
    for (size_t i = 0; i < individual.genes.size(); ++i) {
        if (individual.genes[i]) {
            result.push_back(activities[i]);
        }
    }
    return result;
}

bool GeneticAlgorithmScheduler::hasConflict(const Activity& a1, const Activity& a2) {
    return !(a1.end <= a2.start || a2.end <= a1.start);
}

double GeneticAlgorithmScheduler::calculateConflictPenalty(const std::vector<Activity>& schedule) {
    double penalty = 0.0;
    
    for (size_t i = 0; i < schedule.size(); ++i) {
        for (size_t j = i + 1; j < schedule.size(); ++j) {
            if (hasConflict(schedule[i], schedule[j])) {
                penalty += 1.0;
            }
        }
    }
    
    return penalty;
}
