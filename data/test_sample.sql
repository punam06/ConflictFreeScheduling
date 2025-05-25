-- Test sample data with foreign keys disabled temporarily
PRAGMA foreign_keys = OFF;

-- Insert Batches (BCSE 21st-24th, 8 sections total)
INSERT OR REPLACE INTO batches (batch_code, batch_name, year_level, semester, total_sections, status) VALUES
('BCSE21', 'Bachelor of Computer Science & Engineering - 21st Batch', 4, 8, 2, 'ACTIVE'),
('BCSE22', 'Bachelor of Computer Science & Engineering - 22nd Batch', 3, 6, 2, 'ACTIVE'),
('BCSE23', 'Bachelor of Computer Science & Engineering - 23rd Batch', 2, 4, 2, 'ACTIVE'),
('BCSE24', 'Bachelor of Computer Science & Engineering - 24th Batch', 1, 2, 2, 'ACTIVE');

-- Insert Faculty Members (BUP CSE Department)
INSERT OR REPLACE INTO teachers (teacher_code, full_name, designation, department, email, phone, availability_start, availability_end, external_faculty, max_hours_per_day, max_hours_per_week) VALUES
-- Core Faculty
('DR.ASM', 'Dr. Abu Sayed Md. Latiful Hoque', 'Professor & Head', 'CSE', 'asayed@bup.edu.bd', '+8801712345678', '08:30:00', '17:30:00', 0, 6, 24),
('DR.MAH', 'Dr. Md. Abdul Hamid', 'Professor', 'CSE', 'mhamid@bup.edu.bd', '+8801712345679', '08:30:00', '17:30:00', 0, 6, 24);

-- Insert BUP Classrooms (FBS Building)
INSERT OR REPLACE INTO classrooms (room_code, capacity, room_type, building, floor_number, facilities, status) VALUES
-- Theory Classrooms
('CR302', 45, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC, Sound System', 'AVAILABLE'),
('CR303', 40, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE');

-- Insert some time slots
INSERT OR REPLACE INTO time_slots (slot_name, day_of_week, start_time, end_time, duration_minutes, slot_type, is_available, priority) VALUES
('SUN_S1', 'SUN', '08:30:00', '10:00:00', 90, 'THEORY', 1, 1),
('SUN_S2', 'SUN', '10:10:00', '11:40:00', 90, 'THEORY', 1, 1);

-- Insert just a few courses to test
INSERT OR REPLACE INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, description, status) VALUES
('CSE1101', 'Computer Fundamentals', 3.0, 'THEORY', 90, 2, 4, 1, 'Introduction to computer systems and programming', 'ACTIVE'),
('CSE1102', 'Programming Fundamentals', 3.0, 'THEORY', 90, 2, 4, 2, 'Basic programming concepts using C', 'ACTIVE');

-- Insert Course Sections for the test courses
INSERT OR REPLACE INTO course_sections (course_id, section_name, max_students, enrolled_students, status) VALUES
(1, 'A', 40, 35, 'ACTIVE'), (1, 'B', 40, 38, 'ACTIVE'),
(2, 'A', 40, 36, 'ACTIVE'), (2, 'B', 40, 34, 'ACTIVE');

-- Re-enable foreign keys
PRAGMA foreign_keys = ON;
