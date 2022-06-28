from sqlalchemy import ForeignKey, create_engine, Table, Column, Integer, String, MetaData, Boolean, ForeignKey, insert, update, desc
from sqlalchemy.sql import select, func, distinct
import pandas as pd

def create_table(conn, meta, engine):

    department = Table(
        'department', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )

    employee = Table(
        'employee', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('departmentid', Integer,  ForeignKey(
            'department.id'), nullable=False),
        Column('salary', String, nullable=False),
        Column('active', Boolean, nullable=False),
    )

    meta.create_all(engine)


def insert_to_table(conn, meta, engine):

    department = Table(
        'department', 
        meta, 
        autoload=True, 
        autoload_with=engine
    )

    employee = Table(
        'employee', 
        meta, 
        autoload=True, 
        autoload_with=engine
    )
    
    dept = []
    dept.append([1, 'IT'])
    dept.append([2, 'Admin'])
    dept.append([3, 'HR'])
    dept.append([4, 'Accounts'])
    dept.append([5, 'Health'])

    emp = []
    emp.append([1, 'John', 1, 2000, 1])
    emp.append([2, 'Sean', 1, 4000, 1])
    emp.append([3, 'Eric', 2, 2000, 1])
    emp.append([4, 'Nancy', 2, 2000, 1])
    emp.append([5, 'Lee', 3, 3000, 1])
    emp.append([6, 'Steven', 4, 2000, 1])
    emp.append([7, 'Matt', 1, 5000, 1])
    emp.append([8, 'Sarah', 1, 2000, 0])


    for dep in dept:
        ins = department.insert().values(id=dep[0], name=dep[1])
        conn.execute(ins)
        
    for em in emp:
        ins = employee.insert().values(id=em[0], name=em[1], departmentid=em[2], salary=em[3], active=em[4])
        conn.execute(ins)


def selecting(conn, meta, engine):
    department = Table(
        'department', 
        meta, 
        autoload=True, 
        autoload_with=engine
    )

    employee = Table(
        'employee', 
        meta, 
        autoload=True, 
        autoload_with=engine
    )
    # query = select([func.count()]).select_from(employee)
    join_emp_dep = employee.join(department, employee.c.departmentid == department.c.id)

    query2 = select(employee).order_by(employee.c.salary.desc())

    query3 = select([distinct(employee.c.salary)])

    query4 = select([func.count()]).filter(employee.c.active == True)

    # Update
    query5 = update(employee).where(employee.c.name == 'Nancy').values(departmentid = select(department.c.id).where(department.c.name == 'HR'))
    print(query5)

    query7 = select(employee.c.name, department.c.name).select_from(join_emp_dep)

    query8a = select(employee.c.departmentid).group_by(employee.c.departmentid).order_by(desc(func.count(employee.c.departmentid))).limit(1)
    query8b = select(department.c.name).where(department.c.id == query8a)

    query9 = select(employee.c.departmentid).group_by(employee.c.departmentid)
    a = pd.read_sql(query9, conn)
    print(a)
    
    # result = conn.execute(query7)
    # print(result.fetchall())
    # titles = result._metadata.keys
    # print(type(titles))
    # print(titles)
    # list_title = list(titles)
    # print(list_title)


def main():
    engine = create_engine('postgresql://postgres:admin123@localhost/sqlalchemy')
    meta = MetaData()

    try:
        conn = engine.connect()
        print("DB connected")
    except:
        print("DB not connected")

    # create_table(conn, meta, engine)
    # insert_to_table(conn, meta, engine)
    selecting(conn, meta, engine)


main()