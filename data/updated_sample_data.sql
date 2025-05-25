-- Enhanced Sample Data for BUP CSE Department Scheduling System
-- Updated to meet exact user requirements:
-- 4 batches: BCSE22, BCSE23, BCSE24, BCSE25
-- Course distribution as specified
-- 5 rooms: CR302, CR303, CR304, CR504, LAB1003
-- Time slots: 8:30-5:00 PM with lunch break 1:30-2:00 PM

-- Clear existing data
DELETE FROM schedule;
DELETE FROM course_sections;
DELETE FROM courses;
DELETE FROM time_slots;
DELETE FROM classrooms;
DELETE FROM teachers;
DELETE FROM batches;

-- Insert Batches (4 batches as specified)
INSERT INTO batches (batch_code, batch_name, year_level, semester, total_sections, status) VALUES
('BCSE25', 'Bachelor of CSE 2025 (1st Year)', 1, 1, 2, 'ACTIVE'),  -- 6 Theory, 3 Lab
('BCSE24', 'Bachelor of CSE 2024 (2nd Year)', 2, 1, 2, 'ACTIVE'),  -- 5 Theory, 4 Lab
('BCSE23', 'Bachelor of CSE 2023 (3rd Year)', 3, 1, 2, 'ACTIVE'),  -- 5 Theory, 4 Lab
('BCSE22', 'Bachelor of CSE 2022 (4th Year)', 4, 1, 2, 'ACTIVE');  -- 5 Theory, 5 Lab

-- Insert Faculty Members (Internal + External)
INSERT INTO teachers (teacher_code, full_name, designation, department, email, phone, availability_start, availability_end, external_faculty, max_hours_per_day, max_hours_per_week) VALUES
-- Internal Faculty (4 members)
('FAC001', 'Dr. Abu Sayed Md. Latiful Hoque', 'Professor & Head', 'CSE', 'asayed@bup.edu.bd', '01712345678', '08:30:00', '17:00:00', 0, 8, 30),
('FAC002', 'Dr. Md. Saiful Islam', 'Associate Professor', 'CSE', 'saiful@bup.edu.bd', '01712345679', '08:30:00', '17:00:00', 0, 8, 30),
('FAC003', 'Mr. Tanvir Ahmed Rahman', 'Assistant Professor', 'CSE', 'tanvir@bup.edu.bd', '01712345680', '08:30:00', '17:00:00', 0, 8, 30),
('FAC004', 'Ms. Farhana Khandoker', 'Lecturer', 'CSE', 'farhana@bup.edu.bd', '01712345681', '08:30:00', '17:00:00', 0, 8, 30),

-- External Faculty (6 members with limited availability)
('EXT001', 'Prof. Mahmudur Rahman', 'Professor', 'EEE, DUET', 'mahmud@duet.ac.bd', '01308496660', '10:00:00', '14:00:00', 1, 4, 16),
('EXT002', 'Prof. Shahed Rana', 'Professor', 'Chemistry, JU', 'srana@ju.edu.bd', '01720500701', '12:00:00', '16:00:00', 1, 4, 16),
('EXT003', 'Col. Eare Morshed', 'Colonel', 'Mathematics, MIST', 'morshed@mist.ac.bd', '01769024124', '09:00:00', '13:00:00', 1, 4, 16),
('EXT004', 'Prof. Ziaul Ahsan', 'Professor', 'Physics', 'ziaul@gmail.com', '01769760880', '14:00:00', '17:00:00', 1, 4, 16),
('EXT005', 'Assoc. Prof. Md. Abdus Sattar', 'Associate Professor', 'CSE, MIST', 'sattar@mist.ac.bd', '01713036113', '11:00:00', '15:00:00', 1, 4, 16),
('EXT006', 'Dr. Rashida Begum', 'Professor', 'English, DU', 'rashida@du.ac.bd', '01777888999', '13:00:00', '17:00:00', 1, 4, 16);

-- Insert Classrooms (5 rooms as specified)
INSERT INTO classrooms (room_code, capacity, room_type, building, floor_number, facilities, status) VALUES
('CR302', 45, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
('CR303', 40, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
('CR304', 50, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
('CR504', 35, 'LAB', 'FBS Building', 5, 'Computers(35), Projector, AC', 'AVAILABLE'),
('CR1003', 30, 'LAB', 'Gen Belal Tower', 10, 'Computers(30), Projector, AC', 'AVAILABLE');

-- Insert Time Slots (Sunday to Thursday, 8:30 AM - 5:00 PM with lunch break)
INSERT INTO time_slots (slot_name, day_of_week, start_time, end_time, duration_minutes, slot_type, is_available, priority) VALUES
-- Sunday
('SUN_S1', 'SUN', '08:30:00', '10:00:00', 90, 'REGULAR', 1, 5),
('SUN_S2', 'SUN', '10:05:00', '11:35:00', 90, 'REGULAR', 1, 4),
('SUN_S3', 'SUN', '11:40:00', '13:10:00', 90, 'REGULAR', 1, 3),
('SUN_LUNCH', 'SUN', '13:10:00', '14:00:00', 50, 'LUNCH', 0, 0),
('SUN_S4', 'SUN', '14:00:00', '15:30:00', 90, 'REGULAR', 1, 2),
('SUN_S5', 'SUN', '15:35:00', '17:05:00', 90, 'REGULAR', 1, 1),
-- Lab slots (3 hours)
('SUN_L1', 'SUN', '08:30:00', '11:30:00', 180, 'REGULAR', 1, 3),
('SUN_L2', 'SUN', '14:00:00', '17:00:00', 180, 'REGULAR', 1, 2),

-- Monday
('MON_S1', 'MON', '08:30:00', '10:00:00', 90, 'REGULAR', 1, 5),
('MON_S2', 'MON', '10:05:00', '11:35:00', 90, 'REGULAR', 1, 4),
('MON_S3', 'MON', '11:40:00', '13:10:00', 90, 'REGULAR', 1, 3),
('MON_LUNCH', 'MON', '13:10:00', '14:00:00', 50, 'LUNCH', 0, 0),
('MON_S4', 'MON', '14:00:00', '15:30:00', 90, 'REGULAR', 1, 2),
('MON_S5', 'MON', '15:35:00', '17:05:00', 90, 'REGULAR', 1, 1),
('MON_L1', 'MON', '08:30:00', '11:30:00', 180, 'REGULAR', 1, 3),
('MON_L2', 'MON', '14:00:00', '17:00:00', 180, 'REGULAR', 1, 2),

-- Tuesday
('TUE_S1', 'TUE', '08:30:00', '10:00:00', 90, 'REGULAR', 1, 5),
('TUE_S2', 'TUE', '10:05:00', '11:35:00', 90, 'REGULAR', 1, 4),
('TUE_S3', 'TUE', '11:40:00', '13:10:00', 90, 'REGULAR', 1, 3),
('TUE_LUNCH', 'TUE', '13:10:00', '14:00:00', 50, 'LUNCH', 0, 0),
('TUE_S4', 'TUE', '14:00:00', '15:30:00', 90, 'REGULAR', 1, 2),
('TUE_S5', 'TUE', '15:35:00', '17:05:00', 90, 'REGULAR', 1, 1),
('TUE_L1', 'TUE', '08:30:00', '11:30:00', 180, 'REGULAR', 1, 3),
('TUE_L2', 'TUE', '14:00:00', '17:00:00', 180, 'REGULAR', 1, 2),

-- Wednesday
('WED_S1', 'WED', '08:30:00', '10:00:00', 90, 'REGULAR', 1, 5),
('WED_S2', 'WED', '10:05:00', '11:35:00', 90, 'REGULAR', 1, 4),
('WED_S3', 'WED', '11:40:00', '13:10:00', 90, 'REGULAR', 1, 3),
('WED_LUNCH', 'WED', '13:10:00', '14:00:00', 50, 'LUNCH', 0, 0),
('WED_S4', 'WED', '14:00:00', '15:30:00', 90, 'REGULAR', 1, 2),
('WED_S5', 'WED', '15:35:00', '17:05:00', 90, 'REGULAR', 1, 1),
('WED_L1', 'WED', '08:30:00', '11:30:00', 180, 'REGULAR', 1, 3),
('WED_L2', 'WED', '14:00:00', '17:00:00', 180, 'REGULAR', 1, 2),

-- Thursday
('THU_S1', 'THU', '08:30:00', '10:00:00', 90, 'REGULAR', 1, 5),
('THU_S2', 'THU', '10:05:00', '11:35:00', 90, 'REGULAR', 1, 4),
('THU_S3', 'THU', '11:40:00', '13:10:00', 90, 'REGULAR', 1, 3),
('THU_LUNCH', 'THU', '13:10:00', '14:00:00', 50, 'LUNCH', 0, 0),
('THU_S4', 'THU', '14:00:00', '15:30:00', 90, 'REGULAR', 1, 2),
('THU_S5', 'THU', '15:35:00', '17:05:00', 90, 'REGULAR', 1, 1),
('THU_L1', 'THU', '08:30:00', '11:30:00', 180, 'REGULAR', 1, 3),
('THU_L2', 'THU', '14:00:00', '17:00:00', 180, 'REGULAR', 1, 2);

-- Insert Courses for BCSE25 (6 Theory, 3 Lab)
INSERT INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, department, status) VALUES
-- BCSE25 Theory Courses (6 courses)
('ENG1101', 'Communicative English-I', 3.00, 'THEORY', 90, 2, 1, 6, 'CSE', 'ACTIVE'),
('CHEM1103', 'Fundamentals of Chemistry', 3.00, 'THEORY', 90, 2, 1, 2, 'CSE', 'ACTIVE'),
('ICE1105', 'Electrical Circuit Analysis', 3.00, 'THEORY', 90, 2, 1, 5, 'CSE', 'ACTIVE'),
('GED1119', 'Bangladesh Studies', 3.00, 'THEORY', 90, 2, 1, 6, 'CSE', 'ACTIVE'),
('MATH1109', 'Differential and Integral Calculus', 3.00, 'THEORY', 90, 2, 1, 3, 'CSE', 'ACTIVE'),
('PHY1115', 'Physics', 3.00, 'THEORY', 90, 2, 1, 4, 'CSE', 'ACTIVE'),
-- BCSE25 Lab Courses (3 courses)
('ICE1106', 'Electrical Circuit Analysis Lab', 1.50, 'LAB', 180, 1, 1, 5, 'CSE', 'ACTIVE'),
('PHY1116', 'Physics Laboratory', 1.50, 'LAB', 180, 1, 1, 4, 'CSE', 'ACTIVE'),
('CHEM1104', 'Chemistry Laboratory', 0.75, 'LAB', 180, 1, 1, 2, 'CSE', 'ACTIVE');

-- Insert Courses for BCSE24 (5 Theory, 4 Lab)  
INSERT INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, department, status) VALUES
-- BCSE24 Theory Courses (5 courses)
('ENG2110', 'Presentation Skill Development', 3.00, 'THEORY', 90, 2, 2, 6, 'CSE', 'ACTIVE'),
('MATH2111', 'Differential Equations & Transforms', 3.00, 'THEORY', 90, 2, 2, 3, 'CSE', 'ACTIVE'),
('CSE2201', 'Data Structures and Algorithms-I', 3.00, 'THEORY', 90, 2, 2, 1, 'CSE', 'ACTIVE'),
('CSE2203', 'Computer Architecture', 3.00, 'THEORY', 90, 2, 2, 1, 'CSE', 'ACTIVE'),
('CSE2207', 'Object Oriented Programming-II', 3.00, 'THEORY', 90, 2, 2, 2, 'CSE', 'ACTIVE'),
-- BCSE24 Lab Courses (4 courses)
('CSE2202', 'Engineering Drawing and CAD Lab', 1.50, 'LAB', 180, 1, 2, 3, 'CSE', 'ACTIVE'),
('CSE2204', 'Data Structures and Algorithms-I Lab', 1.50, 'LAB', 180, 1, 2, 1, 'CSE', 'ACTIVE'),
('CSE2208', 'Object Oriented Programming-II Lab', 1.50, 'LAB', 180, 1, 2, 2, 'CSE', 'ACTIVE'),
('ICE2209', 'Digital Electronics Lab', 0.75, 'LAB', 180, 1, 2, 5, 'CSE', 'ACTIVE');

-- Insert Courses for BCSE23 (5 Theory, 4 Lab)
INSERT INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, department, status) VALUES
-- BCSE23 Theory Courses (5 courses)
('CSE3301', 'Database Systems', 3.00, 'THEORY', 90, 2, 3, 1, 'CSE', 'ACTIVE'),
('CSE3303', 'Computer Networks', 3.00, 'THEORY', 90, 2, 3, 2, 'CSE', 'ACTIVE'),
('CSE3305', 'Software Engineering', 3.00, 'THEORY', 90, 2, 3, 1, 'CSE', 'ACTIVE'),
('CSE3307', 'Operating Systems', 3.00, 'THEORY', 90, 2, 3, 2, 'CSE', 'ACTIVE'),
('MATH3311', 'Linear Algebra and Statistics', 3.00, 'THEORY', 90, 2, 3, 3, 'CSE', 'ACTIVE'),
-- BCSE23 Lab Courses (4 courses)
('CSE3302', 'Database Systems Lab', 1.50, 'LAB', 180, 1, 3, 1, 'CSE', 'ACTIVE'),
('CSE3304', 'Computer Networks Lab', 1.50, 'LAB', 180, 1, 3, 2, 'CSE', 'ACTIVE'),
('CSE3306', 'Software Engineering Lab', 1.50, 'LAB', 180, 1, 3, 1, 'CSE', 'ACTIVE'),
('CSE3308', 'Operating Systems Lab', 0.75, 'LAB', 180, 1, 3, 2, 'CSE', 'ACTIVE');

-- Insert Courses for BCSE22 (5 Theory, 5 Lab)
INSERT INTO courses (course_code, course_title, credit_hours, class_type, session_duration, sessions_per_week, batch_id, teacher_id, department, status) VALUES
-- BCSE22 Theory Courses (5 courses)
('CSE4401', 'Machine Learning', 3.00, 'THEORY', 90, 2, 4, 1, 'CSE', 'ACTIVE'),
('CSE4403', 'Artificial Intelligence', 3.00, 'THEORY', 90, 2, 4, 2, 'CSE', 'ACTIVE'),
('CSE4405', 'Computer Graphics', 3.00, 'THEORY', 90, 2, 4, 3, 'CSE', 'ACTIVE'),
('CSE4407', 'Information Security', 3.00, 'THEORY', 90, 2, 4, 1, 'CSE', 'ACTIVE'),
('CSE4409', 'Project Management', 3.00, 'THEORY', 90, 2, 4, 4, 'CSE', 'ACTIVE'),
-- BCSE22 Lab Courses (5 courses)
('CSE4402', 'Machine Learning Lab', 1.50, 'LAB', 180, 1, 4, 1, 'CSE', 'ACTIVE'),
('CSE4404', 'Artificial Intelligence Lab', 1.50, 'LAB', 180, 1, 4, 2, 'CSE', 'ACTIVE'),
('CSE4406', 'Computer Graphics Lab', 1.50, 'LAB', 180, 1, 4, 3, 'CSE', 'ACTIVE'),
('CSE4408', 'Information Security Lab', 1.50, 'LAB', 180, 1, 4, 1, 'CSE', 'ACTIVE'),
('CSE4410', 'Capstone Project', 0.75, 'LAB', 180, 1, 4, 4, 'CSE', 'ACTIVE');

-- Insert Course Sections (A and B for each course)
INSERT INTO course_sections (course_id, section_name, max_students, enrolled_students, status)
SELECT course_id, 'A', 40, 35, 'ACTIVE' FROM courses
UNION ALL
SELECT course_id, 'B', 40, 35, 'ACTIVE' FROM courses;

-- Sample faculty preferences (can be extended)
INSERT INTO teacher_constraints (teacher_id, day_of_week, unavailable_start_time, unavailable_end_time, constraint_type, reason) VALUES
-- External faculty have limited availability
(5, 'SUN', '08:30:00', '09:59:00', 'UNAVAILABLE', 'External faculty - late arrival'),
(5, 'MON', '15:31:00', '17:05:00', 'UNAVAILABLE', 'External faculty - early departure'),
(6, 'WED', '08:30:00', '11:59:00', 'UNAVAILABLE', 'External faculty - other commitments'),
(7, 'THU', '14:01:00', '17:05:00', 'UNAVAILABLE', 'External faculty - other commitments');
