
from datetime import datetime
import os
from flask import Blueprint, jsonify, request,render_template
import json
import sys
from werkzeug.utils import secure_filename
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from Department import Department
from Performance import PerformanceGoal
from database import db
from Employee import Employee

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/performance/goals', methods=['POST'])
def set_performance_goals():
    data = request.json
    goal = PerformanceGoal(
        title=data['title'],
        description=data['description'],
        kpi=data['kpi'],
        target_date=data['target_date'],
        employee_id=data['employee_id']
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify({'message': 'Performance goal set successfully'}), 201

@performance_bp.route('/performance/goals/department', methods=['POST'])
def create_department_goal():
    data = request.get_json()
    department_id = data.get('department_id')
    new_goal = PerformanceGoal(
        title=data.get('title'),
        description=data.get('description'),
        kpi=data.get('kpi'),
        target_date=datetime.strptime(data.get('target_date'), '%Y-%m-%d'),
        department_id=department_id
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"message": "Department goal created successfully"}), 201


@performance_bp.route('/performance/goals', methods=['GET'])
def performance_goals():
    employees = Employee.query.filter_by(RoleName='Regular Employee').all()
    departments = Department.query.all()
    return render_template('HR/performance_goals.html', employees=employees, departments=departments)


@performance_bp.route('/performance/goals/all', methods=['GET'])
def get_performance_goals():
    goals = PerformanceGoal.query.all()
    return jsonify([goal.to_dict() for goal in goals]), 200

@performance_bp.route('/performance/goals/<int:employee_id>', methods=['GET'])
def get_employee_goals(employee_id):
    goals = PerformanceGoal.query.filter_by(employee_id=employee_id).all()
    return jsonify([goal.to_dict() for goal in goals]), 200

@performance_bp.route('/employees', methods=['GET'])
def get_regular_employees():
    employees = Employee.query.filter_by(RoleName='Regular Employee').all()
    employee_list = [{"id": e.EmployeeID, "name": f"{e.FirstName} {e.LastName} ({e.DepartmentName})"} for e in employees]
    return jsonify(employee_list)

@performance_bp.route('/performance/goals/all', methods=['GET'])
def get_all_performance_goals():
    goals = PerformanceGoal.query.all()
    return jsonify([goal.to_dict() for goal in goals]), 200

@performance_bp.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    department_list = [{"DepartmentID": d.DepartmentID, "DepartmentName": d.DepartmentName} for d in departments]
    return jsonify(department_list)

