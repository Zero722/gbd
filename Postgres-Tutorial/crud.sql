CREATE TABLE students(
	stu_id INTEGER PRIMARY KEY,
	stu_name VARCHAR (50) NOT NULL,
	roll_no SMALLINT NOT NULL,
	stu_class SMALLINT NOT NULL,
	stu_section VARCHAR (5) NOT NULL,
	email VARCHAR (255) UNIQUE
)

INSERT INTO students VALUES(
	1, 'akash', 1, 10, 'A', 'akash@gmail.com'
)

INSERT INTO students VALUES(
	2, 'binay', 2, 6, 'A', 'binay@gmail.com'
)

INSERT INTO students VALUES(
	3, 'cath', 3, 7, 'A', 'cath@gmail.com'
)

INSERT INTO students VALUES(
	4, 'dikshya', 6, 10, 'A', 'dikshya@gmail.com'
)

INSERT INTO students VALUES
	( 5, 'ethan', 5, 10, 'A', 'ethan@gmail.com'),
	( 6, 'francis', 6, 10, 'A', 'francis@gmail.com');	

UPDATE students SET roll_no = 4 WHERE stu_name = 'dikshya';
UPDATE students SET roll_no = stu_id + 1;

DELETE FROM students WHERE stu_name = 'francis'



SELECT * FROM students ORDER BY stu_id