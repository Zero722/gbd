CREATE TABLE employee(
	id SERIAL PRIMARY KEY,
	emp_name VARCHAR (50) NOT NULL,
	address VARCHAR (50) NOT NULL,
	age SMALLINT NOT NULL,
	gender VARCHAR (8) NOT NULL,
	email VARCHAR (255) UNIQUE, 
	dept_id INTEGER NOT NULL,
	CONSTRAINT fk_department
      FOREIGN KEY(dept_id) 
	  REFERENCES department(id)
)

CREATE TABLE department(
	id SERIAL PRIMARY KEY,
	dept_name VARCHAR (50) NOT NULL,
	block VARCHAR (50) NOT NULL
)

SELECT * FROM department

INSERT INTO employee VALUES(
	1, 'akash', 'Baneshwor', 32, 'Male', 'akash@gmail.com',1
)

INSERT INTO department (dept_name, block)
	VALUES('IT', 'B')
	
INSERT INTO department (dept_name, block)
	VALUES
		('Sales', 'C'),
		('Analytics', 'B'),
		('HR', 'A');

INSERT INTO employee (emp_name, address, age, gender, email, dept_id)
	VALUES
		('akash', 'Baneshwor', 32, 'Male', 'akash@gmail.com',3),
		('bikash', 'Koteshwor', 34, 'Male', 'bikash@gmail.com',4),
		('cindy', 'Thapathali', 25, 'Female', 'cindy@gmail.com',2),
		('dio', 'Thimi', 28, 'Male', 'dio@gmail.com',5),
		('emilia', 'Jawlakhel', 37, 'Female', 'emilia@gmail.com',1);
		
INSERT INTO employee (emp_name, address, age, gender, email, dept_id)
	VALUES
		('francis', 'Kalimati', 32, 'Male', 'francis@gmail.com',3),
		('gina', 'Kalanki', 34, 'Female', 'gina@gmail.com',4),
		('hulk', 'Thamel', 25, 'Male', 'hulk@gmail.com',2),
		('ino', 'Hetauda', 28, 'Female', 'ino@gmail.com',2),
		('jack', 'Lagankhel', 37, 'Male', 'jack@gmail.com',1);
		
SELECT * FROM employee ORDER BY id

UPDATE employee SET age = 29 WHERE emp_name = 'dio';
UPDATE employee SET gender = 'Male' WHERE gender = 'MaleMale'

DELETE FROM employee
DELETE FROM employee WHERE id = 12

ALTER TABLE employee ADD salary INT; 
UPDATE employee SET salary = (age - dept_id) * 1000 WHERE salary IS NULL
UPDATE employee SET salary = salary * 1.1 WHERE salary IS NOT NULL

TRUNCATE employee RESTART IDENTITY;

SELECT emp_name, salary FROM employee

SELECT * FROM employee WHERE salary > 28000
SELECT * FROM employee WHERE emp_name like '%in%'
SELECT * FROM employee WHERE emp_name like '_%in%'

SELECT sum(salary) FROM employee GROUP BY salary


SELECT dept.dept_name, avg(salary) AS average, sum(salary) AS total
FROM employee emp INNER JOIN department dept
ON emp.dept_id = dept.id
GROUP BY dept.dept_name;


SELECT dept.dept_name, avg(salary) AS average, sum(salary) AS total
FROM employee emp INNER JOIN department dept
ON emp.dept_id = dept.id
GROUP BY dept.dept_name
HAVING sum(salary) < 100000;

