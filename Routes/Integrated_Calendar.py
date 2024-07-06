import json
from flask import Blueprint, blueprints, jsonify, redirect,render_template, session, url_for
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from LeaveRequest import LeaveRequests
from Employee import Employee
from flask_cors import CORS
import datetime
from Training import TrainingPrograms

calendar_bp = Blueprint('calendar', __name__)
CORS(calendar_bp)
@calendar_bp.route('/calendar/events')
def calendar_events():
    if 'employee_id' not in session:
        return redirect(url_for('auth.login'))

    employee_id = session['employee_id']
    employee = Employee.query.get(employee_id)
    # Fetch approved leave requests
    approved_leaves = LeaveRequests.query.filter_by(Status='approved').all()

    # Fetch training programs
    training_programs = TrainingPrograms.query.all()

    # Prepare data for the calendar
    events = []

    # Format leave requests
    for leave_request in approved_leaves:
        event = {
            'title': f"{leave_request.employee.FirstName} {leave_request.employee.LastName} ({leave_request.LeaveType})",
            'start': leave_request.StartDate.isoformat(),
            'end': (leave_request.EndDate + datetime.timedelta(days=1)).isoformat(),  # Add one day to end date
            'color': 'green',  # Customize color as needed
        }
        events.append(event)

    # Format training programs
    for training_program in training_programs:
        event = {
            'title': training_program.ProgramName,
            'start': training_program.StartDate.isoformat(),
            'end': (training_program.EndDate + datetime.timedelta(days=1)).isoformat(),  # Add one day to end date
            'color': 'blue',  # Customize color as needed
        }
        events.append(event)

    # Render the template with events data
    return render_template('HR/calendar.html', events=json.dumps(events),employee=employee)