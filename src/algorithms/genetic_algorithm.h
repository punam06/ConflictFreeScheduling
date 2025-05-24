#ifndef GENETIC_ALGORITHM_H
#define GENETIC_ALGORITHM_H

#include "../scheduler.h"
#include <vector>
#include <random>
#include <algorithm>

/**
 * @brief Genetic Algorithm for Evolutionary Scheduling Optimization
 * 
 * This class implements genetic algorithm to evolve optimal scheduling solutions
 * using population-based optimization with crossover, mutation, and selection.
 */
class GeneticAlgorithmScheduler {
public:
    /**
     * @brief Configuration parameters for genetic algorithm
     */
    struct GAConfig {
        size_t populationSize;   // Size of population
        size_t generations;      // Number of generations
        double crossoverRate;    // Probability of crossover
        double mutationRate;     // Probability of mutation
        size_t eliteSize;        // Number of elite individuals to preserve
        
        GAConfig() : populationSize(100), generations(500), crossoverRate(0.8), mutationRate(0.1), eliteSize(10) {}
        GAConfig(size_t pop, size_t gen, double cross, double mut, size_t elite)
            : populationSize(pop), generations(gen), crossoverRate(cross), 
              mutationRate(mut), eliteSize(elite) {}
    };

    /**
     * @brief Find optimal schedule using genetic algorithm
     * @param activities Vector of activities to schedule
     * @param config GA configuration parameters
     * @return Vector of activities representing optimal schedule
     * @complexity Time: O(P * G * N), Space: O(P * N) where P=population, G=generations, N=activities
     */
    static std::vector<Activity> evolveSchedule(std::vector<Activity> activities, 
                                                const GAConfig& config = GAConfig());

private:
    // Individual represents a potential solution (chromosome)
    struct Individual {
        std::vector<bool> genes;    // Binary representation: gene[i] = true if activity[i] is selected
        double fitness;             // Fitness value (total weight - penalty for conflicts)
        
        Individual(size_t size) : genes(size, false), fitness(0.0) {}
    };

    /**
     * @brief Initialize random population
     */
    static std::vector<Individual> initializePopulation(size_t populationSize, size_t numActivities, std::mt19937& rng);
    
    /**
     * @brief Calculate fitness for an individual
     * @param individual Individual to evaluate
     * @param activities Activities list
     * @return Fitness value (higher is better)
     */
    static double calculateFitness(Individual& individual, const std::vector<Activity>& activities);
    
    /**
     * @brief Select parents using tournament selection
     */
    static std::pair<Individual, Individual> selectParents(const std::vector<Individual>& population, std::mt19937& rng);
    
    /**
     * @brief Perform crossover between two parents
     */
    static std::pair<Individual, Individual> crossover(const Individual& parent1, 
                                                       const Individual& parent2, 
                                                       double crossoverRate, 
                                                       std::mt19937& rng);
    
    /**
     * @brief Mutate an individual
     */
    static void mutate(Individual& individual, double mutationRate, std::mt19937& rng);
    
    /**
     * @brief Convert individual to activity list
     */
    static std::vector<Activity> individualToActivities(const Individual& individual, 
                                                        const std::vector<Activity>& activities);
    
    /**
     * @brief Check if two activities conflict
     */
    static bool hasConflict(const Activity& a1, const Activity& a2);
    
    /**
     * @brief Calculate conflict penalty for a schedule
     */
    static double calculateConflictPenalty(const std::vector<Activity>& schedule);
};

#endif // GENETIC_ALGORITHM_H
