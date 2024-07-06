import os
from flask import Blueprint, jsonify, request,render_template
import json
import sys
from werkzeug.utils import secure_filename

from LeaveRequest import LeaveRequests
from Payroll import PayrollDetails
from Performance import PerformanceGoal
from TrainingSelection import TrainingSelection
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from BenefitSelection import BenefitSelection
from auth import Auth
from database import db
from Employee import Employee
from Roles import Role
from Attendance import Attendance
from Chat import Chat
from datetime import datetime
from flask_cors import CORS
from Department import Department

from face_encoder import *
# Creating a blueprint for the employee module
employee_bp = Blueprint('employee', __name__)
# Enabling CORS for the benefit programs routes
CORS (employee_bp)



# Route to get all employees
@employee_bp.route('/employees', methods=['GET'])
def get_all_employees():
    try:
        # Querying the database to get all employees
        employees = db.session.query(Employee).all()
        # Render the employees HTML template and pass the list of employees
        return render_template('HR//Employee.html', employees=employees)
    except Exception as e:
        # Handle any exceptions that might occur during database query
        return jsonify({'message': 'An error occurred while fetching employees.', 'error': str(e)}), 500
# Route to get an employee by ID
@employee_bp.route('/employees/<employee_id>', methods=['GET'])
def get_employee_by_id(employee_id):
    """
    This route retrieves an employee from the database by their ID and returns them as a JSON response.
    """
    # Querying the database to get an employee by ID
    employee = Employee.query.get(employee_id)
    # If the employee is found, return it as a JSON response
    if employee:
        return jsonify(employee.to_json())
    # If the employee is not found, return an error message with a 404 status code
    return jsonify({'message': 'Employee not found'}), 404

# Route to get an employee by name
# Route to get an employee by name
@employee_bp.route('/employees/name/<employee_name>', methods=['GET'])
def get_employee_by_name(employee_name):
    """
    This route retrieves an employee from the database by their name and returns them as a JSON response.
    """
    # Querying the database to get an employee by name
    employee = Employee.query.filter_by(FirstName=employee_name).first()
    # If the employee is found, return it as a JSON response
    if employee:
        return jsonify(employee.to_json())
    # If the employee is not found, return an error message with a 404 status code
    return jsonify({'message': 'Employee not found'}), 404


BASE_DIRECTORY = "C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Faces"  # Base directory for storing images

@employee_bp.route('/employees', methods=['POST'])
def add_employee():
    try:
        data_list = json.loads(request.form['data'])
        if not isinstance(data_list, list):
            return jsonify({'message': 'Invalid data format. Expected a list of employee data.'}), 400

        if 'images' not in request.files:
            return jsonify({'message': 'No image files provided.'}), 400

        new_employees = []

        for data in data_list:
            role_name = data.pop('RoleName', None)
            if not role_name:
                return jsonify({'error': 'Role name is required for employee assignment'}), 400

            role = Role.query.filter_by(RoleName=role_name).first()
            if not role:
                return jsonify({'error': 'Role not found'}), 404

            if role_name.lower() == 'hr administrator':
                department_name = 'HR Department'
            else:
                department_name = data.get('DepartmentName')
                if department_name:
                    department = Department.query.filter_by(DepartmentName=department_name).first()
                    if not department:
                        department = Department(DepartmentName=department_name)
                        department.Description = "Default description"
                        db.session.add(department)
                        db.session.flush()

            new_employee = Employee(**data)
            if role_name.lower() == 'department head' and department_name:
                department.set_department_head(new_employee)
                department.department_head = new_employee
                db.session.flush()

            new_employee.role = role
            new_employee.DepartmentName = department_name

            employee_folder = os.path.join(BASE_DIRECTORY, f"{new_employee.FirstName}_{new_employee.LastName}")
            if not os.path.exists(employee_folder):
                os.makedirs(employee_folder)
            image_files = request.files.getlist('images')
            image_paths = []
            for image_file in image_files:
                if image_file and image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    file_path = os.path.join(employee_folder, filename)
                    image_file.save(file_path)
                    image_paths.append(file_path)

            new_employee.image_paths = json.dumps(image_paths)

            db.session.add(new_employee)
            db.session.flush()

            default_password = role_name.lower().replace(' ', '') + '123'
            auth_entry = Auth(UserID=new_employee.EmployeeID)
            auth_entry.set_password(default_password)
            db.session.add(auth_entry)

            new_employees.append(new_employee)

            # Encode faces after saving employee and images
            try:
                face_encoding = update_face(new_employee.EmployeeID, json.dumps(image_paths)) #update_face returns a json serialized list of lists
                new_employee.face_encoding = face_encoding  # store as json
                db.session.commit()
            except Exception as e:
                print(f"Error encoding faces for employee {new_employee.EmployeeID}: {e}")

            print(f'Generated password for {new_employee.FirstName} {new_employee.LastName}: {default_password}')

        return jsonify([employee.to_json() for employee in new_employees]), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding employees.', 'error': str(e)}), 500


@employee_bp.route('/manage/employees/<employee_id>', methods=['PUT'])
def manager_update_employee(employee_id):
    data = request.form

    try:
        # Query the database to get the employee by ID
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        # Check if the provided department exists in the department table
        department_name = data.get('DepartmentName')
        if department_name:
            department = Department.query.filter_by(DepartmentName=department_name).first()
            if not department:
                # Create a new department since it doesn't exist
                department = Department(DepartmentName=department_name)
                department.Description = "Default description"  # Add default description
                db.session.add(department)
                db.session.flush()  # Flush to generate DepartmentID
            employee.DepartmentName = department_name

        # Update employee data, only update fields if new value is provided
        for key, value in data.items():
            if value:  # Update only if the value is provided
                setattr(employee, key, value)

        # Handle image uploads
        if 'images' in request.files:
            images = request.files.getlist('images')
            image_paths = json.loads(employee.image_paths) if employee.image_paths else []
            for image in images:
                if image:
                    # Save the image to the file system and store the path in image_paths
                    filename = secure_filename(image.filename)
                    image.save(os.path.join('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Faces', filename))
                    image_paths.append(filename)

            if image_paths:
                employee.image_paths = json.dumps(image_paths)

        db.session.commit()
        return jsonify(employee.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update employee', 'error': str(e)}), 500



    

# Route to search for employees by name
@employee_bp.route('/employees/search/<search_term>', methods=['GET'])
def search_employees(search_term):
    """
    This route searches for employees by name and returns a list of matching employees as a JSON response.
    """
    try:
        # Querying the database to get employees whose first name or last name contains the search term
        employees = Employee.query.filter((Employee.FirstName.like(f'%{search_term}%')) | (Employee.LastName.like(f'%{search_term}%'))).all()
        # Convert the list of employees to JSON format
        return jsonify([employee.to_json() for employee in employees])
    except Exception as e:
        # Handle any exceptions that might occur during database query
        return jsonify({'message': 'An error occurred while searching for employees.', 'error': str(e)}), 500
    
@employee_bp.route('/manage/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        # Query the database to get the employee by ID
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        
        # Check if the employee is a department head
        if employee.DepartmentName:
            department = Department.query.filter_by(DepartmentName=employee.DepartmentName).first()
            if department and department.DepartmentHeadID == employee.EmployeeID:
                department.DepartmentHeadID = None
                department.DepartmentHeadName = None
                db.session.add(department)
        
        
        # Delete related records
        Attendance.query.filter_by(EmployeeID=employee.EmployeeID).delete()
        BenefitSelection.query.filter_by(EmployeeID=employee.EmployeeID).delete()
        PayrollDetails.query.filter_by(EmployeeID=employee.EmployeeID).delete()
        PerformanceGoal.query.filter_by(employee_id=employee.EmployeeID).delete()
        TrainingSelection.query.filter_by(EmployeeID=employee.EmployeeID).delete()
        LeaveRequests.query.filter_by(EmployeeID=employee.EmployeeID).delete()
        Chat.query.filter_by(sender_id=employee.EmployeeID).delete()
        Auth.query.filter_by(UserID=employee.EmployeeID).delete()

        # Delete the employee
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete employee', 'error': str(e)}), 500
