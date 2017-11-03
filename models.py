from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)

    name = Column(String)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)

    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    sex = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))

    department = relationship(Department, foreign_keys=[department_id])
    role = relationship(Role, foreign_keys=[role_id])


class Form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key=True)

    anonymous = Column(String)
    statement = Column(String)
    created_by_id = Column(Integer, ForeignKey('employee.id'))
    against_id = Column(Integer, ForeignKey('employee.id'))

    created_by = relationship(Employee, foreign_keys=[created_by_id])
    against = relationship(Employee, foreign_keys=[against_id])



