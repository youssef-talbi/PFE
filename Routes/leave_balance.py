from flask import Blueprint, jsonify
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Employee import Employee

leave_balance_routes = Blueprint('leave_balance_routes', __name__)

@leave_balance_routes.route('/employees/<int:employee_id>/leave-balances', methods=['GET'])
def get_leave_balances(employee_id):
    """
    Get leave balances for a specific employee.
    """
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify({
        'EmployeeID': employee.EmployeeID,
        'FirstName': employee.FirstName,
        'LastName': employee.LastName,
        'VacationBalance': employee.VacationBalance,
        'SickLeaveBalance': employee.SickLeaveBalance
    })
