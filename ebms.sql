-- Create Database
CREATE DATABASE electricity_billing_system;

-- Use the newly created database
USE electricity_billing_system;

-- 1. Create the Customer Table
CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    dob DATE,
    email_id VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    contact_details VARCHAR(15),
    address VARCHAR(255)
);

DROP TABLE electricity_billing_system.customer;

SELECT * FROM electricity_billing_system.customer;
SELECT * FROM electricity_billing_system.bill_calculation;
-- 2. Create the Billing Table
CREATE TABLE bill_calculation (
    customer_id INT NOT NULL,  -- Ensure it matches the type in the 'customer' table
    previous_meter_reading DECIMAL(10, 2) NOT NULL,
    current_meter_reading DECIMAL(10, 2) NOT NULL,
    tariff_rate DECIMAL(10, 2) NOT NULL,
    payment_due_date DATE NOT NULL,
    is_late BOOLEAN NOT NULL DEFAULT 0,  -- Added is_late column
    bill_amount DECIMAL(10, 2) AS ((current_meter_reading - previous_meter_reading) * tariff_rate) STORED, -- Automatically calculated
    final_bill DECIMAL(10, 2),  -- To store the total amount after applying late fees
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically stores creation time
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)  -- Foreign key referencing 'customer' table
);

ALTER TABLE bill_calculation
ADD COLUMN bill_id INT AUTO_INCREMENT PRIMARY KEY FIRST;

SELECT * FROM electricity_billing_system.bill_calculation;

SELECT * FROM electricity_billing_system.bill_calculation;
DROP TABLE electricity_billing_system.bill_calculation;

-- 3. Create the Admin Table
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

SELECT * FROM electricity_billing_system.admin;
-- 4. Create the Service Provider Table
CREATE TABLE service_provider (
    reader_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255),
    contact_details VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

-- 5. Create the Transaction Table
CREATE TABLE transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    billing_id INT,
    payable DECIMAL(10, 2),
    payment_date DATE,
    status VARCHAR(10),  -- 'paid' or 'pending'
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (billing_id) REFERENCES billing(billing_id)
);

-- 6. Create the Feedback Table
CREATE TABLE feedback (
    customer_id INT,
    feedback TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

DROP TABLE electricity_billing_system.feedback;

-- 7. Create the Complaints Table
CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    admin_id INT,
    complaint TEXT,
    status VARCHAR(50),  -- status of complaint
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id)
);

-- 8. Create the Unit Table
CREATE TABLE unit (
    sr_no INT AUTO_INCREMENT PRIMARY KEY,
    unit_bracket VARCHAR(50),  -- '200units', '500units', '1000units'
    rate_per_unit DECIMAL(10, 2)
);

-- Insert Sample Data

-- Insert into customer
INSERT INTO customer (customer_name, dob, password, email_id, contact_details, address)
VALUES 
('Samruddhi Bagal', '2004-11-22', 'password123', 'sam.bagal@example.com', '1234567890', '123 Elm Street'),
('Vaishnavi Katikar', '2004-11-14', 'password1234', 'vaish.katikar@example.com', '0987654321', '789 Maple Avenue');

-- Insert into admin
INSERT INTO admin (email, password)
VALUES 
('admin@example.com', 'adminpass');

-- Insert into service_provider
INSERT INTO service_provider (name, address, contact_details, email, password)
VALUES 
('Pranali More', '456 Oak Street', '0987654321', 'pranali.more@example.com', 'jane123');

-- Insert into unit
INSERT INTO unit (unit_bracket, rate_per_unit)
VALUES 
('200units', 0.05), 
('500units', 0.07), 
('1000units', 0.10);

-- Insert into billing
INSERT INTO billing (customer_id, before_due_date, after_due_date, amount, meter_reading, billing_date, month, consumption_units, bill_calculation)
VALUES 
(1, 50.00, 60.00, 55.00, 120.00, '2024-08-01', 'August', 240.00, 55.00),
(2, 100.00, 120.00, 110.00, 250.00, '2024-08-01', 'August', 500.00, 110.00);

-- Insert into transaction
INSERT INTO transaction (customer_id, billing_id, payable, payment_date, status)
VALUES 
(1, 1, 55.00, '2024-08-10', 'paid'),
(2, 2, 110.00, '2024-08-12', 'pending');

-- Insert into feedback
INSERT INTO feedback (customer_id, admin_id, feedback)
VALUES 
(1, 1, 'Great service, very prompt.'),
(2, 1, 'Would appreciate quicker responses to queries.');

-- Insert into complaints
INSERT INTO complaints (customer_id, admin_id, complaint, status)
VALUES 
(1, 1, 'Issue with last month’s billing.', 'resolved'),
(2, 1, 'No one came to check the meter this month.', 'pending');

SELECT *  
INTO OUTFILE '"C:\DBMS ASS\exported_data.csv"' 
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
FROM admin;

SHOW VARIABLES LIKE 'secure_file_priv';


