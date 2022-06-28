import psycopg2, os
import pandas as pd

def check_folder(folder):
    if(not os.path.isdir(folder)):
        os.mkdir(folder)


def create_table(conn):
    """Create table in database
    """

    table1 = "department"
    table2 = "employee"

    db_create_dept = """
        CREATE TABLE {table1}(
        Id SERIAL PRIMARY KEY,
        Name VARCHAR (50) NOT NULL
        );
    """.format(table1 = table1)

    db_create_emp = """
        CREATE TABLE {table2}(
        Id SERIAL PRIMARY KEY,
        Name VARCHAR (50) NOT NULL,
        DepartmentId INTEGER NOT NULL,
        Salary INTEGER NOT NULL,
        Active BOOL NOT NULL,
        CONSTRAINT fk_department
            FOREIGN KEY(DepartmentId) 
            REFERENCES Department(id)
        );
    """.format(table2 = table2)

    with conn:
        with conn.cursor() as cursor:

            table_list = [table1, table2]
            db_create = [db_create_dept, db_create_emp]

            for idx, table in enumerate(table_list):
                cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (table,))
                flag = cursor.fetchone()[0]
                if not flag:
                    cursor.execute(db_create[idx])


def insert_to_table(conn):
    """Insert data to table
    """
    insert_dept = """
        INSERT INTO Department (Name)
        VALUES 
            ('IT'),
            ('Admin'),
            ('HR'),
            ('Accounts'),
            ('Health');
    """

    insert_emp = """
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
    """

    with conn:
        with conn.cursor() as cursor:
           
            cursor.execute(insert_dept)
            cursor.execute(insert_emp)


def create_db(dbname):

    conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="admin123")

    db_create = """
        CREATE DATABASE {dbname};
    """.format(dbname = dbname)

    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute("SELECT datname FROM pg_database;")
    list_database = cursor.fetchall()

    if (dbname,) not in list_database:
        cursor.execute(db_create)


def view_all(conn):
    select_all_emp = """
        SELECT * FROM Employee;
    """

    select_all_dept = """
        SELECT * FROM Department;
    """

    with conn:
        with conn.cursor() as cursor:
        
            cursor.execute(select_all_emp)
            all_emp = cursor.fetchall()
            emp_title = [x[0] for x in cursor.description]

            cursor.execute(select_all_dept)
            all_dept = cursor.fetchall()
            dept_title = [x[0] for x in cursor.description]
    
    emp_df = pd.DataFrame(all_emp, columns=emp_title)
    dept_df = pd.DataFrame(all_dept, columns=dept_title)


def tasks(conn, csvfiles):

    query2 = """
        SELECT * 
            FROM Employee 
            ORDER BY Salary ASC
    """

    query3 = """
        SELECT DISTINCT Salary 
            FROM Employee 
            ORDER BY Salary;
    """

    query4 = """
        SELECT count(Active) 
            FROM Employee 
            WHERE Active = '1';
    """

    query5 = """
        UPDATE Employee emp 
            SET DepartmentId = 
                (SELECT Id FROM Department dept 
                WHERE dept.Name = 'HR' ) 
            WHERE emp.Name = 'Nancy';
    """

    query6 = """
        SELECT emp.Id, emp.Name, dept.Name, emp.Salary, emp.Active
            FROM Employee emp 
            INNER JOIN Department dept
            ON emp.DepartmentId = dept.Id
            ORDER BY emp.Salary DESC
            LIMIT 2;
    """

    query7 = """
        SELECT emp.Id, emp.Name, dept.Name
            FROM Employee emp 
            INNER JOIN Department dept
            ON emp.DepartmentId = dept.Id;
    """

    query8 = """
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
    """

    query9 = """
        SELECT dept.Name
            FROM Employee emp
            RIGHT OUTER JOIN Department dept
            ON emp.DepartmentId = dept.Id
            WHERE emp.DepartmentId IS NULL
    """

    query10 = """
        SELECT Name, Salary 
            FROM Employee 
            WHERE Salary IN
                (SELECT emp.Salary
                FROM employee emp 
                GROUP BY emp.Salary
                HAVING count(emp.Salary) > 1)
            ORDER BY Salary;
    """

    queries = [query2, query3, query4, query6, query7, query8, query9, query10]

    for idx, query in enumerate(queries):

        query_df = pd.read_sql(query, conn)
        print(query_df)
        query_df.to_csv(csvfiles + str(idx) + ".csv", index=False)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query5)


def data_manipulate(conn, csvfiles):
    select_all_emp = """
        SELECT * FROM Employee;
    """

    select_emp_dept = """
        SELECT emp.Id, emp.Name AS empName, dept.Name As deptName
            FROM Employee emp 
            INNER JOIN Department dept
            ON emp.DepartmentId = dept.Id;
    """

    with conn:
        with conn.cursor() as cursor:

            cursor.execute(select_all_emp)
            rows = cursor.fetchall()
            title = [x[0].capitalize() for x in cursor.description]
            query_df = pd.DataFrame(rows, columns=title)
            query_df.Salary = (query_df.Salary * 1.1).astype(int)
            print(query_df)
            query_df.to_csv(csvfiles + "salary_incr" + ".csv", index=False)

            print()

            cursor.execute(select_emp_dept)
            rows = cursor.fetchall()
            title = [x[0].capitalize() for x in cursor.description]
            query_df = pd.DataFrame(rows, columns=title)
            query_df.loc[query_df.Empname == "John", 'Deptname'] = "HR"
            print(query_df)
            query_df.to_csv(csvfiles + "change_dept" + ".csv", index=False)


def csv_to_database(conn, csvfiles):

    table1 = "emp"
    table2 = "emp_dept"
    filepath1 = "'" +  csvfiles + "salary_incr" + ".csv" + "'"
    filepath2 = "'" + csvfiles + "change_dept" + ".csv" + "'"


    updated_salary = """
        CREATE TABLE {table1}(
        Id SERIAL PRIMARY KEY,
        Name VARCHAR (50) NOT NULL,
        DepartmentId INTEGER NOT NULL,
        Salary INTEGER NOT NULL,
        Active BOOL NOT NULL,
        CONSTRAINT fk_department
            FOREIGN KEY(DepartmentId) 
            REFERENCES Department(id)
        );
    """.format(table1 = table1)

    changed_dept = """
        CREATE TABLE {table2}(
        Id SERIAL PRIMARY KEY,
        Emp_name VARCHAR (50) NOT NULL,
        Dept_name VARCHAR (50) NOT NULL
        );
    """.format(table2 = table2)

    query1 = """
        COPY emp(id, name, departmentid, salary, active)
            FROM {filepath}
            DELIMITER ','
            CSV HEADER;
    """.format(filepath = filepath1)

    query2 = """
        COPY emp_dept(id, emp_name, dept_name)
            FROM {filepath}
            DELIMITER ','
            CSV HEADER;
    """.format(filepath = filepath2)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(updated_salary)
            cursor.execute(changed_dept)
            cursor.execute(query1)
            cursor.execute(query2)


def main():

    dbname = "task_6"
    try: 
        create_db(dbname)
    finally:
        conn = psycopg2.connect(
        host = "localhost",
        database = dbname,
        user = "postgres",
        password = "admin123")

    csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\\csv\\"
    check_folder(csvfiles)


    # create_table(conn)
    # insert_to_table(conn)
    # view_all(conn)
    tasks(conn, csvfiles)
    # data_manipulate(conn, csvfiles)
    # csv_to_database(conn, csvfiles)
    
main()

