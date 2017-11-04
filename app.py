from flask import Flask, request, jsonify
from sqlalchemy import func
from collections import Counter

from models import *
from schema import *

app = Flask(__name__)
app.debug = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

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

    return employee_schema.dump(employee).data
  
# all forms
@app.route("/api/forms", methods=["GET"])
def get_forms():
    all_forms = Form.query.all()
    result = forms_schema.dump(all_forms)

    return jsonify(result.data)

# form by id
@app.route("/api/form/<id>", methods=["GET"])
def get_form(id):
    form = Form.query.get(id)
    result = form_schema.dump(form)
    return jsonify(result.data)

# all departments
@app.route("/api/departments", methods=["GET"])
def get_departments():
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)

    return jsonify(result.data)

# department by id
@app.route("/api/department/<id>", methods=["GET"])
def get_department(id):

	data = {}

	department = Department.query.get(id)
	result = department_schema.dump(department)
	return jsonify(result.data)

# department form count by id 
@app.route("/api/department/<id>/forms", methods=["GET"])
def get_department_id_count(id):

	data = {}

	count = db_session.query(Form).filter(Form.against_id==id).count()

	department = Department.query.get(id)
	department_name = department.name

	data[department_name] = count

	return jsonify(data)

# department return all count 
@app.route("/api/department/forms", methods=["GET"])
def get_department_count():

    data = {}

    all_employees = Employee.query.all()
    all_forms = Form.query.all()
    
    for employee in all_employees:
    	against_count = db_session.query(Form).filter(Form.against_id==employee.id).count()
    	created_count = db_session.query(Form).filter(Form.created_by_id==employee.id).count()

    	department = Department.query.get(employee.department_id)

    	department_name = department.name

    	data[department_name] = {}
    	if 'against' in data[department_name]:
    		data[department_name]['against'] += against_count
    	else:
    		data[department_name]['against'] = against_count
    	if 'created' in data[department_name]:
    		data[department_name]['created'] += created_count
    	else:
    		data[department_name]['created'] = created_count		

    return jsonify(data)

# forms per employee id
@app.route("/api/employee/<id>/forms", methods=["GET"])
def get_forms_per_employee(id):

	data = {}

	against = db_session.query(Form).filter(Form.against_id==id).count()
	created_by = db_session.query(Form).filter(Form.created_by_id==id).count()
	data['against'] = against
	data['created'] = created_by

	return jsonify(data)

# forms for all employees
@app.route("/api/employee/forms", methods=["GET"])
def get_forms_employees():

	data = {}

	all_employees = Employee.query.all()

	for employee in all_employees:
		against = db_session.query(Form).filter(Form.against_id==employee.id).count()
		created_by = db_session.query(Form).filter(Form.created_by_id==employee.id).count()
		data[employee.id] = {}
		data[employee.id]['against'] = against
		data[employee.id]['created'] = created_by
		
	return jsonify(data)


if __name__ == '__main__':
    app.run()
    