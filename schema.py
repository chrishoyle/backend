from marshmallow_sqlalchemy import ModelSchema
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel
from models import Form as FormModel


class DepartmentSchema(ModelSchema):
    class Meta:

        model = DepartmentModel

class EmployeeSchema(ModelSchema):
    class Meta:
        model = EmployeeModel

class RoleSchema(ModelSchema):
    class Meta:
        model = RoleModel

class FormSchema(ModelSchema):
    class Meta:
        model = FormModel

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
employee_schema = EmployeeSchema(many=True)
employees_schema = EmployeeSchema(many=True)
roles_schema = RoleSchema(many=True)
form_schema = FormSchema()
forms_schema = FormSchema(many=True)