CREATE TABLE Department(
	Id SERIAL PRIMARY KEY,
	Name VARCHAR (50) NOT NULL
);

CREATE TABLE Employee(
	Id SERIAL PRIMARY KEY,
	Name VARCHAR (50) NOT NULL,
	DepartmentId INTEGER NOT NULL,
	Salary INTEGER NOT NULL,
	Active BOOL NOT NULL,
	CONSTRAINT fk_department
      FOREIGN KEY(DepartmentId) 
	  REFERENCES Department(id)
);

INSERT INTO Department (Name)
	VALUES 
		('IT'),
		('Admin'),
		('HR'),
		('Accounts'),
		('Health');
		
INSERT INTO Employee (Name, DepartmentId, Salary, Active)
	VALUES
		('John', 1, 2000, '1'),
		('Sean', 1, 4000, '1'),
		('Eric', 2, 2000, '1'),
		('Nancy', 2, 2000, '1'),
		('Lee', 3, 3000, '1'),
		('Steven', 4, 2000, '1'),
		('Matt', 1, 5000, '1'),
		('Sarah', 1, 2000, '0');
		
SELECT * FROM Employee;
SELECT * FROM Department;

-- Task Start

-- 2
SELECT * 
	FROM Employee 
	ORDER BY Salary ASC;

-- 3
SELECT DISTINCT Salary 
	FROM Employee 
	ORDER BY Salary;

-- 4
SELECT count(Active) 
	FROM Employee 
	WHERE Active = '1';

-- 5
UPDATE Employee emp 
	SET DepartmentId = 
		(SELECT Id FROM Department dept 
		 WHERE dept.Name = 'HR' ) 
	WHERE emp.Name = 'Nancy';

-- 6
SELECT emp.Id, emp.Name, dept.Name, emp.Salary, emp.Active
	FROM Employee emp 
	INNER JOIN Department dept
	ON emp.DepartmentId = dept.Id
	ORDER BY emp.Salary DESC
	LIMIT 2;

-- 7
SELECT emp.Id, emp.Name, dept.Name
	FROM Employee emp 
	INNER JOIN Department dept
	ON emp.DepartmentId = dept.Id;

-- 8
SELECT dept.Name 
	FROM Employee emp
	INNER JOIN Department dept
	ON emp.DepartmentId = dept.Id
	GROUP BY dept.Name
	HAVING count(emp.DepartmentId) = 
		(SELECT max(deptId_count) 
		FROM 
			(SELECT count(emp.DepartmentId) 
		 		AS deptId_count 
		 		FROM employee emp 
		 		GROUP BY emp.DepartmentId) AS max_count);

-- 8
SELECT dept.Name 
	FROM Employee emp
	INNER JOIN Department dept
	ON emp.DepartmentId = dept.Id
	GROUP BY dept.Name
	HAVING count(emp.DepartmentId) = 
		(SELECT DISTINCT deptId_count 
		FROM 
			(SELECT count(emp.DepartmentId) 
		 		AS deptId_count 
		 		FROM employee emp 
		 		GROUP BY emp.DepartmentId) 
		AS max_count
		ORDER BY deptId_count DESC
		LIMIT 1);
			
-- 9
SELECT dept.Name
	FROM Employee emp
	RIGHT OUTER JOIN Department dept
	ON emp.DepartmentId = dept.Id
	WHERE emp.DepartmentId IS NULL
	
-- 10
SELECT Name, Salary 
	FROM Employee 
	WHERE Salary IN
		(SELECT emp.Salary
		FROM employee emp 
		GROUP BY emp.Salary
		HAVING count(emp.Salary) > 1)
	ORDER BY Salary;
	
	
	