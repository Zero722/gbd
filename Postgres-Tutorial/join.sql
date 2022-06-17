SELECT * FROM employee CROSS JOIN department;

INSERT INTO employee (emp_name, address, age, gender, email, dept_id)
	VALUES
		('kapil', 'Sankhamul', 37, 'Male', 'kapil@gmail.com',1),
		('lara', 'Patan', 27, 'Female', 'lara@gmail.com',4),
		('manas', 'Chahabil', 31, 'Male', 'manas@gmail.com',5),
		('nina', 'Hetauda', 29, 'Female', 'nina@gmail.com',3),
		('oman', 'Lagankhel', 31, 'Male', 'oman@gmail.com',4);

INSERT INTO department (dept_name, block)
	VALUES
		('Canteen', 'D'),
		('Security', 'D'),
		('Networking', 'B');
		
		 
SELECT emp_name, salary FROM employee WHERE salary IS NOT NULL
		
SELECT emp.emp_name, emp.email, emp.salary, dept.dept_name 
FROM employee emp 
INNER JOIN department dept 
ON emp.dept_id = dept.id 
ORDER BY emp.id;

SELECT emp.emp_name, emp.email, emp.salary, dept.dept_name 
FROM employee emp 
RIGHT OUTER JOIN department dept 
ON emp.dept_id = dept.id 
ORDER BY dept.id;

SELECT emp.emp_name, emp.email, emp.salary, dept.dept_name 
FROM employee emp 
FULL OUTER JOIN department dept 
ON emp.dept_id = dept.id 
ORDER BY dept.id;