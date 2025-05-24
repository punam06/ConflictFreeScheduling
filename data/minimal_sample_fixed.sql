-- Minimal sample data for testing the database functionality
-- Insert a basic batch
INSERT OR IGNORE INTO batches (batch_id, batch_code, batch_name, year_level, semester) 
VALUES (1, 'CSE23A', 'CSE 2023 Batch A', 2, 2);

-- Insert a basic teacher  
INSERT OR IGNORE INTO teachers (teacher_id, teacher_code, full_name, designation, department, email) 
VALUES (1, 'T001', 'Dr. Sample Teacher', 'Associate Professor', 'CSE', 'teacher@bup.edu.bd');

-- Insert a basic classroom
INSERT OR IGNORE INTO classrooms (room_id, room_code, capacity, room_type, building, floor_number)
VALUES (1, 'LAB001', 40, 'LAB', 'Academic Building', 1);

-- Insert basic time slots
INSERT OR IGNORE INTO time_slots (slot_id, slot_name, start_time, end_time, duration_minutes, day_of_week)
VALUES 
(1, 'Morning 1', '09:00', '10:30', 90, 'Sunday'),
(2, 'Morning 2', '10:45', '12:15', 90, 'Sunday');

-- Insert a basic course using schema column names
INSERT OR IGNORE INTO courses (course_id, course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, description) 
VALUES (1, 'CSE1101', 'Programming Fundamentals', 3.0, 'THEORY', 90, 2, 1, 1, 'Basic programming concepts');
