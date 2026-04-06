-- Hospital Management System Database Schema
-- Created: 2026-03-22

CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Doctor', 'Receptionist', 'Patient') NOT NULL DEFAULT 'Patient',
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- Patients Table
CREATE TABLE patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    blood_group VARCHAR(5),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    emergency_contact VARCHAR(15),
    emergency_contact_name VARCHAR(100),
    medical_history TEXT,
    allergies TEXT,
    current_medications TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id)
);

-- Doctors Table
CREATE TABLE doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    specialization VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    experience_years INT,
    qualification VARCHAR(200),
    clinic_address VARCHAR(255),
    consultation_fee DECIMAL(10, 2),
    available_from TIME,
    available_to TIME,
    consultation_duration INT DEFAULT 30,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_specialization (specialization),
    INDEX idx_user_id (user_id)
);

-- Appointments Table
CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show') DEFAULT 'Scheduled',
    reason_for_visit TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_appointment_date (appointment_date),
    INDEX idx_patient_id (patient_id),
    INDEX idx_doctor_id (doctor_id),
    INDEX idx_status (status),
    UNIQUE KEY unique_appointment (doctor_id, appointment_date, appointment_time)
);

-- Rooms/Wards Table
CREATE TABLE rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    room_type ENUM('General', 'Semi-Private', 'Private', 'ICU') NOT NULL,
    floor INT,
    capacity INT DEFAULT 1,
    occupied_beds INT DEFAULT 0,
    rate_per_day DECIMAL(10, 2),
    facilities TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_room_type (room_type),
    INDEX idx_is_available (is_available)
);

-- Lab Reports Table
CREATE TABLE lab_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT,
    test_name VARCHAR(150) NOT NULL,
    test_type VARCHAR(100),
    test_date DATE NOT NULL,
    result TEXT,
    status ENUM('Pending', 'Complete', 'Cancelled') DEFAULT 'Pending',
    normal_range VARCHAR(100),
    comments TEXT,
    cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL,
    INDEX idx_patient_id (patient_id),
    INDEX idx_test_date (test_date),
    INDEX idx_status (status)
);

-- Billing Table
CREATE TABLE billing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    appointment_id INT,
    billing_date DATE NOT NULL,
    consultation_fee DECIMAL(10, 2) DEFAULT 0,
    medicine_cost DECIMAL(10, 2) DEFAULT 0,
    test_cost DECIMAL(10, 2) DEFAULT 0,
    room_cost DECIMAL(10, 2) DEFAULT 0,
    other_charges DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) GENERATED ALWAYS AS (consultation_fee + medicine_cost + test_cost + room_cost + other_charges) STORED,
    discount DECIMAL(10, 2) DEFAULT 0,
    amount_paid DECIMAL(10, 2) DEFAULT 0,
    amount_due GENERATED ALWAYS AS (total_amount - discount - amount_paid) STORED,
    payment_status ENUM('Unpaid', 'Partial', 'Paid') DEFAULT 'Unpaid',
    payment_method VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL,
    INDEX idx_patient_id (patient_id),
    INDEX idx_billing_date (billing_date),
    INDEX idx_payment_status (payment_status)
);

-- Room Allocation Table (for tracking patient admissions)
CREATE TABLE room_allocations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    room_id INT NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    status ENUM('Active', 'Discharged', 'Cancelled') DEFAULT 'Active',
    reason_for_admission TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT,
    INDEX idx_patient_id (patient_id),
    INDEX idx_room_id (room_id),
    INDEX idx_status (status)
);

-- Medicines Table (optional, for tracking medicines prescribed)
CREATE TABLE medicines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(150) NOT NULL,
    description TEXT,
    dosage VARCHAR(50),
    unit_price DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_medicine_name (medicine_name)
);

-- Prescriptions Table
CREATE TABLE prescriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    prescription_date DATE NOT NULL,
    medicine_id INT,
    medicine_name VARCHAR(150),
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    duration INT,
    duration_unit ENUM('Days', 'Weeks', 'Months') DEFAULT 'Days',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE SET NULL,
    INDEX idx_appointment_id (appointment_id),
    INDEX idx_patient_id (patient_id)
);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Admin User
INSERT INTO users (username, email, password, role, full_name, phone, is_active) VALUES
('admin', 'admin@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Admin', 'Dr. Admin', '8800000001', TRUE);

-- Doctors
INSERT INTO users (username, email, password, role, full_name, phone, is_active) VALUES
('dr_sharma', 'sharma@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Doctor', 'Dr. Rajesh Sharma', '9001234567', TRUE),
('dr_patel', 'patel@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Doctor', 'Dr. Priya Patel', '9001234568', TRUE),
('dr_gupta', 'gupta@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Doctor', 'Dr. Amit Gupta', '9001234569', TRUE);

-- Doctor Details
INSERT INTO doctors (user_id, specialization, license_number, experience_years, qualification, consultation_fee, available_from, available_to, is_available) VALUES
(2, 'Cardiology', 'LIC001', 15, 'MBBS, MD (Cardiology), DM (Cardiothoracic Surgery)', 800.00, '09:00:00', '17:00:00', TRUE),
(3, 'Orthopedics', 'LIC002', 12, 'MBBS, MS (Orthopedics)', 600.00, '10:00:00', '18:00:00', TRUE),
(4, 'General Medicine', 'LIC003', 8, 'MBBS, MD (Internal Medicine)', 500.00, '08:00:00', '16:00:00', TRUE);

-- Receptionist
INSERT INTO users (username, email, password, role, full_name, phone, is_active) VALUES
('receptionist', 'receptionist@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Receptionist', 'Priya Receptionist', '9001234570', TRUE);

-- Patients
INSERT INTO users (username, email, password, role, full_name, phone, is_active) VALUES
('patient1', 'patient1@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Patient', 'John Doe', '9999000001', TRUE),
('patient2', 'patient2@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Patient', 'Jane Smith', '9999000002', TRUE),
('patient3', 'patient3@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUFUfRVm', 'Patient', 'Robert Johnson', '9999000003', TRUE);

-- Patient Details
INSERT INTO patients (user_id, date_of_birth, gender, blood_group, address, city, state, zip_code, emergency_contact, emergency_contact_name, medical_history, allergies, current_medications) VALUES
(6, '1990-05-15', 'Male', 'O+', '123 Main Street', 'Mumbai', 'Maharashtra', '400001', '9999000011', 'Mary Doe', 'Diabetes, Hypertension', 'Penicillin', 'Metformin'),
(7, '1995-08-22', 'Female', 'B+', '456 Park Avenue', 'Delhi', 'Delhi', '110001', '9999000012', 'Sarah Smith', 'Asthma', 'Aspirin', 'Albuterol'),
(8, '1988-03-10', 'Male', 'AB-', '789 Oak Avenue', 'Bangalore', 'Karnataka', '560001', '9999000013', 'Michael Johnson', 'None', 'None', 'None');

-- Rooms
INSERT INTO rooms (room_number, room_type, floor, capacity, rate_per_day, facilities, is_available) VALUES
('101', 'General', 1, 3, 500.00, 'Fan, Bed, Basic Furniture', TRUE),
('102', 'General', 1, 3, 500.00, 'Fan, Bed, Basic Furniture', TRUE),
('201', 'Semi-Private', 2, 2, 1200.00, 'A/C, TV, Attached Bath', TRUE),
('202', 'Semi-Private', 2, 2, 1200.00, 'A/C, TV, Attached Bath', TRUE),
('301', 'Private', 3, 1, 2500.00, 'A/C, TV, WiFi, Attached Bath, Sofa', TRUE),
('401', 'ICU', 4, 1, 5000.00, 'Advanced Equipment, Monitor, Nurse Call', TRUE);

-- Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason_for_visit) VALUES
(1, 2, '2026-03-25', '10:30:00', 'Scheduled', 'Routine Check-up'),
(2, 3, '2026-03-26', '14:00:00', 'Scheduled', 'Knee Pain'),
(3, 4, '2026-03-27', '09:00:00', 'Scheduled', 'General Checkup');

-- Lab Reports
INSERT INTO lab_reports (patient_id, doctor_id, test_name, test_type, test_date, status, normal_range, cost) VALUES
(1, 2, 'Blood Glucose', 'Blood Test', '2026-03-20', 'Complete', '70-100 mg/dl', 300.00),
(2, 3, 'X-Ray Knee', 'Imaging', '2026-03-21', 'Complete', 'Normal', 500.00),
(3, 4, 'Complete Blood Count', 'Blood Test', '2026-03-22', 'Pending', '-', 400.00);

-- Billing
INSERT INTO billing (patient_id, appointment_id, billing_date, consultation_fee, medicine_cost, test_cost, payment_status, payment_method) VALUES
(1, 1, '2026-03-20', 800.00, 200.00, 300.00, 'Paid', 'Cash'),
(2, 2, '2026-03-21', 600.00, 150.00, 500.00, 'Paid', 'Card'),
(3, 3, '2026-03-22', 500.00, 100.00, 400.00, 'Unpaid', NULL);

-- Sample Medicines
INSERT INTO medicines (medicine_name, description, dosage, unit_price, stock_quantity) VALUES
('Aspirin', 'Pain reliever and anti-inflammatory', '500mg', 5.00, 100),
('Metformin', 'For Type 2 Diabetes', '500mg', 15.00, 200),
('Albuterol', 'Asthma rescue inhaler', '100mcg', 150.00, 50);
