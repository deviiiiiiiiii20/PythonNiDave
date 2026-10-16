-- ======================================================================
-- schema.sql - Barangay Amsic Complaint and Request Tracking System
-- Run this script ONCE in phpMyAdmin (SQL tab) or the MySQL command line.
-- To start over:  DROP DATABASE barangay_amsic;  then run this script again.
-- ======================================================================

CREATE DATABASE IF NOT EXISTS barangay_amsic
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE barangay_amsic;

-- ----------------------------------------------------------------------
-- TABLE: users (residents and staff share one table; "role" tells them apart)
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    username      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,          -- "salt$hash", never the plain password
    role          VARCHAR(20)  NOT NULL,          -- 'resident' or 'staff'
    address       VARCHAR(255) NULL,              -- used by residents
    position      VARCHAR(100) NULL,              -- used by staff
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- UNIQUE KEY also creates an index, so username lookups (login) are fast
    -- and two users can never share the same username.
    UNIQUE KEY uq_users_username (username),
    CONSTRAINT chk_users_role CHECK (role IN ('resident', 'staff'))
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------
-- TABLE: complaints
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id      INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number   VARCHAR(30)  NOT NULL,      -- e.g. AMS-00001
    user_id           INT          NOT NULL,      -- the resident who submitted it
    category          VARCHAR(100) NOT NULL,
    location          VARCHAR(255) NOT NULL,
    description       TEXT         NOT NULL,
    status            VARCHAR(50)  NOT NULL DEFAULT 'Submitted',
    assigned_staff_id INT          NULL,          -- NULL until staff assigns it
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                      ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_complaints_tracking (tracking_number),
    KEY idx_complaints_user_id (user_id),
    KEY idx_complaints_status (status),
    KEY idx_complaints_assigned_staff (assigned_staff_id),
    CONSTRAINT fk_complaints_user
        FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT fk_complaints_staff
        FOREIGN KEY (assigned_staff_id) REFERENCES users (user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------
-- TABLE: complaint_updates (the HISTORY of every status change / remark)
-- staff_id is NULL for the first record because the resident, not staff,
-- submitted the complaint.
-- ----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS complaint_updates (
    update_id    INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT         NOT NULL,
    staff_id     INT         NULL,
    status       VARCHAR(50) NOT NULL,
    remarks      TEXT        NULL,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_updates_complaint_id (complaint_id),
    CONSTRAINT fk_updates_complaint
        FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id),
    CONSTRAINT fk_updates_staff
        FOREIGN KEY (staff_id) REFERENCES users (user_id)
) ENGINE=InnoDB;

-- ======================================================================
-- DEVELOPMENT / TEST DATA ONLY - delete before real use!
-- Passwords are stored as PBKDF2 hashes (format: salt$hash).
--   staff1     / Staff123!      (staff)
--   staff2     / Staff123!      (staff)
--   resident1  / Resident123!   (resident)
-- ======================================================================
INSERT INTO users (full_name, username, password_hash, role, address, position)
VALUES
    ('Test Staff One', 'staff1',
     '415ff8ae2d40e0b4562d9c43394bfce2$715084bbfca613e190e4e509d8d7a030b3bdd75d0f14f432feca70e54eb6f0bc',
     'staff', NULL, 'Barangay Secretary'),
    ('Test Staff Two', 'staff2',
     '94077817e7d89b6e1f3a0b4b908785ed$6dccdb12042bd0d1125f6d038b330960768dad9eae42cd2159638265aa184d90',
     'staff', NULL, 'Barangay Kagawad'),
    ('Test Resident One', 'resident1',
     'a5e0efc867557d09cebe1f3b0effc6ae$fbead698012c8d103d0d9da2ab0471a2f611ad4e1a6c8e2406583e2c1bf105d7',
     'resident', 'Test Street, Barangay Amsic', NULL);

-- TEST complaints (belong to resident1)
INSERT INTO complaints (complaint_id, tracking_number, user_id, category, location, description, status)
VALUES
    (1, 'AMS-00001', (SELECT user_id FROM users WHERE username = 'resident1'),
     'Streetlights', 'Corner of Test Street',
     'The streetlight near the corner has been off for a week.', 'Submitted'),
    (2, 'AMS-00002', (SELECT user_id FROM users WHERE username = 'resident1'),
     'Waste Collection', 'Test Street, near the basketball court',
     'Garbage was not collected this week.', 'Under Review');

-- TEST history for the complaints above
INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
VALUES
    (1, NULL, 'Submitted', 'Complaint submitted by resident.'),
    (2, NULL, 'Submitted', 'Complaint submitted by resident.'),
    (2, (SELECT user_id FROM users WHERE username = 'staff1'),
     'Under Review', 'Checking the collection schedule with the garbage hauler.');
