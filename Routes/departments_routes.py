from flask import jsonify, render_template, request,session
from flask_cors import CORS
from flask import Blueprint
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
import Department
from Employee import Employee
from Department import Department
from Roles import Role
from database import db



departments_routes = Blueprint('departments_routes', __name__)
CORS(app=departments_routes)
@departments_routes.route('/all-departments', methods=['GET'])
def get_all_departments():
    departments = Department.query.all()
    departments_data = [department.to_json() for department in departments]

    # Fetch department head for each department
    for department_data in departments_data:
        department_head_name = department_data.get('DepartmentHeadName')
        if department_head_name:
            department_head_employee = Employee.query.filter(
                (Employee.FirstName + ' ' + Employee.LastName) == department_head_name
            ).first()
            if department_head_employee:
                department_data['DepartmentHeadID'] = department_head_employee.EmployeeID

    return render_template('HR//departments.html', departments=departments_data)


@departments_routes.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    department = Department.query.get_or_404(department_id)
    return jsonify({'department': department.to_json()})


@departments_routes.route('/departments', methods=['POST'])
def add_department():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        department_name = data.get('DepartmentName')
        description = data.get('Description')
        department_head_name = data.get('DepartmentHeadName')

        if not all([department_name, description]):
            return jsonify({'error': 'Missing required fields in request'}), 400

        # Query employee by name to get the correct employee object
        department_head_employee = None
        if department_head_name:
            department_head_employee = Employee.query.filter(
                (Employee.FirstName + ' ' + Employee.LastName) == department_head_name
            ).first()
            if not department_head_employee:
                return jsonify({'error': f'Employee with the name "{department_head_name}" not found'}), 404

        # Create new department instance
        department = Department(
            DepartmentName=department_name,
            Description=description
        )

        # Set department head if provided
        if department_head_employee:
            department.set_department_head(department_head_employee)

        db.session.add(department)
        db.session.commit()

        return jsonify({'message': 'Department added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@departments_routes.route('/departments/<string:department_name>', methods=['PUT'])
def update_department(department_name):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        department = Department.query.filter_by(DepartmentName=department_name).first()
        if not department:
            return jsonify({'error': f'Department "{department_name}" not found'}), 404

        # Update department attributes if provided in the request
        if 'Description' in data:
            department.Description = data['Description']

        if 'DepartmentHeadName' in data:
            # Query employee by name to get the correct employee object
            department_head_employee = Employee.query.filter(
                (Employee.FirstName + ' ' + Employee.LastName) == data['DepartmentHeadName']
            ).first()
            if not department_head_employee:
                return jsonify({'error': f'Employee with the name "{data["DepartmentHeadName"]}" not found'}), 404

            # Set department head using the employee object
            department.set_department_head(department_head_employee)

        db.session.commit()

        return jsonify({'message': f'Department "{department_name}" updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@departments_routes.route('/departments/<string:department_name>', methods=['DELETE'])
def delete_department(department_name):
    department = Department.query.filter_by(DepartmentName=department_name).first()
    if department:
        # Update employees in the department to set their department to None
        Employee.query.filter_by(DepartmentName=department_name).update(
            {Employee.DepartmentName: None},
            synchronize_session=False
        )

        # Delete the department
        db.session.delete(department)
        db.session.commit()
        return jsonify({'message': f'Department "{department_name}" deleted successfully'}), 200
    else:
        return jsonify({'error': f'Department "{department_name}" not found'}), 404

@departments_routes.route('/departments', methods=['GET'])
def regular_employee_view_department():
    # Retrieve the department name from the session
    department_name = session.get('department')
    if not department_name:
        return jsonify({'error': 'Department not found in session'}), 403

    # Query the database to get all the employees in the department
    employees_in_department = Employee.query.filter_by(DepartmentName=department_name).all()

    # Render the template and pass the employees data to it
    return render_template('Regular-employee//view_departments.html', employees=employees_in_department)


# Route to display the employees in a department along with their roles
@departments_routes.route('/manager-departments', methods=['GET'])
def manager_view_department():
    # Retrieve the department name from the session
    department_name = session.get('department')
    if not department_name:
        return jsonify({'error': 'Department not found in session'}), 403

    try:
        # Query the database to get all the employees in the department along with their roles
        employees_in_department = db.session.query(Employee, Role).join(Role).filter(Employee.DepartmentName == department_name).all()

        # Render the template and pass the employees data to it
        return render_template('Manager/manager-department.html', employees=employees_in_department)
    except Exception as e:
        # Handle any exceptions that might occur during database query
        return jsonify({'message': 'An error occurred while fetching employees.', 'error': str(e)}), 500

