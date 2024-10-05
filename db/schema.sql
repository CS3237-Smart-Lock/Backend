-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    face_image BLOB
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

-- Seed data for Users table
INSERT INTO Users (name, description, face_image) VALUES 
    ('Alice Smith', 'Admin of the smart lock system', NULL), -- face_image can be set later as BLOB data
    ('Bob Johnson', 'Regular user with access to the main door', NULL),
    ('Charlie Brown', 'Guest user for limited access', NULL);

-- Seed data for Attempts table
INSERT INTO Attempts (timestamp, recognized_user, status, details) VALUES 
    ('2024-10-01 08:30:00', 1, 'success', 'Admin accessed the front door'),
    ('2024-10-01 09:00:00', 2, 'success', 'Bob entered the main entrance'),
    ('2024-10-01 12:45:00', 3, 'failure', 'Unsuccessful attempt by guest user'),
    ('2024-10-02 07:15:00', 2, 'failure', 'Bob attempted access outside of allowed hours'),
    ('2024-10-02 18:20:00', 1, 'success', 'Admin accessed the back door'),
    ('2024-10-02 20:00:00', NULL, 'failure', 'Unrecognized face detected');
