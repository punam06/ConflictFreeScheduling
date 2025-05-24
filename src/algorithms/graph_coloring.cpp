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
    
    // Group activities by color (time slot)
    std::unordered_map<int, std::vector<Activity>> colorGroups;
    for (const auto& activity : activities) {
        int color = colorAssignment[activity.id];
        if (color >= 0) {
            colorGroups[color].push_back(activity);
        }
    }
    
    // Schedule each color group sequentially
    int currentTime = 0;
    for (auto& [color, group] : colorGroups) {
        // Sort activities in group by original start time to maintain some order
        std::sort(group.begin(), group.end(), 
                  [](const Activity& a, const Activity& b) {
                      return a.start < b.start;
                  });
        
        // Schedule activities in this color group non-conflictingly
        for (auto& activity : group) {
            Activity scheduled = activity;
            int duration = activity.end - activity.start;
            scheduled.start = currentTime;
            scheduled.end = currentTime + duration;
            scheduledActivities.push_back(scheduled);
            currentTime = scheduled.end + 1; // Add gap to prevent edge conflicts
        }
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
    
    // First, sort activities by duration (descending) to handle longer activities first
    std::vector<std::pair<int, int>> sortedActivities; // {duration, id}
    for (const auto& activity : activities) {
        sortedActivities.push_back({activity.end - activity.start, activity.id});
    }
    std::sort(sortedActivities.begin(), sortedActivities.end(), std::greater<std::pair<int, int>>());
    
    // Try to assign colors, marking unassignable activities with -1
    for (const auto& pair : sortedActivities) {
        int activityId = pair.second;
        std::set<int> usedColors;
        
        // Check colors used by neighbors
        if (graph.find(activityId) != graph.end()) {
            for (int neighbor : graph.at(activityId)) {
                if (colors.find(neighbor) != colors.end() && colors[neighbor] >= 0) {
                    usedColors.insert(colors[neighbor]);
                }
            }
        }
        
        // Try to find an available color
        int color = -1;
        for (int c = 0; c < static_cast<int>(activities.size()); c++) {
            if (!usedColors.count(c)) {
                color = c;
                break;
            }
        }
        
        colors[activityId] = color;
    }
    
    return colors;
}
