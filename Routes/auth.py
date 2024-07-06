
from flask import Blueprint, jsonify, request,render_template
from flask import redirect, url_for
from flask_restful import abort
import jwt
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from flask import g,session
from database import db
from Roles import Role
from datetime import datetime, timedelta
from Employee import Employee
from Auth import Auth
from flask_cors import CORS
from passwordhash import hash_password, verify_password
# Secret key for token generation
SECRET_KEY = 'mysecretkey'

# Blueprint for authentication route
auth = Blueprint('auth', __name__)
CORS(auth)


    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.form

            # Super admin login
            if data['email'] == 'admin@example.com' and data['password'] == 'admin123':
                session['role_name'] = 'super_admin'
                return render_template('admin/superHR.html')  # Render super admin dashboard
            
            # Employee login
            employee = Employee.query.filter_by(Email=data['email']).first()
            if not employee:
                return jsonify({'message': 'Employee not found'}), 404

            auth_entry = Auth.query.filter_by(UserID=employee.EmployeeID).first()
            if not auth_entry:
                return jsonify({'message': 'Authentication details not found'}), 404

            if not verify_password(data['password'], auth_entry.PasswordHash.encode('utf-8')):
                return jsonify({'message': 'Invalid Password'}), 401

            session['employee_id'] = employee.EmployeeID
            session['role_name'] = employee.RoleName
            session['user_name'] = f"{employee.FirstName} {employee.LastName}"
            session['department'] = employee.DepartmentName
            print(session)
            
            # Debug prints for session values
            print(f"Logged in employee_id: {session['employee_id']}")
            print(f"Logged in role_name: {session['role_name']}")
            
            employee_role = employee.RoleName.lower()
            if employee_role == 'hr administrator':
                return redirect(url_for('auth.hr_profile', employee_id=employee.EmployeeID))
            elif employee_role == 'manager':
                return redirect(url_for('auth.manager_profile', employee_id=employee.EmployeeID))
            elif employee_role == 'regular employee':
                return redirect(url_for('auth.employee_profile', employee_id=employee.EmployeeID))
            elif employee_role == 'department head':
                return redirect(url_for('auth.manager_profile', employee_id=employee.EmployeeID))
            else:
                return jsonify({'message': 'Invalid Role Name'}), 400

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('login.html')



@auth.route('/profile/hr/', methods=['GET'])
@auth.route('/profile/hr/<int:employee_id>', methods=['GET'])
def hr_profile(employee_id=None):
    if employee_id is None:
        employee_id = session.get('employee_id') 
    employee = Employee.query.get_or_404(employee_id)
    role = Role.query.filter_by(RoleName=employee.RoleName.lower()).first()
    return render_template('HR/hr-profile.html', employee=employee, role=role)

@auth.route('/profile/manager/', methods=['GET'])
@auth.route('/profile/manager/<int:employee_id>', methods=['GET'])
def manager_profile(employee_id=None):
    if employee_id is None :
        employee_id = session.get('employee_id')
    # Query the database to get the manager's profile based on employee_id
    employee = Employee.query.get_or_404(employee_id)
    role = Role.query.filter_by(RoleName=employee.RoleName.lower()).first()  # Query the role based on RoleName
    return render_template('Manager/manager-profile.html', employee=employee, role=role)

@auth.route('/profile/employee/', methods=['GET'])
@auth.route('/profile/employee/<int:employee_id>', methods=['GET'])
def employee_profile(employee_id):
    # Query the database to get the employee's profile based on employee_id
    employee = Employee.query.get_or_404(employee_id)
    role = Role.query.filter_by(RoleName=employee.RoleName.lower()).first()  # Query the role based on RoleName
    return render_template('Regular-employee/employee-profile.html', employee=employee, role=role)


@auth.route('/profile/employee/<int:employee_id>')
def view_employee_profile(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        abort(404)
    return render_template('Regular-employee/employee-profile.html', employee=employee)

# Function for generating a token
def generate_token(EmployeeID):
    # Payload for the token containing the employee ID and expiration time
    payload = {
        'EmployeeID': EmployeeID,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    # Encoding the payload to a token using the secret key
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@auth.route('/logout')
def logout():
    session.clear()  # This clears all the session data
    return redirect(url_for('auth.login'))  # Redirect to the login page