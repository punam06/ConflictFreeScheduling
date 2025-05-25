-- Reset classrooms table
DELETE FROM classrooms WHERE room_code IN ('CR302', 'CR303', 'CR304', 'LAB504', 'LAB505');

-- Insert updated classroom configurations
INSERT OR REPLACE INTO classrooms (room_code, capacity, room_type, building, floor_number, facilities, status) VALUES
-- Theory Classrooms (3)
('CR302', 45, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC, Sound System', 'AVAILABLE'),
('CR303', 40, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
('CR304', 50, 'THEORY', 'FBS Building', 3, 'Projector, Whiteboard, AC', 'AVAILABLE'),
-- Lab Rooms (2)
('LAB504', 30, 'LAB', 'FBS Building', 5, 'Computers(30), Projector, AC, Programming Software', 'AVAILABLE'),
('LAB505', 35, 'LAB', 'FBS Building', 5, 'Computers(35), Projector, AC, Programming Software', 'AVAILABLE');
