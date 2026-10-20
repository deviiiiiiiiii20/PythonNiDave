
CREATE DATABASE IF NOT EXISTS barangay_amsic;
USE barangay_amsic;


CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    username      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(20)  NOT NULL,
    address       VARCHAR(255),
    position      VARCHAR(100),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_username (username)
);


CREATE TABLE IF NOT EXISTS complaints (
    complaint_id      INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number   VARCHAR(30)  NOT NULL,
    user_id           INT          NOT NULL,
    category          VARCHAR(100) NOT NULL,
    location          VARCHAR(255) NOT NULL,
    description       TEXT         NOT NULL,
    status            VARCHAR(50)  NOT NULL,
    assigned_staff_id INT,
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_tracking (tracking_number),
    KEY idx_user_id (user_id),
    KEY idx_status (status),
    KEY idx_assigned_staff (assigned_staff_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (assigned_staff_id) REFERENCES users (user_id)
);


CREATE TABLE IF NOT EXISTS complaint_updates (
    update_id    INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT         NOT NULL,
    staff_id     INT,
    status       VARCHAR(50) NOT NULL,
    remarks      TEXT,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    KEY idx_complaint_id (complaint_id),
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id),
    FOREIGN KEY (staff_id) REFERENCES users (user_id)
);

INSERT INTO users (full_name, username, password_hash, role, address, position)
VALUES
    ('Test Staff One', 'staff1',
     '05dd4a1376a72d9a5e0fad32000f7e61651a5cef5c9c9a0c3816c7443dafbf6f',
     'staff', NULL, 'Barangay Secretary'),
    ('Test Staff Two', 'staff2',
     '05dd4a1376a72d9a5e0fad32000f7e61651a5cef5c9c9a0c3816c7443dafbf6f',
     'staff', NULL, 'Barangay Kagawad'),
    ('Test Resident One', 'resident1',
     '528bc8e3ff3618480f49cfffaf84f2b0ac9fb3404ffbc78130447e07e7031c3e',
     'resident', 'Test Street, Barangay Amsic', NULL);

INSERT INTO complaints (complaint_id, tracking_number, user_id, category, location, description, status)
VALUES
    (1, 'AMS-00001', 3, 'Streetlights', 'Corner of Test Street',
     'The streetlight near the corner has been off for a week.', 'Submitted'),
    (2, 'AMS-00002', 3, 'Waste Collection', 'Near the basketball court',
     'Garbage was not collected this week.', 'Under Review');

INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
VALUES
    (1, NULL, 'Submitted', 'Complaint submitted by resident.'),
    (2, NULL, 'Submitted', 'Complaint submitted by resident.'),
    (2, 1, 'Under Review', 'Checking the collection schedule.');
