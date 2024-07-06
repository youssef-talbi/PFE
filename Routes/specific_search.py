from flask import Blueprint, jsonify, request
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
import Employee
from Employee import Employee
from flask_cors import CORS
from Department import Department
from Roles import Role
specific_search_bp = Blueprint('specific_search', __name__, url_prefix='/api')
CORS(specific_search_bp)

@specific_search_bp.route('/employees', methods=['GET'])
def specific_search():
    department = request.args.get('department')
    role = request.args.get('role')
    gender = request.args.get('gender')
    min_age = request.args.get('min_age')
    max_age = request.args.get('max_age')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    rating = request.args.get('rating')
    skill = request.args.get('skill')
    location = request.args.get('location')
    manager = request.args.get('manager')

    criteria = []
    if department:
        criteria.append(db.func.lower(Employee.department.has(Department.DepartmentName == department)).label('department_match'))
    if role:
        criteria.append(db.func.lower(Employee.role.has(Role.RoleName == role)).label('role_match'))
    if gender:
        criteria.append(db.func.lower(Employee.gender) == db.func.lower(gender))
    if min_age and max_age:
        criteria.append(db.extract('year', Employee.birth_date) >= min_age)
        criteria.append(db.extract('year', Employee.birth_date) <= max_age)
    if start_date and end_date:
        criteria.append(Employee.created_at >= start_date)
        criteria.append(Employee.created_at <= end_date)
    if rating:
        criteria.append(db.func.lower(Employee.rating) == db.func.lower(rating))
    if skill:
        criteria.append(db.func.lower(Employee.skills).contains(db.func.lower(skill)))
    if location:
        criteria.append(db.func.lower(Employee.location) == db.func.lower(location))
    if manager:
        criteria.append(db.func.lower(Employee.manager.has(Employee.first_name + ' ' + Employee.last_name)) == db.func.lower(manager))

    employees = Employee.query.filter(*criteria).all()

    employees_list = [employee.to_json() for employee in employees]

    return jsonify(employees_list)

