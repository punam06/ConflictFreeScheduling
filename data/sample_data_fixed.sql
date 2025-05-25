-- Enhanced Sample Data for BUP CSE Department Scheduling System
-- Based on Bangladesh University of Professionals requirements
-- Follows proper academic structure with batches, sections, faculty, and rooms
-- CORRECTED VERSION - Matches exact requirements: 4 batches, 8 sections, 6 in-house faculty, 5 classrooms

-- Insert Batches (BCSE 21st-24th, 8 sections total)
INSERT OR REPLACE INTO batches (batch_code, batch_name, year_level, semester, total_sections, status) VALUES
('BCSE21', 'Bachelor of Computer Science & Engineering - 21st Batch', 4, 8, 2, 'ACTIVE'),
('BCSE22', 'Bachelor of Computer Science & Engineering - 22nd Batch', 3, 6, 2, 'ACTIVE'),
('BCSE23', 'Bachelor of Computer Science & Engineering - 23rd Batch', 2, 4, 2, 'ACTIVE'),
('BCSE24', 'Bachelor of Computer Science & Engineering - 24th Batch', 1, 2, 2, 'ACTIVE');

-- Insert Faculty Members (BUP CSE Department) - EXACTLY 6 IN-HOUSE FACULTY
INSERT OR REPLACE INTO teachers (teacher_code, full_name, designation, department, email, phone, availability_start, availability_end, external_faculty, max_hours_per_day, max_hours_per_week) VALUES
-- Core Faculty (6 in-house faculty members)
('DR.ASM', 'Dr. Abu Sayed Md. Latiful Hoque', 'Professor & Head', 'CSE', 'asayed@bup.edu.bd', '+8801712345678', '08:30:00', '17:30:00', 0, 6, 24),
('DR.MAH', 'Dr. Md. Abdul Hamid', 'Professor', 'CSE', 'mhamid@bup.edu.bd', '+8801712345679', '08:30:00', '17:30:00', 0, 6, 24),
('DR.MSI', 'Dr. Md. Saiful Islam', 'Associate Professor', 'CSE', 'saiful@bup.edu.bd', '+8801712345680', '08:30:00', '17:30:00', 0, 6, 24),
('DR.RKS', 'Dr. Rashed Kabir Sunny', 'Assistant Professor', 'CSE', 'rashed@bup.edu.bd', '+8801712345681', '08:30:00', '17:30:00', 0, 6, 24),
('DR.FKH', 'Dr. Farhana Khandoker', 'Assistant Professor', 'CSE', 'farhana@bup.edu.bd', '+8801712345682', '08:30:00', '17:30:00', 0, 6, 24),
('MR.TAR', 'Mr. Tanvir Ahmed Rahman', 'Lecturer', 'CSE', 'tanvir@bup.edu.bd', '+8801712345683', '08:30:00', '17:30:00', 0, 6, 24);

-- Insert BUP Classrooms (5 classrooms total: 3 theory + 2 lab rooms)
INSERT OR REPLACE INTO classrooms (room_code, capacity, room_type, building, floor_number, facilities, status) VALUES
-- Theory Classrooms (3 rooms)
('CR302', 45, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC, Sound System', 'AVAILABLE'),
('CR303', 40, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'), 
('CR304', 50, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
-- Lab Rooms (2 dedicated labs)
('LAB504', 30, 'LAB', 'FBS Building', 5, 'Computers(30), Projector, AC, Programming Software', 'AVAILABLE'),
('LAB505', 35, 'LAB', 'FBS Building', 5, 'Computers(35), Projector, AC, Programming Software', 'AVAILABLE');

-- Insert BUP Time Slots (8:30 AM - 5:00 PM, with proper breaks)
-- STANDARDIZED FORMAT: SUN-THU schedule
INSERT OR REPLACE INTO time_slots (slot_name, day_of_week, start_time, end_time, duration_minutes, slot_type, is_available, priority) VALUES
-- Sunday
('SUN_S1', 'SUN', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('SUN_S2', 'SUN', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('SUN_S3', 'SUN', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
('SUN_S4', 'SUN', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('SUN_S5', 'SUN', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('SUN_L1', 'SUN', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('SUN_L2', 'SUN', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Monday
('MON_S1', 'MON', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('MON_S2', 'MON', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('MON_S3', 'MON', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
('MON_S4', 'MON', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('MON_S5', 'MON', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('MON_L1', 'MON', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('MON_L2', 'MON', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Tuesday
('TUE_S1', 'TUE', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('TUE_S2', 'TUE', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('TUE_S3', 'TUE', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
('TUE_S4', 'TUE', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('TUE_S5', 'TUE', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('TUE_L1', 'TUE', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('TUE_L2', 'TUE', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Wednesday
('WED_S1', 'WED', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('WED_S2', 'WED', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('WED_S3', 'WED', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
('WED_S4', 'WED', '13:55:00', '15:25:00', 90, 'THEORY', 1, 2),
('WED_S5', 'WED', '15:30:00', '17:00:00', 90, 'THEORY', 1, 1),
('WED_L1', 'WED', '08:30:00', '11:30:00', 180, 'LAB', 1, 3),
('WED_L2', 'WED', '13:55:00', '16:55:00', 180, 'LAB', 1, 2),
-- Thursday
('THU_S1', 'THU', '08:30:00', '10:00:00', 90, 'THEORY', 1, 5),
('THU_S2', 'THU', '10:05:00', '11:35:00', 90, 'THEORY', 1, 4),
('THU_S3', 'THU', '11:40:00', '13:10:00', 90, 'THEORY', 1, 3),
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
('MAT1101', 'Calculus I', 3.0, 'THEORY', 90, 2, 4, 3, 'Differential and integral calculus', 'ACTIVE'),
('ENG1101', 'English Composition', 3.0, 'THEORY', 90, 2, 4, 4, 'Academic writing and communication', 'ACTIVE'),

-- BCSE 23rd Batch (2nd Year) Courses  
('CSE2201', 'Data Structures', 3.0, 'THEORY', 90, 2, 3, 2, 'Arrays, linked lists, stacks, queues, trees', 'ACTIVE'),
('CSE2202', 'Object Oriented Programming', 3.0, 'THEORY', 90, 2, 3, 3, 'OOP concepts using Java/C++', 'ACTIVE'),
('CSE2203', 'OOP Lab', 1.5, 'LAB', 180, 1, 3, 6, 'Object oriented programming practice', 'ACTIVE'),
('CSE2204', 'Digital Logic Design', 3.0, 'THEORY', 90, 2, 3, 4, 'Boolean algebra and digital circuits', 'ACTIVE'),
('MAT2201', 'Discrete Mathematics', 3.0, 'THEORY', 90, 2, 3, 5, 'Logic, sets, relations, graph theory', 'ACTIVE'),

-- BCSE 22nd Batch (3rd Year) Courses
('CSE3301', 'Algorithms', 3.0, 'THEORY', 90, 2, 2, 1, 'Algorithm design and analysis', 'ACTIVE'),
('CSE3302', 'Database Systems', 3.0, 'THEORY', 90, 2, 2, 3, 'Database design and SQL', 'ACTIVE'),
('CSE3303', 'Database Lab', 1.5, 'LAB', 180, 1, 2, 6, 'Database implementation and queries', 'ACTIVE'),
('CSE3304', 'Computer Networks', 3.0, 'THEORY', 90, 2, 2, 4, 'Network protocols and architecture', 'ACTIVE'),
('CSE3305', 'Software Engineering', 3.0, 'THEORY', 90, 2, 2, 5, 'Software development lifecycle', 'ACTIVE'),

-- BCSE 21st Batch (4th Year) Courses
('CSE4401', 'Operating Systems', 3.0, 'THEORY', 90, 2, 1, 1, 'OS concepts and system programming', 'ACTIVE'),
('CSE4402', 'Artificial Intelligence', 3.0, 'THEORY', 90, 2, 1, 2, 'AI algorithms and applications', 'ACTIVE'),
('CSE4403', 'Machine Learning', 3.0, 'THEORY', 90, 2, 1, 3, 'ML algorithms and data science', 'ACTIVE'),
('CSE4404', 'Capstone Project', 3.0, 'THEORY', 90, 2, 1, 5, 'Final year project work', 'ACTIVE'),
('CSE4405', 'Project Lab', 1.5, 'LAB', 180, 1, 1, 6, 'Project development and presentation', 'ACTIVE');

-- Insert Course Sections (A and B for each course) - 8 sections total per batch
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
