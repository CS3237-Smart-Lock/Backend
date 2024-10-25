-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    face_image BLOB, -- the image that the user uploaded, with face circled
    embedding TEXT-- an image embedding of the face, store as text separated by comma
);

-- Create Attempts Table
CREATE TABLE IF NOT EXISTS Attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recognized_user INTEGER, -- user id
    status TEXT NOT NULL CHECK (status IN ('success', 'failure')), -- Enforcing ENUM-like behavior
    details TEXT,
    FOREIGN KEY (recognized_user) REFERENCES Users(id)
);
--
-- -- Seed data for Users table
-- INSERT INTO Users (name, description, face_image) VALUES 
--     ('Alice Smith', 'Admin of the smart lock system', NULL), -- face_image can be set later as BLOB data
--     ('Bob Johnson', 'Regular user with access to the main door', NULL),
--     ('Charlie Brown', 'Guest user for limited access', NULL);
--
-- Seed data for Attempts table
INSERT INTO Attempts (timestamp, recognized_user, status, details) VALUES 
    ('2024-10-02 20:30:00', 4, 'success', 'Alice accessed the main entrance'),
    ('2024-10-03 08:10:00', 2, 'success', 'Bob accessed the garage'),
    ('2024-10-03 09:30:00', NULL, 'failure', 'Unrecognized attempt at front door'),
    ('2024-10-03 12:45:00', 3, 'success', 'Charlie entered the building'),
    ('2024-10-03 14:50:00', NULL, 'failure', 'Unknown face detected at back door'),
    ('2024-10-03 17:30:00', 5, 'success', 'David accessed the garage'),
    ('2024-10-04 06:15:00', NULL, 'failure', 'Unrecognized attempt during night hours'),
    ('2024-10-04 07:45:00', 4, 'success', 'Alice entered via the side entrance'),
    ('2024-10-04 09:00:00', 2, 'failure', 'Bob denied access due to incorrect credentials'),
    ('2024-10-04 10:15:00', 1, 'success', 'Admin accessed the control room'),
    ('2024-10-04 12:30:00', NULL, 'failure', 'Unrecognized face tried accessing the server room'),
    ('2024-10-04 15:10:00', 3, 'success', 'Charlie accessed the back door'),
    ('2024-10-05 08:00:00', NULL, 'failure', 'Unknown person detected at the gate'),
    ('2024-10-05 10:00:00', 4, 'success', 'Alice accessed the main entrance'),
    ('2024-10-05 13:45:00', NULL, 'failure', 'Unsuccessful attempt by guest at the side door'),
    ('2024-10-05 18:30:00', 1, 'success', 'Admin entered the garage'),
    ('2024-10-05 19:00:00', 5, 'success', 'David accessed the warehouse'),
    ('2024-10-06 08:25:00', NULL, 'failure', 'Unrecognized face at front gate'),
    ('2024-10-06 10:50:00', 2, 'success', 'Bob accessed the garage'),
    ('2024-10-06 13:30:00', 4, 'failure', 'Alice denied access outside of authorized hours'),
    ('2024-10-06 15:40:00', 3, 'success', 'Charlie accessed the main entrance'),
    ('2024-10-06 17:15:00', NULL, 'failure', 'Unrecognized person attempted access at night'),
    ('2024-10-07 07:30:00', 5, 'success', 'David accessed the side entrance'),
    ('2024-10-07 10:15:00', 1, 'success', 'Admin entered the control room'),
    ('2024-10-07 13:05:00', NULL, 'failure', 'Guest failed to access front door'),
    ('2024-10-07 16:50:00', 2, 'success', 'Bob accessed the back entrance'),
    ('2024-10-08 07:00:00', 3, 'failure', 'Charlie failed to access during restricted hours'),
    ('2024-10-08 09:45:00', 4, 'success', 'Alice accessed the main entrance'),
    ('2024-10-08 11:30:00', NULL, 'failure', 'Unrecognized face detected near loading dock'),
    ('2024-10-08 15:20:00', 5, 'success', 'David accessed the main entrance'),
    ('2024-10-08 18:00:00', NULL, 'failure', 'Unauthorized access attempt at night'),
    ('2024-10-09 07:45:00', 1, 'success', 'Admin accessed the control room'),
    ('2024-10-09 10:15:00', 4, 'success', 'Alice entered through side door'),
    ('2024-10-09 13:30:00', 3, 'success', 'Charlie accessed the back door'),
    ('2024-10-09 17:00:00', 2, 'failure', 'Bob attempted unauthorized access after hours'),
    ('2024-10-10 07:10:00', NULL, 'failure', 'Unrecognized face detected at back gate'),
    ('2024-10-10 09:30:00', 5, 'success', 'David accessed the garage'),
    ('2024-10-10 12:00:00', 1, 'success', 'Admin accessed the server room'),
    ('2024-10-10 15:15:00', NULL, 'failure', 'Unknown person tried accessing the facility');
