from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func
from collections import Counter
from random import *
from models import *
from schema import *

app = Flask(__name__)
CORS(app)
app.debug = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# submit form
@app.route("/submitform", methods=['POST'])
def submit_form():
  anonymous = request.form['anonymous']
  statement = request.form['statement']
  created_by_id = randint(1, 20) 	# simulate a logged in id
  against_id = request.form['against_id']
  form = Form(anonymous = anonymous, statement = statement, created_by_id = created_by_id, against_id =against_id)
  db.session.add(form)
  db.session.commit()

# all employees
@app.route("/api/employee", methods=["GET"])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)

    return jsonify(result.data)

# employee by id
@app.route('/api/employee/<id>')
def get_employee(id):
    employee = Employee.query.get(id)
    result = employee_schema.dump(employee)

    return jsonify(result.data)

# all forms
@app.route("/api/forms", methods=["GET"])
def get_forms():
    all_forms = Form.query.all()
    result = forms_schema.dump(all_forms)

    return jsonify(result.data)

# all forms with department names (time-series)
@app.route("/api/forms/department", methods=["GET"])
def get_form_department():

	data = {}

	all_forms = Form.query.all()
	for form in all_forms:
		data[form.id] = {}
		data[form.id]['against'] = form.against_id
		data[form.id]['anonymous'] = form.anonymous
		data[form.id]['created_at'] = form.created_at
		data[form.id]['created_by'] = form.created_by_id
		data[form.id]['id'] = form.id
		data[form.id]['statement'] = form.statement

		employee_against = Employee.query.get(form.against_id)
		department_against_id = employee_against.department_id
		department_against_name = Department.query.get(department_against_id)
		data[form.id]['sex_against'] = employee_against.sex
		data[form.id]['department_against'] = department_against_name.name

		employee_created = Employee.query.get(form.created_by_id)
		department_created_id = employee_created.department_id
		department_created_name = Department.query.get(department_created_id)
		data[form.id]['sex_created'] = employee_created.sex
		data[form.id]['department_created_by'] = department_created_name.name

	return jsonify(data)

# all forms with employee info (time-series)
@app.route("/api/forms/employee", methods=["GET"])
def get_forms_employee():

	data = {}

	all_forms = Form.query.all()
	for form in all_forms:
		data[form.id] = {}
		data[form.id]['against'] = form.against_id
		data[form.id]['anonymous'] = form.anonymous
		data[form.id]['created_at'] = form.created_at
		data[form.id]['created_by'] = form.created_by_id
		data[form.id]['id'] = form.id
		data[form.id]['statement'] = form.statement

		employee_against = Employee.query.get(form.against_id)
		data[form.id]['employee_name_against'] = employee_against.name
		data[form.id]['hired_on_against'] = employee_against.hired_on
		data[form.id]['sex_against'] = employee_against.sex
		role = Role.query.get(employee_against.role_id)
		data[form.id]['role_against'] = role.name

		employee_created = Employee.query.get(form.created_by_id)
		data[form.id]['employee_name_created'] = employee_created.name
		data[form.id]['hired_on_created'] = employee_created.hired_on
		data[form.id]['sex_created'] = employee_created.sex
		role = Role.query.get(employee_created.role_id)
		data[form.id]['role_created'] = role.name

	return jsonify(data)

# form by id
@app.route("/api/form/<id>", methods=["GET"])
def get_form(id):
    form = Form.query.get(id)
    result = form_schema.dump(form)
    return jsonify(result.data)

# all department names
@app.route("/api/departments", methods=["GET"])
def get_departments():
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)

    return jsonify(result.data)

# department name by id
@app.route("/api/department/<id>", methods=["GET"])
def get_department(id):

	data = {}

	department = Department.query.get(id)
	result = department_schema.dump(department)
	return jsonify(result.data)

# department by id form count (against and created)
@app.route("/api/department/<id>/form-count", methods=["GET"])
def get_department_id_count(id):

	data = {}
	department = Department.query.get(id)
	department_name = department.name

	against = db_session.query(Form).filter(Form.against_id==id).count()
	created_by = db_session.query(Form).filter(Form.created_by_id==id).count()
	data[department_name] = {}

	data[department_name]['against'] = against
	data[department_name]['created'] = created_by

	return jsonify(data)

# all departments form count (against and created)
@app.route("/api/department/forms", methods=["GET"])
def get_department_count():

    data = {}

    all_employees = Employee.query.all()
    all_forms = Form.query.all()
    all_departments = Department.query.all()

    for department in all_departments:
    	data[department.name] = {}
    	data[department.name]['against'] = 0
    	data[department.name]['created'] = 0

    for employee in all_employees:
    	against_count = db_session.query(Form).filter(Form.against_id==employee.id).count()
    	created_count = db_session.query(Form).filter(Form.created_by_id==employee.id).count()

    	department = Department.query.get(employee.department_id)

    	data[department.name]['against'] += against_count
    	data[department.name]['created'] += created_count


    return jsonify(data)

# all roles form count (against and created)
@app.route("/api/role/forms", methods=["GET"])
def get_role_count():

    data = {}

    all_employees = Employee.query.all()
    all_forms = Form.query.all()
    all_roles = Role.query.all()

    for role in all_roles:
    	data[role.name] = {}
    	data[role.name]['against'] = 0
    	data[role.name]['created'] = 0

    for employee in all_employees:
    	against_count = db_session.query(Form).filter(Form.against_id==employee.id).count()
    	created_count = db_session.query(Form).filter(Form.created_by_id==employee.id).count()

    	role = role.query.get(employee.role_id)

    	data[role.name]['against'] += against_count
    	data[role.name]['created'] += created_count


    return jsonify(data)

# employee by id form count (against and created)
@app.route("/api/employee/<id>/forms", methods=["GET"])
def get_forms_per_employee(id):

	data = {}

	against = db_session.query(Form).filter(Form.against_id==id).count()
	created_by = db_session.query(Form).filter(Form.created_by_id==id).count()
	data['against'] = against
	data['created'] = created_by

	return jsonify(data)

# all employees form count (against and created)
@app.route("/api/employee/forms", methods=["GET"])
def get_forms_employees():

	data = {}

	all_employees = Employee.query.all()

	for employee in all_employees:
		against = db_session.query(Form).filter(Form.against_id==employee.id).count()
		created_by = db_session.query(Form).filter(Form.created_by_id==employee.id).count()
		data[employee.name] = {}
		data[employee.name]['against'] = against
		data[employee.name]['created'] = created_by
		

	return jsonify(data)


if __name__ == '__main__':
    app.run()

