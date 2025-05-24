#include "graph_coloring.h"
#include <iostream>
#include <set>

std::vector<Activity> GraphColoringScheduler::coloringSchedule(std::vector<Activity> activities) {
    if (activities.empty()) return {};
    
    // Build conflict graph
    auto conflictGraph = buildConflictGraph(activities);
    
    // Assign colors (time slots) to activities
    auto colorAssignment = assignColors(activities, conflictGraph);
    
    // Create scheduled activities with assigned time slots
    std::vector<Activity> scheduledActivities;
    for (const auto& activity : activities) {
        Activity scheduled = activity;
        int color = colorAssignment[activity.id];
        
        // Assign new time slot based on color
        scheduled.start = color * 2;  // Each color represents a 2-hour slot
        scheduled.end = scheduled.start + (activity.end - activity.start);
        
        scheduledActivities.push_back(scheduled);
    }
    
    return scheduledActivities;
}

int GraphColoringScheduler::welshPowellColoring(std::vector<Activity> activities) {
    if (activities.empty()) return 0;
    
    auto conflictGraph = buildConflictGraph(activities);
    
    // Calculate degree of each vertex
    std::vector<std::pair<int, int>> degreeList; // {degree, activity_id}
    for (const auto& activity : activities) {
        int degree = conflictGraph[activity.id].size();
        degreeList.push_back({degree, activity.id});
    }
    
    // Sort by degree (descending order)
    std::sort(degreeList.begin(), degreeList.end(), std::greater<std::pair<int, int>>());
    
    std::unordered_map<int, int> colors;
    int maxColor = 0;
    
    for (const auto& pair : degreeList) {
        int activityId = pair.second;
        
        // Find the smallest color not used by neighbors
        std::set<int> usedColors;
        for (int neighbor : conflictGraph[activityId]) {
            if (colors.find(neighbor) != colors.end()) {
                usedColors.insert(colors[neighbor]);
            }
        }
        
        int color = 0;
        while (usedColors.count(color)) {
            color++;
        }
        
        colors[activityId] = color;
        maxColor = std::max(maxColor, color);
    }
    
    return maxColor + 1; // Number of colors needed
}

std::unordered_map<int, std::vector<int>> GraphColoringScheduler::buildConflictGraph(const std::vector<Activity>& activities) {
    std::unordered_map<int, std::vector<int>> graph;
    
    // Initialize adjacency lists
    for (const auto& activity : activities) {
        graph[activity.id] = std::vector<int>();
    }
    
    // Add edges for conflicting activities
    for (size_t i = 0; i < activities.size(); i++) {
        for (size_t j = i + 1; j < activities.size(); j++) {
            if (hasTimeConflict(activities[i], activities[j])) {
                graph[activities[i].id].push_back(activities[j].id);
                graph[activities[j].id].push_back(activities[i].id);
            }
        }
    }
    
    return graph;
}

bool GraphColoringScheduler::hasTimeConflict(const Activity& a1, const Activity& a2) {
    // Two activities conflict if their time intervals overlap
    return !(a1.end <= a2.start || a2.end <= a1.start);
}

std::unordered_map<int, int> GraphColoringScheduler::assignColors(
    const std::vector<Activity>& activities,
    const std::unordered_map<int, std::vector<int>>& graph) {
    
    std::unordered_map<int, int> colors;
    
    for (const auto& activity : activities) {
        // Find the smallest color not used by neighbors
        std::set<int> usedColors;
        
        if (graph.find(activity.id) != graph.end()) {
            for (int neighbor : graph.at(activity.id)) {
                if (colors.find(neighbor) != colors.end()) {
                    usedColors.insert(colors[neighbor]);
                }
            }
        }
        
        int color = 0;
        while (usedColors.count(color)) {
            color++;
        }
        
        colors[activity.id] = color;
    }
    
    return colors;
}
