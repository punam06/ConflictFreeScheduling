-- Minimal sample data for testing the database functionality
-- Insert a basic batch
INSERT OR IGNORE INTO batches (batch_id, batch_code, batch_name, year_level, semester) 
VALUES (1, 'CSE23A', 'CSE 2023 Batch A', 2, 2);

-- Insert a basic teacher  
INSERT OR IGNORE INTO teachers (teacher_id, teacher_code, full_name, designation, department, email) 
VALUES (1, 'T001', 'Dr. Sample Teacher', 'Associate Professor', 'CSE', 'teacher@bup.edu.bd');

-- Insert a basic classroom
INSERT OR IGNORE INTO classrooms (room_id, room_code, capacity, room_type, building, floor_number) 
VALUES (1, 'ENG101', 50, 'THEORY', 'Engineering Building', 1);

-- Insert basic time slots
INSERT OR IGNORE INTO time_slots (slot_id, slot_name, day_of_week, start_time, end_time, duration_minutes) 
VALUES 
(1, 'Period 1', 'MON', '08:30:00', '10:00:00', 90),
(2, 'Period 2', 'MON', '10:00:00', '11:30:00', 90),
(3, 'Period 3', 'MON', '11:30:00', '13:00:00', 90);
