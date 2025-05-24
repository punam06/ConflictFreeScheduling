-- SQLite Database Schema for BUP Conflict-Free Scheduling System
-- Based on Bangladesh University of Professionals - CSE Department
-- This file contains all table definitions and relationships

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Batches table (representing different academic years/semesters)
CREATE TABLE IF NOT EXISTS batches (
    batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_code VARCHAR(20) NOT NULL UNIQUE,
    batch_name VARCHAR(100) NOT NULL,
    year_level INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    total_sections INTEGER DEFAULT 2,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Teachers table with external faculty support
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    designation VARCHAR(50),
    department VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    availability_start TIME DEFAULT '08:30:00',
    availability_end TIME DEFAULT '17:30:00',
    external_faculty BOOLEAN DEFAULT 0,
    max_hours_per_day INTEGER DEFAULT 6,
    max_hours_per_week INTEGER DEFAULT 30,
    preferred_time_slot VARCHAR(20) DEFAULT 'ANY',
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Classrooms table with BUP-specific room types
CREATE TABLE IF NOT EXISTS classrooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_code VARCHAR(20) NOT NULL UNIQUE,
    capacity INTEGER NOT NULL,
    room_type VARCHAR(20) NOT NULL DEFAULT 'THEORY', -- THEORY, LAB, BOTH
    building VARCHAR(50),
    floor_number INTEGER,
    facilities TEXT,
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced courses table matching BUP structure
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(15) NOT NULL UNIQUE,
    course_title VARCHAR(100) NOT NULL,
    credit_hours REAL NOT NULL,
    class_type VARCHAR(20) NOT NULL, -- THEORY, LAB
    session_duration INTEGER NOT NULL, -- Duration in minutes (90 for theory, 180 for lab)
    sessions_per_week INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    prerequisite_course_id INTEGER,
    description TEXT,
    department VARCHAR(50) DEFAULT 'CSE',
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE RESTRICT,
    FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);

-- Course sections table (A and B sections)
CREATE TABLE IF NOT EXISTS course_sections (
    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    section_name VARCHAR(5) NOT NULL, -- A, B
    max_students INTEGER DEFAULT 40,
    enrolled_students INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE(course_id, section_name)
);

-- Time slots table with BUP schedule structure
CREATE TABLE IF NOT EXISTS time_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_name VARCHAR(20) NOT NULL UNIQUE,
    day_of_week VARCHAR(3) NOT NULL, -- SUN, MON, TUE, WED, THU, FRI, SAT
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_minutes INTEGER,
    slot_type VARCHAR(20) DEFAULT 'REGULAR',
    is_available BOOLEAN DEFAULT 1,
    priority INTEGER DEFAULT 1, -- Higher priority slots are preferred
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Main schedule table
CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    section_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    session_number INTEGER DEFAULT 1, -- For multiple sessions per week
    academic_year VARCHAR(10) NOT NULL,
    semester VARCHAR(20) NOT NULL, -- SPRING, SUMMER, FALL
    status VARCHAR(20) DEFAULT 'SCHEDULED',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES course_sections(section_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE RESTRICT,
    FOREIGN KEY (room_id) REFERENCES classrooms(room_id) ON DELETE RESTRICT,
    FOREIGN KEY (slot_id) REFERENCES time_slots(slot_id) ON DELETE RESTRICT,
    UNIQUE(course_id, section_id, session_number, academic_year, semester)
);

-- Teacher constraints table
CREATE TABLE IF NOT EXISTS teacher_constraints (
    constraint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    day_of_week VARCHAR(3),
    unavailable_start_time TIME,
    unavailable_end_time TIME,
    constraint_type VARCHAR(20) NOT NULL, -- UNAVAILABLE, PREFERRED, RESTRICTED
    reason VARCHAR(255),
    priority INTEGER DEFAULT 1,
    is_permanent BOOLEAN DEFAULT 0,
    valid_from DATE DEFAULT CURRENT_DATE,
    valid_to DATE DEFAULT '2099-12-31',
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

-- Room constraints table
CREATE TABLE IF NOT EXISTS room_constraints (
    constraint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    day_of_week VARCHAR(3),
    unavailable_start_time TIME,
    unavailable_end_time TIME,
    constraint_type VARCHAR(20) NOT NULL, -- MAINTENANCE, RESERVED, UNAVAILABLE
    reason VARCHAR(255),
    valid_from DATE DEFAULT CURRENT_DATE,
    valid_to DATE DEFAULT '2099-12-31',
    FOREIGN KEY (room_id) REFERENCES classrooms(room_id) ON DELETE CASCADE
);

-- Conflict detection table
CREATE TABLE IF NOT EXISTS schedule_conflicts (
    conflict_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conflict_type VARCHAR(30) NOT NULL, -- TEACHER_OVERLAP, ROOM_OVERLAP, BATCH_OVERLAP, TIME_CONSTRAINT
    schedule_id_1 INTEGER NOT NULL,
    schedule_id_2 INTEGER,
    conflict_description TEXT,
    severity VARCHAR(20) DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH, CRITICAL
    is_resolved BOOLEAN DEFAULT 0,
    resolution_notes TEXT,
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (schedule_id_1) REFERENCES schedule(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id_2) REFERENCES schedule(schedule_id) ON DELETE CASCADE
);

-- System settings table
CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(50) NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    setting_type VARCHAR(20) DEFAULT 'STRING', -- STRING, INTEGER, BOOLEAN, TIME, JSON
    description TEXT,
    is_editable BOOLEAN DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Routine generation log table
CREATE TABLE IF NOT EXISTS routine_generation_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_id VARCHAR(36) NOT NULL UNIQUE,
    academic_year VARCHAR(10) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    algorithm_used VARCHAR(30) NOT NULL, -- GRAPH_COLORING, BACKTRACKING, HYBRID
    execution_time_ms INTEGER,
    total_courses INTEGER,
    total_conflicts INTEGER,
    conflicts_resolved INTEGER,
    optimization_score REAL,
    status VARCHAR(20) DEFAULT 'RUNNING', -- RUNNING, COMPLETED, FAILED, CANCELLED
    error_message TEXT,
    generated_by VARCHAR(50),
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_batches_code ON batches(batch_code);
CREATE INDEX IF NOT EXISTS idx_teachers_code ON teachers(teacher_code);
CREATE INDEX IF NOT EXISTS idx_teachers_external ON teachers(external_faculty);
CREATE INDEX IF NOT EXISTS idx_classrooms_code ON classrooms(room_code);
CREATE INDEX IF NOT EXISTS idx_classrooms_type ON classrooms(room_type);
CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(course_code);
CREATE INDEX IF NOT EXISTS idx_courses_batch ON courses(batch_id);
CREATE INDEX IF NOT EXISTS idx_timeslots_day ON time_slots(day_of_week);
CREATE INDEX IF NOT EXISTS idx_schedule_teacher ON schedule(teacher_id, slot_id);
CREATE INDEX IF NOT EXISTS idx_schedule_room ON schedule(room_id, slot_id);
CREATE INDEX IF NOT EXISTS idx_conflicts_unresolved ON schedule_conflicts(is_resolved, detected_at);

-- Triggers for updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_batches_timestamp 
    AFTER UPDATE ON batches
    BEGIN
        UPDATE batches SET updated_at = CURRENT_TIMESTAMP WHERE batch_id = NEW.batch_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_teachers_timestamp 
    AFTER UPDATE ON teachers
    BEGIN
        UPDATE teachers SET updated_at = CURRENT_TIMESTAMP WHERE teacher_id = NEW.teacher_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_classrooms_timestamp 
    AFTER UPDATE ON classrooms
    BEGIN
        UPDATE classrooms SET updated_at = CURRENT_TIMESTAMP WHERE room_id = NEW.room_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_courses_timestamp 
    AFTER UPDATE ON courses
    BEGIN
        UPDATE courses SET updated_at = CURRENT_TIMESTAMP WHERE course_id = NEW.course_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_schedule_timestamp 
    AFTER UPDATE ON schedule
    BEGIN
        UPDATE schedule SET updated_at = CURRENT_TIMESTAMP WHERE schedule_id = NEW.schedule_id;
    END;
