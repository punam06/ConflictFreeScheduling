-- Enhanced Sample Data for BUP CSE Department Scheduling System
-- Based on Bangladesh University of Professionals requirements
-- Follows proper academic structure with batches, sections, faculty, and rooms

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
('DR.MAH', 'Dr. Md. Abdul Hamid', 'Professor', 'CSE', 'mhamid@bup.edu.bd', '+8801712345679', '08:30:00', '17:30:00', 0, 6, 24),
('DR.MSI', 'Dr. Md. Saiful Islam', 'Associate Professor', 'CSE', 'saiful@bup.edu.bd', '+8801712345680', '08:30:00', '17:30:00', 0, 6, 24),
('DR.RKS', 'Dr. Rashed Kabir Sunny', 'Assistant Professor', 'CSE', 'rashed@bup.edu.bd', '+8801712345681', '08:30:00', '17:30:00', 0, 6, 24),
('DR.FKH', 'Dr. Farhana Khandoker', 'Assistant Professor', 'CSE', 'farhana@bup.edu.bd', '+8801712345682', '08:30:00', '17:30:00', 0, 6, 24),
('MR.TAR', 'Mr. Tanvir Ahmed Rahman', 'Lecturer', 'CSE', 'tanvir@bup.edu.bd', '+8801712345683', '08:30:00', '17:30:00', 0, 6, 24),
('MS.SSK', 'Ms. Sadia Sultana Khan', 'Lecturer', 'CSE', 'sadia@bup.edu.bd', '+8801712345684', '08:30:00', '17:30:00', 0, 6, 24),
('MR.AHI', 'Mr. Ahmed Hassan Imran', 'Lecturer', 'CSE', 'ahmed@bup.edu.bd', '+8801712345685', '08:30:00', '17:30:00', 0, 6, 24),
-- External Faculty (Part-time)
('DR.EXT1', 'Dr. Mohammad Rahman', 'Adjunct Professor', 'CSE', 'ext1@bup.edu.bd', '+8801712345686', '12:00:00', '18:00:00', 1, 4, 12),
('MR.EXT2', 'Mr. Industry Expert', 'Guest Lecturer', 'CSE', 'ext2@bup.edu.bd', '+8801712345687', '14:00:00', '17:30:00', 1, 3, 9);

-- Insert BUP Classrooms (3 theory + 2 lab rooms)
INSERT OR REPLACE INTO classrooms (room_code, capacity, room_type, building, floor_number, facilities, status) VALUES
-- Theory Classrooms (3 rooms)
('CR302', 45, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC, Sound System', 'AVAILABLE'),
('CR303', 40, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'), 
('CR304', 50, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
-- Lab Rooms (2 dedicated labs)
('LAB504', 30, 'LAB', 'FBS Building', 5, 'Computers(30), Projector, AC, Programming Software', 'AVAILABLE'),
('LAB505', 35, 'LAB', 'FBS Building', 5, 'Computers(35), Projector, AC, Programming Software', 'AVAILABLE');

-- Insert BUP Time Slots (8:30 AM - 5:00 PM, with proper breaks)
INSERT OR REPLACE INTO time_slots (slot_name, day_of_week, start_time, end_time, duration_minutes, slot_type, is_available, priority) VALUES
-- Theory slots (90 minutes with breaks)
-- Sunday
('SUN_S1', 'SUN', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('SUN_S2', 'SUN', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('SUN_S3', 'SUN', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
-- Lunch Break: 13:10 - 13:55 (45 minutes)
('SUN_S4', 'SUN', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('SUN_S5', 'SUN', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('SUN_L1', 'SUN', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('SUN_L2', 'SUN', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Monday (5-10 min gaps, 45 min lunch break after 1 PM)
('MON_S1', 'MON', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('MON_S2', 'MON', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('MON_S3', 'MON', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
-- Lunch Break: 13:10 - 13:55 (45 minutes)
('MON_S4', 'MON', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('MON_S5', 'MON', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('MON_L1', 'MON', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('MON_L2', 'MON', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Tuesday (5-10 min gaps, 45 min lunch break after 1 PM)
('TUE_S1', 'TUE', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('TUE_S2', 'TUE', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('TUE_S3', 'TUE', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
-- Lunch Break: 13:10 - 13:55 (45 minutes)
('TUE_S4', 'TUE', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('TUE_S5', 'TUE', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('TUE_L1', 'TUE', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('TUE_L2', 'TUE', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Wednesday (5-10 min gaps, 45 min lunch break after 1 PM)
('WED_S1', 'WED', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('WED_S2', 'WED', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('WED_S3', 'WED', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
-- Lunch Break: 13:10 - 13:55 (45 minutes)
('WED_S4', 'WED', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('WED_S5', 'WED', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('WED_L1', 'WED', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('WED_L2', 'WED', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Thursday (5-10 min gaps, 45 min lunch break after 1 PM)
('THU_S1', 'THU', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('THU_S2', 'THU', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('THU_S3', 'THU', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
-- Lunch Break: 13:10 - 13:55 (45 minutes)
('THU_S4', 'THU', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('THU_S5', 'THU', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('THU_L1', 'THU', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('THU_L2', 'THU', '13:55:00', '16:55:00', 180, 'LAB', 1, 2);

-- Insert BUP CSE Courses with proper credit structure
INSERT OR REPLACE INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, description, status) VALUES
-- BCSE 24th Batch (1st Year) Courses
('CSE1101', 'Computer Fundamentals', 3.0, 'THEORY', 90, 2, 4, 1, 'Introduction to computer systems and programming', 'ACTIVE'),
('CSE1102', 'Programming Fundamentals', 3.0, 'THEORY', 90, 2, 4, 2, 'Basic programming concepts using C', 'ACTIVE'),
('CSE1103', 'Programming Lab', 1.5, 'LAB', 180, 1, 4, 6, 'Hands-on programming practice', 'ACTIVE'),
('MAT1101', 'Calculus I', 3.0, 'THEORY', 90, 2, 4, 9, 'Differential and integral calculus', 'ACTIVE'),
('ENG1101', 'English Composition', 3.0, 'THEORY', 90, 2, 4, 10, 'Academic writing and communication', 'ACTIVE'),

-- BCSE 23rd Batch (2nd Year) Courses  
('CSE2201', 'Data Structures', 3.0, 'THEORY', 90, 2, 3, 2, 'Arrays, linked lists, stacks, queues, trees', 'ACTIVE'),
('CSE2202', 'Object Oriented Programming', 3.0, 'THEORY', 90, 2, 3, 3, 'OOP concepts using Java/C++', 'ACTIVE'),
('CSE2203', 'OOP Lab', 1.5, 'LAB', 180, 1, 3, 7, 'Object oriented programming practice', 'ACTIVE'),
('CSE2204', 'Digital Logic Design', 3.0, 'THEORY', 90, 2, 3, 4, 'Boolean algebra and digital circuits', 'ACTIVE'),
('MAT2201', 'Discrete Mathematics', 3.0, 'THEORY', 90, 2, 3, 9, 'Logic, sets, relations, graph theory', 'ACTIVE'),

-- BCSE 22nd Batch (3rd Year) Courses
('CSE3301', 'Algorithms', 3.0, 'THEORY', 90, 2, 2, 1, 'Algorithm design and analysis', 'ACTIVE'),
('CSE3302', 'Database Systems', 3.0, 'THEORY', 90, 2, 2, 3, 'Database design and SQL', 'ACTIVE'),
('CSE3303', 'Database Lab', 1.5, 'LAB', 180, 1, 2, 8, 'Database implementation and queries', 'ACTIVE'),
('CSE3304', 'Computer Networks', 3.0, 'THEORY', 90, 2, 2, 4, 'Network protocols and architecture', 'ACTIVE'),
('CSE3305', 'Software Engineering', 3.0, 'THEORY', 90, 2, 2, 5, 'Software development lifecycle', 'ACTIVE'),

-- BCSE 21st Batch (4th Year) Courses
('CSE4401', 'Operating Systems', 3.0, 'THEORY', 90, 2, 1, 1, 'OS concepts and system programming', 'ACTIVE'),
('CSE4402', 'Artificial Intelligence', 3.0, 'THEORY', 90, 2, 1, 2, 'AI algorithms and applications', 'ACTIVE'),
('CSE4403', 'Machine Learning', 3.0, 'THEORY', 90, 2, 1, 3, 'ML algorithms and data science', 'ACTIVE'),
('CSE4404', 'Capstone Project', 3.0, 'THEORY', 90, 2, 1, 5, 'Final year project work', 'ACTIVE'),
('CSE4405', 'Project Lab', 1.5, 'LAB', 180, 1, 1, 6, 'Project development and presentation', 'ACTIVE');

-- Insert Course Sections (A and B for each course)
INSERT OR REPLACE INTO course_sections (course_id, section_name, max_students, enrolled_students, status) VALUES
-- BCSE24 sections
(1, 'A', 40, 35, 'ACTIVE'), (1, 'B', 40, 38, 'ACTIVE'),
(2, 'A', 40, 36, 'ACTIVE'), (2, 'B', 40, 34, 'ACTIVE'),
(3, 'A', 30, 28, 'ACTIVE'), (3, 'B', 30, 27, 'ACTIVE'),
(4, 'A', 40, 37, 'ACTIVE'), (4, 'B', 40, 39, 'ACTIVE'),
(5, 'A', 40, 33, 'ACTIVE'), (5, 'B', 40, 35, 'ACTIVE'),
-- BCSE23 sections
(6, 'A', 40, 32, 'ACTIVE'), (6, 'B', 40, 30, 'ACTIVE'),
(7, 'A', 40, 31, 'ACTIVE'), (7, 'B', 40, 33, 'ACTIVE'),
(8, 'A', 30, 25, 'ACTIVE'), (8, 'B', 30, 24, 'ACTIVE'),
(9, 'A', 40, 29, 'ACTIVE'), (9, 'B', 40, 31, 'ACTIVE'),
(10, 'A', 40, 28, 'ACTIVE'), (10, 'B', 40, 26, 'ACTIVE'),
-- BCSE22 sections
(11, 'A', 40, 27, 'ACTIVE'), (11, 'B', 40, 25, 'ACTIVE'),
(12, 'A', 40, 24, 'ACTIVE'), (12, 'B', 40, 26, 'ACTIVE'),
(13, 'A', 30, 22, 'ACTIVE'), (13, 'B', 30, 21, 'ACTIVE'),
(14, 'A', 40, 23, 'ACTIVE'), (14, 'B', 40, 25, 'ACTIVE'),
(15, 'A', 40, 22, 'ACTIVE'), (15, 'B', 40, 24, 'ACTIVE'),
-- BCSE21 sections
(16, 'A', 40, 20, 'ACTIVE'), (16, 'B', 40, 22, 'ACTIVE'),
(17, 'A', 40, 19, 'ACTIVE'), (17, 'B', 40, 21, 'ACTIVE'),
(18, 'A', 40, 18, 'ACTIVE'), (18, 'B', 40, 20, 'ACTIVE'),
(19, 'A', 40, 17, 'ACTIVE'), (19, 'B', 40, 19, 'ACTIVE'),
(20, 'A', 30, 16, 'ACTIVE'), (20, 'B', 30, 18, 'ACTIVE');

-- Insert classrooms  
INSERT OR REPLACE INTO classrooms (room_code, capacity, room_type, facilities, building, floor_number) VALUES
('R101', 45, 'LAB', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R102', 40, 'LAB', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R103', 35, 'LAB', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R104', 25, 'LAB', 'High-end Computers, Servers, Projector', 'Main Building', 1),
('R201', 50, 'THEORY', 'Projector, Whiteboard, Audio System', 'Main Building', 2),
('R202', 45, 'THEORY', 'Projector, Whiteboard, Audio System', 'Main Building', 2),
('R203', 40, 'THEORY', 'Projector, Whiteboard', 'Main Building', 2),
('R204', 100, 'THEORY', 'Projector, Audio System, Stage', 'Main Building', 2),
('R301', 30, 'THEORY', 'Projector, Whiteboard', 'Main Building', 3),
('R302', 25, 'THEORY', 'Projector, Whiteboard', 'Main Building', 3),
('R303', 20, 'THEORY', 'Projector, Round Table', 'Main Building', 3),
('R401', 15, 'LAB', 'High-end Computers, Servers', 'Research Building', 4);

-- Insert time slots (Monday to Friday, 5 slots per day)
INSERT OR REPLACE INTO time_slots (slot_name, day_of_week, start_time, end_time, slot_type) VALUES
-- Monday
('MON1', 'MON', '08:00:00', '09:30:00', 'Morning'),
('MON2', 'MON', '09:45:00', '11:15:00', 'Morning'),
('MON3', 'MON', '11:30:00', '13:00:00', 'Late Morning'),
('MON4', 'MON', '14:00:00', '15:30:00', 'Afternoon'),
('MON5', 'MON', '15:45:00', '17:15:00', 'Afternoon'),
-- Tuesday
('TUE1', 'TUE', '08:00:00', '09:30:00', 'Morning'),
('TUE2', 'TUE', '09:45:00', '11:15:00', 'Morning'),
('TUE3', 'TUE', '11:30:00', '13:00:00', 'Late Morning'),
('TUE4', 'TUE', '14:00:00', '15:30:00', 'Afternoon'),
('TUE5', 'TUE', '15:45:00', '17:15:00', 'Afternoon'),
-- Wednesday
('WED1', 'WED', '08:00:00', '09:30:00', 'Morning'),
('WED2', 'WED', '09:45:00', '11:15:00', 'Morning'),
('WED3', 'WED', '11:30:00', '13:00:00', 'Late Morning'),
('WED4', 'WED', '14:00:00', '15:30:00', 'Afternoon'),
('WED5', 'WED', '15:45:00', '17:15:00', 'Afternoon'),
-- Thursday
('THU1', 'THU', '08:00:00', '09:30:00', 'Morning'),
('THU2', 'THU', '09:45:00', '11:15:00', 'Morning'),
('THU3', 'THU', '11:30:00', '13:00:00', 'Late Morning'),
('THU4', 'THU', '14:00:00', '15:30:00', 'Afternoon'),
('THU5', 'THU', '15:45:00', '17:15:00', 'Afternoon'),
-- Friday
('FRI1', 'FRI', '08:00:00', '09:30:00', 'Morning'),
('FRI2', 'FRI', '09:45:00', '11:15:00', 'Morning'),
('FRI3', 'FRI', '11:30:00', '13:00:00', 'Late Morning'),
('FRI4', 'FRI', '14:00:00', '15:30:00', 'Afternoon'),
('FRI5', 'FRI', '15:45:00', '17:15:00', 'Afternoon');

-- Insert some sample conflicts for testing (Note: These would typically be generated by the system)
-- We need actual schedule_ids from the schedule table, so these are just examples
-- INSERT OR REPLACE INTO schedule_conflicts (conflict_type, schedule_id_1, schedule_id_2, conflict_description, is_resolved) VALUES
-- ('ROOM_OVERLAP', 1, 2, 'Two courses scheduled in same room at overlapping times', 0),
-- ('TEACHER_OVERLAP', 3, 4, 'Same teacher assigned to overlapping time slots', 1),
-- ('BATCH_OVERLAP', 5, 6, 'Same batch has conflicting course schedules', 0);
