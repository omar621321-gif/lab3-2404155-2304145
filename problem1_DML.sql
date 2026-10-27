USE company;

-- 1) employees first, without a department yet (Dno is NULL)
INSERT INTO employee (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES
('123456789', 'Ahmed', 'Hassan', '1985-03-12', 'Alexandria', 'M', 15000.00, NULL),
('987654321', 'Sara',  'Ali',    '1990-07-25', 'Cairo',      'F', 12000.00, NULL),
('555666777', 'Omar',  'Khaled', '1992-11-02', 'Giza',        'M',  9000.50, NULL),
('111222333', 'Mona',  'Samir',  '1988-01-30', 'Alexandria', 'F', 11000.00, NULL);

-- 2) departments, with the managers that now exist
INSERT INTO department (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(1, 'Research',  '123456789', '2015-06-01'),
(2, 'Software',  '987654321', '2018-09-15'),
(3, 'Marketing', '111222333', '2020-02-01');

-- 3) now give each employee a department
UPDATE employee SET Dno = 1 WHERE ssn IN ('123456789', '555666777');
UPDATE employee SET Dno = 2 WHERE ssn = '987654321';
UPDATE employee SET Dno = 3 WHERE ssn = '111222333';

-- 4) projects
INSERT INTO project (Pnumber, Pname, Plocation, Dno) VALUES
(10, 'ProductX', 'Alexandria', 1),
(20, 'ProductY', 'Cairo',      2),
(30, 'Campaign', 'Giza',       3);
