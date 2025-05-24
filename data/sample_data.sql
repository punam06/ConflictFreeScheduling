-- Sample data for Conflict-Free Scheduling System
-- This file populates the database with realistic CSE department data

-- Insert courses
INSERT OR REPLACE INTO courses (course_code, course_name, instructor, duration, priority, capacity, room_requirement, department, semester) VALUES
('CSE101', 'Introduction to Programming', 'Dr. Smith', 3, 1, 45, 'Lab', 'CSE', 1),
('CSE102', 'Discrete Mathematics', 'Prof. Johnson', 3, 2, 40, 'Regular', 'CSE', 1),
('CSE103', 'Computer Fundamentals', 'Dr. Wilson', 2, 3, 50, 'Regular', 'CSE', 1),
('CSE201', 'Data Structures', 'Dr. Wilson', 3, 1, 35, 'Lab', 'CSE', 3),
('CSE202', 'Computer Organization', 'Prof. Brown', 3, 2, 30, 'Regular', 'CSE', 3),
('CSE203', 'Object Oriented Programming', 'Dr. Garcia', 3, 1, 40, 'Lab', 'CSE', 3),
('CSE301', 'Algorithms', 'Dr. Davis', 3, 1, 35, 'Regular', 'CSE', 5),
('CSE302', 'Database Systems', 'Prof. Miller', 3, 2, 30, 'Lab', 'CSE', 5),
('CSE303', 'Software Engineering', 'Dr. Garcia', 3, 1, 25, 'Regular', 'CSE', 5),
('CSE304', 'Computer Networks', 'Prof. Martinez', 3, 2, 25, 'Lab', 'CSE', 5),
('CSE401', 'Operating Systems', 'Dr. Anderson', 3, 1, 30, 'Regular', 'CSE', 7),
('CSE402', 'Compiler Design', 'Prof. Taylor', 3, 2, 20, 'Regular', 'CSE', 7),
('CSE403', 'Machine Learning', 'Prof. Taylor', 3, 3, 20, 'Lab', 'CSE', 7),
('CSE404', 'Artificial Intelligence', 'Dr. Thomas', 3, 2, 25, 'Regular', 'CSE', 7),
('CSE405', 'Computer Graphics', 'Prof. Jackson', 3, 3, 20, 'Lab', 'CSE', 7),
('CSE450', 'Senior Project I', 'Dr. White', 3, 1, 15, 'Regular', 'CSE', 7),
('CSE451', 'Senior Project II', 'Prof. Harris', 3, 1, 15, 'Regular', 'CSE', 8),
('CSE499', 'Special Topics', 'Dr. Clark', 3, 3, 10, 'Regular', 'CSE', 8);

-- Insert rooms
INSERT OR REPLACE INTO rooms (room_code, room_name, capacity, room_type, equipment, building, floor) VALUES
('R101', 'Computer Lab 1', 45, 'Lab', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R102', 'Computer Lab 2', 40, 'Lab', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R103', 'Computer Lab 3', 35, 'Lab', 'Computers, Projector, Whiteboard', 'Main Building', 1),
('R104', 'Advanced Lab', 25, 'Lab', 'High-end Computers, Servers, Projector', 'Main Building', 1),
('R201', 'Lecture Hall A', 50, 'Regular', 'Projector, Whiteboard, Audio System', 'Main Building', 2),
('R202', 'Lecture Hall B', 45, 'Regular', 'Projector, Whiteboard, Audio System', 'Main Building', 2),
('R203', 'Lecture Hall C', 40, 'Regular', 'Projector, Whiteboard', 'Main Building', 2),
('R204', 'Large Auditorium', 100, 'Regular', 'Projector, Audio System, Stage', 'Main Building', 2),
('R301', 'Seminar Room 1', 30, 'Regular', 'Projector, Whiteboard', 'Main Building', 3),
('R302', 'Seminar Room 2', 25, 'Regular', 'Projector, Whiteboard', 'Main Building', 3),
('R303', 'Conference Room', 20, 'Regular', 'Projector, Round Table', 'Main Building', 3),
('R401', 'Research Lab', 15, 'Lab', 'High-end Computers, Servers', 'Research Building', 4);

-- Insert time slots (Monday to Friday, 5 slots per day)
INSERT OR REPLACE INTO time_slots (day_of_week, start_time, end_time, slot_type) VALUES
-- Monday
(1, '08:00:00', '09:30:00', 'Morning'),
(1, '09:45:00', '11:15:00', 'Morning'),
(1, '11:30:00', '13:00:00', 'Late Morning'),
(1, '14:00:00', '15:30:00', 'Afternoon'),
(1, '15:45:00', '17:15:00', 'Afternoon'),
-- Tuesday
(2, '08:00:00', '09:30:00', 'Morning'),
(2, '09:45:00', '11:15:00', 'Morning'),
(2, '11:30:00', '13:00:00', 'Late Morning'),
(2, '14:00:00', '15:30:00', 'Afternoon'),
(2, '15:45:00', '17:15:00', 'Afternoon'),
-- Wednesday
(3, '08:00:00', '09:30:00', 'Morning'),
(3, '09:45:00', '11:15:00', 'Morning'),
(3, '11:30:00', '13:00:00', 'Late Morning'),
(3, '14:00:00', '15:30:00', 'Afternoon'),
(3, '15:45:00', '17:15:00', 'Afternoon'),
-- Thursday
(4, '08:00:00', '09:30:00', 'Morning'),
(4, '09:45:00', '11:15:00', 'Morning'),
(4, '11:30:00', '13:00:00', 'Late Morning'),
(4, '14:00:00', '15:30:00', 'Afternoon'),
(4, '15:45:00', '17:15:00', 'Afternoon'),
-- Friday
(5, '08:00:00', '09:30:00', 'Morning'),
(5, '09:45:00', '11:15:00', 'Morning'),
(5, '11:30:00', '13:00:00', 'Late Morning'),
(5, '14:00:00', '15:30:00', 'Afternoon'),
(5, '15:45:00', '17:15:00', 'Afternoon');

-- Insert some sample scheduling preferences
INSERT OR REPLACE INTO scheduling_preferences (course_id, preferred_slot_id, preference_type, priority, notes) VALUES
(1, 1, 'preferred', 1, 'Programming courses work better in morning slots'),
(4, 6, 'preferred', 1, 'Data structures needs consistent timing'),
(7, 11, 'required', 1, 'Algorithms course requires focused attention'),
(13, 16, 'preferred', 2, 'ML course benefits from afternoon lab time');

-- Insert some sample conflicts for testing
INSERT OR REPLACE INTO conflicts_log (conflict_type, description, course_id_1, course_id_2, resolved) VALUES
('ROOM_CAPACITY', 'Course capacity exceeds room capacity', 1, NULL, 1),
('TIME_CONFLICT', 'Two courses scheduled at same time in same room', 2, 3, 0),
('INSTRUCTOR_CONFLICT', 'Same instructor assigned to overlapping time slots', 4, 5, 1);
