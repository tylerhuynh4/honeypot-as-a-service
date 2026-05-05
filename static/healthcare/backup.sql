-- Clinic DB Backup 2026-04-01
-- CONFIDENTIAL

CREATE TABLE patients (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    ssn VARCHAR(11),
    diagnosis VARCHAR(200),
    insurance VARCHAR(100)
);

INSERT INTO patients VALUES (001, 'Tyler Huynh', '04/28/2003', '528-32-1847', 'Hypertension', 'Medicare');
INSERT INTO patients VALUES (002, 'Peter Parker', '08/10/2001', '374-91-2053', 'Spinal Fracture', 'Avengers');
INSERT INTO patients VALUES (003, 'Yuji Itadori', '03/20/2003', '819-44-3671', 'Asthma', 'United');
INSERT INTO patients VALUES (004, 'Michael Myers', '10/19/1957', '221-67-4892', 'Anxiety', 'Cigna');
INSERT INTO patients VALUES (005, 'Donald Toliver', '06/12/1994', '663-28-5104', 'COPD', 'Medicare');