from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, g
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from flask_login import current_user
from Employee import Employee
from LeaveRequest import LeaveRequests
from Department import Department
from flask_cors import CORS
# Blueprint for the leave request routes
leaverequest_routes = Blueprint('leaverequest_routes', __name__)
CORS(leaverequest_routes)




# Function to get the current employee's ID
def get_current_employee_id():
    """
    Retrieve the current employee's ID from the session.

    Returns:
        int: The ID of the current employee, or None if the ID is not in the session.

    Raises:
        RuntimeError: If the function is called outside of a request context.
    """
    try:
        return session.get('employee_id')
    except RuntimeError:
        # This exception is raised when the function is called outside of a request context.
        # We can safely ignore it here, since this function is not guaranteed to be called
        # within a request context.
        return None
    
# Route to display the leave request form and employee's own requests
@leaverequest_routes.route('/leave-requests', methods=['GET'])
def display_leave_request_form():
    employee_id = get_current_employee_id()  # Get the current employee's ID
    leave_requests = LeaveRequests.query.filter_by(EmployeeID=employee_id).all()
    return render_template('Regular-employee//submit_leave_requests.html', leaveRequests=leave_requests)

# Route to get all leave requests of the current employee
@leaverequest_routes.route('/view/leave-requests', methods=['GET'])
def get_all_leave_requests():
    leave_requests = LeaveRequests.query.all()
    if leave_requests:
        serialized_leave_requests = [leave_request.serialize() for leave_request in leave_requests]
    else:
        serialized_leave_requests = []
    return render_template('HR//leave-request.html', leave_requests=serialized_leave_requests)

# Route to get a leave request by ID and ensure it belongs to the current employee
@leaverequest_routes.route('/leave-requests/<int:RequestID>/<int:EmployeeID>', methods=['GET'])
def get_leave_request_by_id_employee(RequestID, EmployeeID):
    employee_id = get_current_employee_id()  # Get the current employee's ID
    if employee_id == EmployeeID:
        leave_request = LeaveRequests.query.filter_by(RequestID=RequestID, EmployeeID=employee_id).first()
        if leave_request:  
            return jsonify(leave_request.serialize())  
    return jsonify({'message': 'Leave Request not found or unauthorized'}), 404  

# Route to submit a leave request associated with the current employee
@leaverequest_routes.route('/leave-requests', methods=['POST'])
def submit_leave_request():
    employee_id = get_current_employee_id()  # Get the current employee's ID
    print (employee_id)
    if employee_id:
        data = request.get_json()
        required_fields = ['LeaveType', 'StartDate', 'EndDate']
        if all(field in data for field in required_fields):
            leave_request = LeaveRequests(
                EmployeeID=employee_id,
                LeaveType=data['LeaveType'],
                StartDate=data['StartDate'],
                EndDate=data['EndDate']
            )
            db.session.add(leave_request)
            db.session.commit()
            return jsonify(leave_request.serialize()), 201
        else:
            return jsonify({'error': 'Missing required fields: LeaveType, StartDate, EndDate'}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401


# Function to get the current department head's ID
def get_current_department_head_id():
    """
    Retrieve the current department head's ID from the session.

    Returns:
        int: The ID of the current department head, or None if the ID is not in the session.
    """
    try:
        return session.get('department.DepartmentHeadID')
    except RuntimeError:
        return None
print(get_current_department_head_id())

# Route to display the leave requests of employees belonging to the department managed by the current department head
@leaverequest_routes.route('/manager-leave-requests', methods=['GET', 'POST'])
def display_department_leave_requests():
    department_head_id = get_current_employee_id()
    if department_head_id:
        # Query the database to find the department managed by the current department head
        department = Department.query.filter_by(DepartmentHeadID=department_head_id).first()
        if department:
            # Find all employees in the department
            employees = Employee.query.filter_by(DepartmentName=department.DepartmentName).all()
            employee_ids = [employee.EmployeeID for employee in employees]

            if request.method == 'GET':
                # Find all leave requests submitted by employees in the department
                leave_requests = LeaveRequests.query.filter(LeaveRequests.EmployeeID.in_(employee_ids)).all()

                # Render the HTML template with leave requests data
                return render_template('Manager//manage-leave-request.html', leave_requests=leave_requests)
            elif request.method == 'POST':
                # Get the data from the form submission
                leave_request_id = request.form.get('leave_request_id')
                action = request.form.get('action')

                # Find the leave request in the database
                leave_request = LeaveRequests.query.get(leave_request_id)
                if leave_request and leave_request.EmployeeID in employee_ids:
                    # Update the status based on the action
                    if action == 'approve':
                        leave_request.Status = 'approved'
                    elif action == 'deny':
                        leave_request.Status = 'denied'

                    # Commit the changes to the database
                    db.session.commit()

                    # Redirect to the GET route to display updated leave requests
                    return redirect(url_for('leaverequest_routes.display_department_leave_requests'))

                else:
                    return jsonify({'message': 'Leave request not found or not in the department'}), 404
        else:
            return jsonify({'message': 'Department not found for the current department head'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401



# Route to get approved leave requests for the FullCalendar
@leaverequest_routes.route('/calendar/leave-requests', methods=['GET'])
def get_approved_leave_requests_for_calendar():
    approved_leave_requests = LeaveRequests.query.filter_by(Status='approved').all()
    serialized_approved_leave_requests = [{
        'title': f"{leave_request.employee.FirstName} {leave_request.employee.LastName}",
        'start': leave_request.StartDate.isoformat(),
        'end': leave_request.EndDate.isoformat(),
        'description': leave_request.Description,
    } for leave_request in approved_leave_requests]

    # Print the serialized data for debugging
    print(serialized_approved_leave_requests)

    return jsonify(serialized_approved_leave_requests)
