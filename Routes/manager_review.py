import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from LeaveRequest import LeaveRequests
from Employee import Employee
from flask import Blueprint, jsonify, request
from flask_cors import CORS
leave_requests = Blueprint('leave_requests', __name__)
CORS(leave_requests)

@leave_requests.route('/manager/leave-requests', methods=['GET'])
def manager_get_all_leave_requests():
    """
    Get all leave requests from the database and return them as a JSON response.
    This route is intended for managers to review leave requests.
    """
    leave_requests = LeaveRequests.query.all()
    result = [leave_request.__repr__() for leave_request in leave_requests]
    return jsonify(result)

@leave_requests.route('/manager/leave-requests/<int:RequestID>', methods=['PUT'])
def manager_review_leave_request(RequestID):
    """
    Update the status of a leave request (approve or reject).
    This route is intended for managers to approve or reject leave requests.
    """
    data = request.get_json()
    leave_request = LeaveRequests.query.get(RequestID)

    if leave_request:
        status = data.get('Status')
        comment = data.get('Comment')

        if status is not None:
            leave_request.Status = status
        if comment is not None:
            leave_request.Comment = comment

        db.session.commit()
        return jsonify(leave_request.__repr__()), 200
    else:
        return jsonify({'message': 'Leave Request not found'}), 404
    