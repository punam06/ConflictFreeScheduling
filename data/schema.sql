-- SQLite Database Schema for Conflict-Free Scheduling System
-- This file contains all table definitions and relationships

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(10) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    instructor VARCHAR(100) NOT NULL,
    duration INTEGER NOT NULL DEFAULT 3,
    priority INTEGER NOT NULL DEFAULT 1,
    capacity INTEGER NOT NULL DEFAULT 30,
    room_requirement VARCHAR(20) DEFAULT 'Regular',
    department VARCHAR(50) DEFAULT 'CSE',
    semester INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_code VARCHAR(10) NOT NULL UNIQUE,
    room_name VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    room_type VARCHAR(20) NOT NULL DEFAULT 'Regular',
    equipment TEXT,
    building VARCHAR(50),
    floor INTEGER,
    is_available BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Time slots table
CREATE TABLE IF NOT EXISTS time_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week INTEGER NOT NULL, -- 1=Monday, 2=Tuesday, etc.
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_type VARCHAR(20) DEFAULT 'Regular',
    is_available BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(day_of_week, start_time, end_time)
);

-- Schedule assignments table
CREATE TABLE IF NOT EXISTS schedule_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    semester VARCHAR(20) NOT NULL,
    academic_year VARCHAR(10) NOT NULL,
    assignment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE RESTRICT,
    FOREIGN KEY (slot_id) REFERENCES time_slots(slot_id) ON DELETE RESTRICT,
    UNIQUE(room_id, slot_id, semester, academic_year),
    UNIQUE(course_id, semester, academic_year)
);

-- Conflicts log table
CREATE TABLE IF NOT EXISTS conflicts_log (
    conflict_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conflict_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    course_id_1 INTEGER,
    course_id_2 INTEGER,
    room_id INTEGER,
    slot_id INTEGER,
    resolved BOOLEAN DEFAULT 0,
    resolution_method VARCHAR(100),
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (course_id_1) REFERENCES courses(course_id),
    FOREIGN KEY (course_id_2) REFERENCES courses(course_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (slot_id) REFERENCES time_slots(slot_id)
);

-- Scheduling preferences table
CREATE TABLE IF NOT EXISTS scheduling_preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    preferred_slot_id INTEGER,
    preferred_room_id INTEGER,
    preference_type VARCHAR(20) NOT NULL, -- 'required', 'preferred', 'avoid'
    priority INTEGER DEFAULT 1,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (preferred_slot_id) REFERENCES time_slots(slot_id),
    FOREIGN KEY (preferred_room_id) REFERENCES rooms(room_id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_courses_department ON courses(department);
CREATE INDEX IF NOT EXISTS idx_courses_semester ON courses(semester);
CREATE INDEX IF NOT EXISTS idx_rooms_type ON rooms(room_type);
CREATE INDEX IF NOT EXISTS idx_timeslots_day ON time_slots(day_of_week);
CREATE INDEX IF NOT EXISTS idx_assignments_semester ON schedule_assignments(semester, academic_year);
CREATE INDEX IF NOT EXISTS idx_conflicts_unresolved ON conflicts_log(resolved, detected_at);

-- Triggers for updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_courses_timestamp 
    AFTER UPDATE ON courses
    BEGIN
        UPDATE courses SET updated_at = CURRENT_TIMESTAMP WHERE course_id = NEW.course_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_rooms_timestamp 
    AFTER UPDATE ON rooms
    BEGIN
        UPDATE rooms SET updated_at = CURRENT_TIMESTAMP WHERE room_id = NEW.room_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_assignments_timestamp 
    AFTER UPDATE ON schedule_assignments
    BEGIN
        UPDATE schedule_assignments SET updated_at = CURRENT_TIMESTAMP WHERE assignment_id = NEW.assignment_id;
    END;
