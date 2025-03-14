-- Create schemas for each service
CREATE SCHEMA IF NOT EXISTS user_schema;
CREATE SCHEMA IF NOT EXISTS rider_schema;
CREATE SCHEMA IF NOT EXISTS booking_schema;

-- Users table
CREATE TABLE IF NOT EXISTS user_schema.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Riders table
CREATE TABLE IF NOT EXISTS rider_schema.riders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    license_plate VARCHAR(20) NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 5.0,
    status VARCHAR(20) DEFAULT 'Available' CHECK (status IN ('Available', 'Busy')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Distance matrix for user-rider combinations
CREATE TABLE IF NOT EXISTS rider_schema.distance_matrix (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    rider_id INT NOT NULL,
    distance_km DECIMAL(5, 2) NOT NULL,
    UNIQUE (user_id, rider_id)
);

-- Rides table
CREATE TABLE IF NOT EXISTS booking_schema.rides (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    rider_id INT NOT NULL,
    pickup_location VARCHAR(255) NOT NULL,
    dropoff_location VARCHAR(255) NOT NULL,
    distance_km DECIMAL(5, 2) NOT NULL,
    fare_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed', 'Canceled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Populate distance matrix with dummy data (5 users, 5 riders)
INSERT INTO rider_schema.distance_matrix (user_id, rider_id, distance_km) VALUES
-- User 1 distances
(1, 1, 8.0),
(1, 2, 5.0),
(1, 3, 6.0),
(1, 4, 2.0),
(1, 5, 7.0),
-- User 2 distances
(2, 1, 3.0),
(2, 2, 9.0),
(2, 3, 4.0),
(2, 4, 6.0),
(2, 5, 1.0),
-- User 3 distances
(3, 1, 5.0),
(3, 2, 2.0),
(3, 3, 8.0),
(3, 4, 7.0),
(3, 5, 4.0),
-- User 4 distances
(4, 1, 6.0),
(4, 2, 10.0),
(4, 3, 3.0),
(4, 4, 1.0),
(4, 5, 9.0),
-- User 5 distances
(5, 1, 7.0),
(5, 2, 4.0),
(5, 3, 2.0),
(5, 4, 9.0),
(5, 5, 5.0)
ON CONFLICT (user_id, rider_id) DO NOTHING;