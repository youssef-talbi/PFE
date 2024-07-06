from flask import Blueprint, jsonify, request
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Employee import Employee
from AuditTrail import AuditTrail
from flask_cors import CORS
audit_trail_bp = Blueprint('audit_trail', __name__)

# Route to get all audit trail records
@audit_trail_bp.route('/audit-trail', methods=['GET'])
def get_all_audit_trail_records():
    audit_trail_records = AuditTrail.query.all()
    serialized_records = [{
        'AuditTrailID': record.AuditTrailID,
        'EmployeeID': record.EmployeeID,
        'ActionType': record.ActionType,
        'Timestamp': record.Timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for record in audit_trail_records]
    return jsonify(serialized_records)

# Route to get audit trail records by employee ID
@audit_trail_bp.route('/audit-trail/<int:employee_id>', methods=['GET'])
def get_audit_trail_records_by_employee_id(employee_id):
    audit_trail_records = AuditTrail.query.filter_by(EmployeeID=employee_id).all()
    if not audit_trail_records:
        return jsonify({'message': 'No audit trail records found for the specified employee ID'}), 404
    serialized_records = [{
        'AuditTrailID': record.AuditTrailID,
        'EmployeeID': record.EmployeeID,
        'ActionType': record.ActionType,
        'Timestamp': record.Timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for record in audit_trail_records]
    return jsonify(serialized_records)

# Route to get audit trail records by action type
@audit_trail_bp.route('/audit-trail/action/<action_type>', methods=['GET'])
def get_audit_trail_records_by_action_type(action_type):
    audit_trail_records = AuditTrail.query.filter_by(ActionType=action_type).all()
    if not audit_trail_records:
        return jsonify({'message': 'No audit trail records found for the specified action type'}), 404
    serialized_records = [{
        'AuditTrailID': record.AuditTrailID,
        'EmployeeID': record.EmployeeID,
        'ActionType': record.ActionType,
        'Timestamp': record.Timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for record in audit_trail_records]
    return jsonify(serialized_records)