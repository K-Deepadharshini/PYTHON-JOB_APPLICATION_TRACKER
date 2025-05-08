-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

-- Create the 'companies' table
CREATE TABLE IF NOT EXISTS companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    company_location VARCHAR(255),
    company_email VARCHAR(255),
    company_pno VARCHAR(20)
);

-- Create the 'statuses' table
CREATE TABLE IF NOT EXISTS statuses (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(100) NOT NULL
);

-- Insert initial status values
INSERT INTO statuses (status_name) VALUES
('Applied'),
('Offer Received'),
('Awaiting Response'), 
('Interview Scheduled'), 
('Rejected'), 
('Hired')
ON DUPLICATE KEY UPDATE status_name = VALUES(status_name);

-- Create the 'applications' table
CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    job_position VARCHAR(255),
    application_date DATE,
    job_description TEXT,
    status_id INT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (status_id) REFERENCES statuses(status_id)
);

-- Create the 'interviews' table
CREATE TABLE IF NOT EXISTS interviews (
    interview_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT,
    interview_date DATE,
    interview_time VARCHAR(20),
    interview_location VARCHAR(255),
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);


