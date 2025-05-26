#include "enhanced_routine_generator.h"
#include <algorithm>
#include <random>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <sstream>

EnhancedRoutineGenerator::EnhancedRoutineGenerator(std::shared_ptr<DatabaseManager> dbMgr)
    : dbManager(dbMgr), prioritizeExternalFaculty(true), minimizeGaps(true), 
      balanceRoomUsage(true), maxTriesPerCourse(50) {
    
    if (!dbManager) {
        throw std::runtime_error("Database manager cannot be null");
    }
    
    // Load all necessary data
    loadCourseData();
    loadTimeSlotData();
    loadRoomData();
    loadFacultyConstraints();
    
    std::cout << "🎓 Enhanced Routine Generator initialized" << std::endl;
    std::cout << "   📚 Courses loaded: " << allCourses.size() << std::endl;
    std::cout << "   ⏰ Time slots: " << allTimeSlots.size() << std::endl;
    std::cout << "   🏢 Rooms: " << allRooms.size() << std::endl;
}

void EnhancedRoutineGenerator::loadCourseData() {
    std::cout << "📚 Loading course data..." << std::endl;
    
    // Get all academic courses from database
    auto dbCourses = dbManager->getAllAcademicCourses();
    auto dbBatches = dbManager->getAllBatches();
    auto dbTeachers = dbManager->getAllTeachers();
    
    // Convert to internal format
    for (const auto& dbCourse : dbCourses) {
        // Find the batch for this course
        auto batchIt = std::find_if(dbBatches.begin(), dbBatches.end(),
            [&](const DatabaseManager::AcademicBatch& b) { return b.batch_id == dbCourse.batch_id; });
        
        if (batchIt == dbBatches.end()) continue;
        
        // Find the teacher for this course
        auto teacherIt = std::find_if(dbTeachers.begin(), dbTeachers.end(),
            [&](const DatabaseManager::AcademicTeacher& t) { return t.teacher_id == dbCourse.teacher_id; });
        
        if (teacherIt == dbTeachers.end()) continue;
        
        // Create CourseScheduleInfo for both sections A and B
        for (const std::string& section : {"A", "B"}) {
            CourseScheduleInfo course;
            course.course_id = dbCourse.course_id;
            course.course_code = dbCourse.course_code;
            course.course_title = dbCourse.course_title;
            course.batch_code = batchIt->batch_code;
            course.section_name = section;
            course.credit_hours = dbCourse.credit_hours;
            course.class_type = dbCourse.class_type;
            course.session_duration = dbCourse.session_duration;
            course.sessions_per_week = dbCourse.sessions_per_week;
            course.teacher_id = dbCourse.teacher_id;
            course.faculty_name = teacherIt->full_name;
            course.is_external_faculty = teacherIt->external_faculty;
            
            // Set preferences based on faculty type
            if (course.is_external_faculty) {
                // External faculty prefer concentrated schedules
                course.preferred_days = {"TUE", "WED"};  // Middle of week
                if (teacherIt->availability_start >= "12:00:00") {
                    course.preferred_times = {"14:00:00", "15:35:00"};  // Afternoon
                } else {
                    course.preferred_times = {"10:05:00", "11:40:00"};  // Late morning
                }
            } else {
                // Internal faculty can teach any time
                course.preferred_days = {"SUN", "MON", "TUE", "WED", "THU"};
                course.preferred_times = {"08:30:00", "10:05:00", "11:40:00", "14:00:00", "15:35:00"};
            }
            
            allCourses.push_back(course);
            coursesByBatch[course.batch_code].push_back(course);
        }
    }
    
    std::cout << "   ✓ Total course-section combinations: " << allCourses.size() << std::endl;
    for (const auto& [batch, courses] : coursesByBatch) {
        std::cout << "   ✓ " << batch << ": " << courses.size() << " course-sections" << std::endl;
    }
}

void EnhancedRoutineGenerator::loadTimeSlotData() {
    std::cout << "⏰ Loading time slot data..." << std::endl;
    
    auto dbTimeSlots = dbManager->getAllAcademicTimeSlots();
    
    for (const auto& dbSlot : dbTimeSlots) {
        TimeSlotInfo slot;
        slot.slot_id = dbSlot.slot_id;
        slot.slot_name = dbSlot.slot_name;
        slot.day_of_week = dbSlot.day_of_week;
        slot.start_time = dbSlot.start_time;
        slot.end_time = dbSlot.end_time;
        slot.duration_minutes = dbSlot.duration_minutes;
        slot.slot_type = dbSlot.slot_type;
        slot.is_available = (dbSlot.slot_type != "LUNCH");  // Lunch slots not available for classes
        
        allTimeSlots.push_back(slot);
    }
    
    std::cout << "   ✓ Available time slots: " << 
        std::count_if(allTimeSlots.begin(), allTimeSlots.end(), 
                     [](const TimeSlotInfo& s) { return s.is_available; }) << std::endl;
}

void EnhancedRoutineGenerator::loadRoomData() {
    std::cout << "🏢 Loading room data..." << std::endl;
    
    auto dbRooms = dbManager->getAllRooms();
    
    for (const auto& dbRoom : dbRooms) {
        RoomInfo room;
        room.room_id = dbRoom.room_id;
        room.room_code = dbRoom.room_code;
        room.capacity = dbRoom.capacity;
        room.room_type = dbRoom.room_type;
        room.building = dbRoom.building;
        room.is_available = dbRoom.is_available;
        
        allRooms.push_back(room);
    }
    
    int theoryRooms = std::count_if(allRooms.begin(), allRooms.end(),
        [](const RoomInfo& r) { return r.room_type == "THEORY"; });
    int labRooms = std::count_if(allRooms.begin(), allRooms.end(),
        [](const RoomInfo& r) { return r.room_type == "LAB"; });
    
    std::cout << "   ✓ Theory rooms: " << theoryRooms << std::endl;
    std::cout << "   ✓ Lab rooms: " << labRooms << std::endl;
}

void EnhancedRoutineGenerator::loadFacultyConstraints() {
    std::cout << "👥 Loading faculty constraints..." << std::endl;
    
    auto dbTeachers = dbManager->getAllTeachers();
    
    for (const auto& teacher : dbTeachers) {
        std::vector<TimeSlotInfo> availableSlots;
        
        // Filter time slots based on teacher availability
        for (const auto& slot : allTimeSlots) {
            if (!slot.is_available) continue;
            
            // Check if slot time is within teacher's availability
            if (slot.start_time >= teacher.availability_start && 
                slot.end_time <= teacher.availability_end) {
                availableSlots.push_back(slot);
            }
        }
        
        teacherAvailability[teacher.teacher_id] = availableSlots;
        
        std::cout << "   ✓ " << teacher.full_name << " (" << 
            (teacher.external_faculty ? "External" : "Internal") << "): " <<
            availableSlots.size() << " available slots" << std::endl;
    }
}

bool EnhancedRoutineGenerator::generateCompleteRoutine(const std::string& academic_year, 
                                                      const std::string& semester) {
    std::cout << "\n🎓 === Generating Complete University Routine ===" << std::endl;
    std::cout << "Academic Year: " << academic_year << ", Semester: " << semester << std::endl;
    
    // Clear previous schedule
    currentSchedule.clear();
    detectedConflicts.clear();
    
    // Sort courses by priority (external faculty first, then by credit hours)
    std::vector<CourseScheduleInfo> sortedCourses = allCourses;
    std::sort(sortedCourses.begin(), sortedCourses.end(), 
        [](const CourseScheduleInfo& a, const CourseScheduleInfo& b) {
            // Prioritize external faculty
            if (a.is_external_faculty != b.is_external_faculty) {
                return a.is_external_faculty > b.is_external_faculty;
            }
            // Then by credit hours (higher first)
            if (a.credit_hours != b.credit_hours) {
                return a.credit_hours > b.credit_hours;
            }
            // Then by class type (LAB first as they need specific rooms)
            if (a.class_type != b.class_type) {
                return a.class_type == "LAB";
            }
            // Then by batch (newer batches first)
            return a.batch_code > b.batch_code;
        });
    
    int successfullyScheduled = 0;
    int totalCoursesToSchedule = 0;
    
    for (const auto& course : sortedCourses) {
        for (int session = 1; session <= course.sessions_per_week; ++session) {
            totalCoursesToSchedule++;
            
            std::cout << "\n📅 Scheduling " << course.course_code << " (" << course.batch_code 
                     << "-" << course.section_name << ") Session " << session 
                     << " [" << course.class_type << "]" << std::endl;
            
            ScheduleAssignment assignment;
            assignment.course = course;
            assignment.session_number = session;
            assignment.has_conflict = false;
            
            bool scheduled = false;
            int attempts = 0;
            
            // Try to find suitable time slot and room
            while (!scheduled && attempts < maxTriesPerCourse) {
                attempts++;
                
                // Get available time slots for this course
                std::vector<std::pair<TimeSlotInfo, RoomInfo>> candidateSlots;
                
                for (const auto& timeSlot : allTimeSlots) {
                    if (!timeSlot.is_available) continue;
                    
                    // Check if slot duration matches course requirements
                    bool slotMatches = false;
                    if (course.class_type == "THEORY" && timeSlot.duration_minutes == 90) {
                        slotMatches = true;
                    } else if (course.class_type == "LAB" && timeSlot.duration_minutes == 180) {
                        slotMatches = true;
                    }
                    
                    if (!slotMatches) continue;
                    
                    // Check faculty availability
                    auto facultySlots = teacherAvailability[course.teacher_id];
                    bool facultyAvailable = std::any_of(facultySlots.begin(), facultySlots.end(),
                        [&](const TimeSlotInfo& fSlot) { return fSlot.slot_id == timeSlot.slot_id; });
                    
                    if (!facultyAvailable) continue;
                    
                    // Find available rooms
                    for (const auto& room : allRooms) {
                        if (!room.is_available) continue;
                        
                        // Check room type compatibility
                        if (course.class_type == "LAB" && room.room_type != "LAB") continue;
                        if (course.class_type == "THEORY" && room.room_type == "LAB") continue;
                        
                        candidateSlots.push_back({timeSlot, room});
                    }
                }
                
                if (candidateSlots.empty()) {
                    std::cout << "   ❌ No available slots found (attempt " << attempts << ")" << std::endl;
                    break;
                }
                
                // Prioritize slots that minimize gaps for this batch-section
                if (minimizeGaps) {
                    std::string batchSection = course.batch_code + "-" + course.section_name;
                    
                    // Find existing classes for this batch-section
                    std::vector<ScheduleAssignment> batchClasses;
                    for (const auto& existing : currentSchedule) {
                        if (existing.course.batch_code == course.batch_code && 
                            existing.course.section_name == course.section_name) {
                            batchClasses.push_back(existing);
                        }
                    }
                    
                    // Sort candidate slots by gap-minimization score
                    std::sort(candidateSlots.begin(), candidateSlots.end(),
                        [&](const std::pair<TimeSlotInfo, RoomInfo>& a, const std::pair<TimeSlotInfo, RoomInfo>& b) {
                            return calculateGapScore(a.first, batchClasses) < calculateGapScore(b.first, batchClasses);
                        });
                } else {
                    // Shuffle candidates for variety if gap minimization is disabled
                    std::shuffle(candidateSlots.begin(), candidateSlots.end(), 
                               std::default_random_engine(std::chrono::system_clock::now().time_since_epoch().count()));
                }
                
                // Try each candidate
                for (const auto& [timeSlot, room] : candidateSlots) {
                    assignment.time_slot = timeSlot;
                    assignment.room = room;
                    
                    // Check for conflicts
                    if (!checkTeacherConflict(assignment) && 
                        !checkRoomConflict(assignment) && 
                        !checkBatchConflict(assignment)) {
                        
                        currentSchedule.push_back(assignment);
                        scheduled = true;
                        successfullyScheduled++;
                        
                        std::cout << "   ✅ Scheduled at " << timeSlot.day_of_week << " " 
                                 << timeSlot.start_time.substr(0, 5) << "-" 
                                 << timeSlot.end_time.substr(0, 5) << " in " << room.room_code << std::endl;
                        break;
                    }
                }
            }
            
            if (!scheduled) {
                std::cout << "   ❌ Failed to schedule after " << attempts << " attempts" << std::endl;
                
                // Record as conflict
                ConflictInfo conflict;
                conflict.conflict_type = "SCHEDULING_FAILED";
                conflict.description = "Could not find suitable time slot and room for " + 
                                     course.course_code + " (" + course.batch_code + "-" + course.section_name + ")";
                conflict.severity = "HIGH";
                detectedConflicts.push_back(conflict);
            }
        }
    }
    
    std::cout << "\n📊 Scheduling Summary:" << std::endl;
    std::cout << "   ✅ Successfully scheduled: " << successfullyScheduled << "/" << totalCoursesToSchedule << std::endl;
    std::cout << "   📈 Success rate: " << std::fixed << std::setprecision(1) 
              << (100.0 * successfullyScheduled / totalCoursesToSchedule) << "%" << std::endl;
    std::cout << "   ⚠️ Conflicts detected: " << detectedConflicts.size() << std::endl;
    
    // Save to database
    if (successfullyScheduled > 0) {
        std::cout << "\n💾 Saving schedule to database..." << std::endl;
        
        for (const auto& assignment : currentSchedule) {
            // Get section ID
            auto sections = dbManager->getAllSections();
            auto sectionIt = std::find_if(sections.begin(), sections.end(),
                [&](const DatabaseManager::AcademicSection& s) {
                    return s.course_id == assignment.course.course_id && 
                           s.section_name == assignment.course.section_name;
                });
            
            if (sectionIt != sections.end()) {
                DatabaseManager::AcademicSchedule schedule;
                schedule.course_id = assignment.course.course_id;
                schedule.section_id = sectionIt->section_id;
                schedule.teacher_id = assignment.course.teacher_id;
                schedule.room_id = assignment.room.room_id;
                schedule.slot_id = assignment.time_slot.slot_id;
                schedule.session_number = assignment.session_number;
                schedule.academic_year = academic_year;
                schedule.semester = semester;
                schedule.status = "SCHEDULED";
                schedule.notes = "Generated by Enhanced Routine Generator";
                
                // Insert into database
                dbManager->insertAcademicSchedule(schedule);
            }
        }
        
        std::cout << "   ✅ Schedule saved successfully!" << std::endl;
    }
    
    // Apply gap minimization optimization if enabled and we have scheduled courses
    if (minimizeGaps && successfullyScheduled > 0) {
        minimizeGapsBetweenClasses();
    }
    
    return successfullyScheduled > 0;
}

bool EnhancedRoutineGenerator::checkTeacherConflict(const ScheduleAssignment& assignment) const {
    for (const auto& existing : currentSchedule) {
        if (existing.course.teacher_id == assignment.course.teacher_id &&
            existing.time_slot.slot_id == assignment.time_slot.slot_id) {
            return true;  // Teacher conflict
        }
    }
    return false;
}

bool EnhancedRoutineGenerator::checkRoomConflict(const ScheduleAssignment& assignment) const {
    for (const auto& existing : currentSchedule) {
        if (existing.room.room_id == assignment.room.room_id &&
            existing.time_slot.slot_id == assignment.time_slot.slot_id) {
            return true;  // Room conflict
        }
    }
    return false;
}

bool EnhancedRoutineGenerator::checkBatchConflict(const ScheduleAssignment& assignment) const {
    for (const auto& existing : currentSchedule) {
        if (existing.course.batch_code == assignment.course.batch_code &&
            existing.course.section_name == assignment.course.section_name &&
            existing.time_slot.slot_id == assignment.time_slot.slot_id) {
            return true;  // Batch-section conflict
        }
    }
    return false;
}

EnhancedRoutineGenerator::ScheduleStatistics EnhancedRoutineGenerator::getScheduleStatistics() const {
    ScheduleStatistics stats;
    
    stats.total_courses = allCourses.size();
    stats.scheduled_courses = currentSchedule.size();
    stats.total_conflicts = detectedConflicts.size();
    
    stats.teacher_conflicts = std::count_if(detectedConflicts.begin(), detectedConflicts.end(),
        [](const ConflictInfo& c) { return c.conflict_type == "TEACHER"; });
    stats.room_conflicts = std::count_if(detectedConflicts.begin(), detectedConflicts.end(),
        [](const ConflictInfo& c) { return c.conflict_type == "ROOM"; });
    stats.batch_conflicts = std::count_if(detectedConflicts.begin(), detectedConflicts.end(),
        [](const ConflictInfo& c) { return c.conflict_type == "BATCH"; });
    
    stats.schedule_efficiency = stats.total_courses > 0 ? 
        (100.0 * stats.scheduled_courses / stats.total_courses) : 0.0;
    
    // Calculate room utilization
    std::set<int> usedRooms;
    for (const auto& assignment : currentSchedule) {
        usedRooms.insert(assignment.room.room_id);
    }
    stats.room_utilization = allRooms.size() > 0 ? 
        (100.0 * usedRooms.size() / allRooms.size()) : 0.0;
    
    // Count courses per batch
    for (const auto& assignment : currentSchedule) {
        stats.courses_per_batch[assignment.course.batch_code]++;
    }
    
    // Calculate faculty workload
    std::map<int, int> teacherSessions;
    for (const auto& assignment : currentSchedule) {
        teacherSessions[assignment.course.teacher_id]++;
    }
    
    auto teachers = dbManager->getAllTeachers();
    for (const auto& teacher : teachers) {
        int sessions = teacherSessions[teacher.teacher_id];
        stats.faculty_workload[teacher.full_name] = sessions * 1.5;  // 1.5 hours per session
    }
    
    return stats;
}

void EnhancedRoutineGenerator::printScheduleSummary() const {
    auto stats = getScheduleStatistics();
    
    std::cout << "\n📊 === Schedule Summary ===" << std::endl;
    std::cout << "📚 Total Courses: " << stats.total_courses << std::endl;
    std::cout << "✅ Successfully Scheduled: " << stats.scheduled_courses << std::endl;
    std::cout << "📈 Efficiency: " << std::fixed << std::setprecision(1) << stats.schedule_efficiency << "%" << std::endl;
    std::cout << "🏢 Room Utilization: " << std::fixed << std::setprecision(1) << stats.room_utilization << "%" << std::endl;
    
    std::cout << "\n📋 Courses per Batch:" << std::endl;
    for (const auto& [batch, count] : stats.courses_per_batch) {
        std::cout << "   " << batch << ": " << count << " sessions" << std::endl;
    }
    
    std::cout << "\n👥 Faculty Workload (hours/week):" << std::endl;
    for (const auto& [faculty, hours] : stats.faculty_workload) {
        std::cout << "   " << faculty << ": " << std::fixed << std::setprecision(1) << hours << " hours" << std::endl;
    }
    
    if (!detectedConflicts.empty()) {
        std::cout << "\n⚠️ Conflicts Summary:" << std::endl;
        std::cout << "   Teacher conflicts: " << stats.teacher_conflicts << std::endl;
        std::cout << "   Room conflicts: " << stats.room_conflicts << std::endl;
        std::cout << "   Batch conflicts: " << stats.batch_conflicts << std::endl;
        std::cout << "   Other issues: " << (stats.total_conflicts - stats.teacher_conflicts - 
                                           stats.room_conflicts - stats.batch_conflicts) << std::endl;
    }
}

void EnhancedRoutineGenerator::minimizeGapsBetweenClasses() {
    std::cout << "\n🔄 Optimizing schedule to minimize gaps between classes..." << std::endl;
    
    // Group schedule assignments by batch-section
    std::map<std::string, std::vector<ScheduleAssignment*>> batchSectionSchedules;
    
    for (auto& assignment : currentSchedule) {
        std::string batchSection = assignment.course.batch_code + "-" + assignment.course.section_name;
        batchSectionSchedules[batchSection].push_back(&assignment);
    }
    
    int totalOptimizations = 0;
    
    // Process each batch-section
    for (auto& [batchSection, assignments] : batchSectionSchedules) {
        std::cout << "   📚 Optimizing " << batchSection << " with " << assignments.size() << " classes..." << std::endl;
        
        // Group assignments by day
        std::map<std::string, std::vector<ScheduleAssignment*>> daySchedules;
        for (auto* assignment : assignments) {
            daySchedules[assignment->time_slot.day_of_week].push_back(assignment);
        }
        
        // Optimize each day
        for (auto& [day, dayAssignments] : daySchedules) {
            if (dayAssignments.size() < 2) continue; // No optimization needed for single class
            
            // Sort assignments by current start time
            std::sort(dayAssignments.begin(), dayAssignments.end(),
                [](const ScheduleAssignment* a, const ScheduleAssignment* b) {
                    return a->time_slot.start_time < b->time_slot.start_time;
                });
            
            // Find available consecutive slots for this batch-section on this day
            std::vector<TimeSlotInfo> daySlots;
            for (const auto& slot : allTimeSlots) {
                if (slot.day_of_week == day && slot.is_available) {
                    daySlots.push_back(slot);
                }
            }
            
            // Sort day slots by start time
            std::sort(daySlots.begin(), daySlots.end(),
                [](const TimeSlotInfo& a, const TimeSlotInfo& b) {
                    return a.start_time < b.start_time;
                });
            
            // Try to find consecutive slots
            for (size_t i = 0; i < daySlots.size() && i + dayAssignments.size() <= daySlots.size(); ++i) {
                bool canReassign = true;
                std::vector<TimeSlotInfo> consecutiveSlots;
                
                // Check if we can get enough consecutive slots
                for (size_t j = 0; j < dayAssignments.size(); ++j) {
                    if (i + j >= daySlots.size()) {
                        canReassign = false;
                        break;
                    }
                    
                    const auto& targetSlot = daySlots[i + j];
                    auto* assignment = dayAssignments[j];
                    
                    // Check if slot type matches course requirements
                    bool slotMatches = false;
                    if (assignment->course.class_type == "THEORY" && targetSlot.duration_minutes == 90) {
                        slotMatches = true;
                    } else if (assignment->course.class_type == "LAB" && targetSlot.duration_minutes == 180) {
                        slotMatches = true;
                    }
                    
                    if (!slotMatches) {
                        canReassign = false;
                        break;
                    }
                    
                    // Check faculty availability
                    auto facultySlots = teacherAvailability[assignment->course.teacher_id];
                    bool facultyAvailable = std::any_of(facultySlots.begin(), facultySlots.end(),
                        [&](const TimeSlotInfo& fSlot) { return fSlot.slot_id == targetSlot.slot_id; });
                    
                    if (!facultyAvailable) {
                        canReassign = false;
                        break;
                    }
                    
                    // Check for conflicts (excluding current assignments for this batch-section)
                    bool hasConflict = false;
                    for (const auto& existing : currentSchedule) {
                        // Skip if it's one of our current assignments for this batch-section
                        bool isOurAssignment = false;
                        for (const auto* ourAssignment : dayAssignments) {
                            if (&existing == ourAssignment) {
                                isOurAssignment = true;
                                break;
                            }
                        }
                        if (isOurAssignment) continue;
                        
                        // Check for conflicts
                        if (existing.time_slot.slot_id == targetSlot.slot_id) {
                            // Teacher conflict
                            if (existing.course.teacher_id == assignment->course.teacher_id) {
                                hasConflict = true;
                                break;
                            }
                            // Room conflict (if we're keeping the same room)
                            if (existing.room.room_id == assignment->room.room_id) {
                                hasConflict = true;
                                break;
                            }
                        }
                    }
                    
                    if (hasConflict) {
                        canReassign = false;
                        break;
                    }
                    
                    consecutiveSlots.push_back(targetSlot);
                }
                
                // If we can reassign all classes to consecutive slots, do it
                if (canReassign && consecutiveSlots.size() == dayAssignments.size()) {
                    // Check if this actually improves the schedule (reduces gaps)
                    int currentGaps = 0;
                    int newGaps = 0;
                    
                    // Calculate current gaps
                    for (size_t j = 1; j < dayAssignments.size(); ++j) {
                        auto prevEndTime = dayAssignments[j-1]->time_slot.end_time;
                        auto currStartTime = dayAssignments[j]->time_slot.start_time;
                        if (prevEndTime < currStartTime) {
                            currentGaps++;
                        }
                    }
                    
                    // Calculate new gaps (should be 0 for consecutive slots)
                    for (size_t j = 1; j < consecutiveSlots.size(); ++j) {
                        auto prevEndTime = consecutiveSlots[j-1].end_time;
                        auto currStartTime = consecutiveSlots[j].start_time;
                        if (prevEndTime < currStartTime) {
                            newGaps++;
                        }
                    }
                    
                    // Only apply if it reduces gaps
                    if (newGaps < currentGaps) {
                        // Apply the reassignment
                        for (size_t j = 0; j < dayAssignments.size(); ++j) {
                            dayAssignments[j]->time_slot = consecutiveSlots[j];
                        }
                        
                        totalOptimizations++;
                        std::cout << "     ✅ " << batchSection << " on " << day 
                                 << ": Reduced gaps from " << currentGaps << " to " << newGaps << std::endl;
                        break; // Move to next day
                    }
                }
            }
        }
    }
    
    std::cout << "   🎯 Total optimizations applied: " << totalOptimizations << std::endl;
    
    // Note: The optimized schedule is now in memory (currentSchedule)
    // The database will be updated when the main routine generation completes
    if (totalOptimizations > 0) {
        std::cout << "   ✅ Schedule optimized in memory. Database will be updated on completion." << std::endl;
    }
}

double EnhancedRoutineGenerator::calculateGapScore(const TimeSlotInfo& candidate_slot, 
                                                  const std::vector<ScheduleAssignment>& existing_classes) const {
    if (existing_classes.empty()) {
        return 0.0; // No penalty for first class
    }
    
    double score = 0.0;
    
    // Group existing classes by day
    std::map<std::string, std::vector<std::string>> daySchedules;
    for (const auto& assignment : existing_classes) {
        daySchedules[assignment.time_slot.day_of_week].push_back(assignment.time_slot.start_time);
    }
    
    // Check if candidate slot's day already has classes
    auto dayIt = daySchedules.find(candidate_slot.day_of_week);
    if (dayIt != daySchedules.end()) {
        // Calculate minimum gap to existing classes on same day
        double minGap = std::numeric_limits<double>::max();
        
        for (const std::string& existingTime : dayIt->second) {
            // Calculate time difference in minutes
            double candidateMinutes = timeStringToMinutes(candidate_slot.start_time);
            double existingMinutes = timeStringToMinutes(existingTime);
            double gap = std::abs(candidateMinutes - existingMinutes);
            
            if (gap < minGap) {
                minGap = gap;
            }
        }
        
        // Prefer slots that create smaller gaps (lower score is better)
        // Give bonus for adjacent slots (90-minute theory classes or 180-minute lab classes)
        if (minGap <= 95) { // Adjacent or overlapping (with 5-minute buffer)
            score = 0.0; // Best score for consecutive classes
        } else if (minGap <= 185) { // One slot gap
            score = 1.0; // Small penalty for one gap
        } else if (minGap <= 275) { // Two slot gap
            score = 2.0; // Medium penalty
        } else {
            score = 3.0 + (minGap / 100.0); // Higher penalty for larger gaps
        }
    } else {
        // New day - give moderate score to encourage spreading across days
        score = 1.5;
    }
    
    return score;
}

double EnhancedRoutineGenerator::timeStringToMinutes(const std::string& timeStr) const {
    // Convert time string "HH:MM:SS" to minutes since midnight
    int hours = std::stoi(timeStr.substr(0, 2));
    int minutes = std::stoi(timeStr.substr(3, 2));
    return hours * 60.0 + minutes;
}
