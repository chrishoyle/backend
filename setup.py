from models import engine, db_session, Base, Department, Employee, Role, Form

Base.metadata.create_all(bind=engine)

# Departments 
engineering = Department(name='Engineering')
hr = Department(name='Human Resources')
production = Department(name='Production')
rd = Department(name='Research and Development')
marketing = Department(name='Marketing')
accounting = Department(name='Accounting')

db_session.add(engineering)
db_session.add(hr)
db_session.add(production)
db_session.add(rd)
db_session.add(marketing)
db_session.add(accounting)

# Roles
manager = Role(name='manager')
engineer = Role(name='engineer')
programmer = Role(name='programmer')
security = Role(name='security specialist')
data_admin = Role(name='database administrator')

db_session.add(manager)
db_session.add(engineer)
db_session.add(programmer)
db_session.add(security)
db_session.add(data_admin)


# Employees
peter = Employee(name='Peter', department=engineering, role=engineer, sex='M')
roy = Employee(name='Roy', department=engineering, role=engineer, sex='M')
tracy = Employee(name='Tracy', department=hr, role=manager, sex='F')

db_session.add(peter)
db_session.add(roy)
db_session.add(tracy)

# Forms
form1 = Form(anonymous=True, statement='Example statement', created_by=peter, against=roy)
form2 = Form(anonymous=True, statement='Example statement', created_by=roy, against=peter)
form3 = Form(anonymous=True, statement='Example statement', created_by=tracy, against=roy)

db_session.add(form1)
db_session.add(form2)
db_session.add(form3)

db_session.commit()

