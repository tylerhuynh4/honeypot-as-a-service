-- Deo Medical Clinic DB Backup
-- Generated: 2026-04-01

CREATE TABLE patients (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    ssn VARCHAR(11),
    diagnosis VARCHAR(200)
);

INSERT INTO patients VALUES (001, 'Tyler Huynh', '2003-04-28', '528-32-1847', 'Hypertension');
INSERT INTO patients VALUES (002, 'Peter Parker', '2001-08-10', '374-91-2053', 'Spinal Fracture');
INSERT INTO patients VALUES (003, 'Yuji Itadori', '2003-03-20', '819-44-3671', 'Asthma');