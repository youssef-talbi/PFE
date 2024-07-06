from flask import Blueprint, jsonify, render_template, session
import sys
from sqlalchemy import extract
from datetime import datetime
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Attendance import Attendance
from flask_cors import CORS
from Employee import Employee

attendance_bp = Blueprint('attendance', __name__)
CORS(attendance_bp)

# Route to get all attendance records for HR administrator
@attendance_bp.route('/manager-attendance', methods=['GET'])
def manager_view_attendance():
    employee_id = session.get('employee_id')
    
    if not employee_id:
        print("No employee ID in session")
        return "No employee ID in session", 400

    print(f"Session employee_id: {employee_id}")
    
    today = datetime.today().date()
    print(f"Today's date: {today}")

    
    
    # Debug prints
    print(f"Session employee_id: {employee_id}")
    print(f"Today's date: {today}")
    
    # Filter attendance records for the current day
    today_attendance = Attendance.query.filter(
        extract('year', Attendance.ClockInTime) == today.year,
        extract('month', Attendance.ClockInTime) == today.month,
        extract('day', Attendance.ClockInTime) == today.day
    ).all()

    if not today_attendance:
        print("No attendance records found for today")

    attendance_data = []
    for record in today_attendance:
        employee = Employee.query.filter_by(EmployeeID=record.EmployeeID).first()
        employee_name = '{} {}'.format(employee.FirstName, employee.LastName) if employee else 'Unknown'

        attendance_data.append({
            'Day': record.ClockInTime.strftime("%A"),
            'ClockInTime': record.ClockInTime.strftime("%H:%M"),
            'ClockOutTime': record.ClockOutTime.strftime("%H:%M") if record.ClockOutTime else 'Not Clocked Out',
            'EmployeeName': employee_name
        })

    print(f"Attendance data: {attendance_data}")
    return render_template('HR/view_attendance.html', attendance_data=attendance_data)
