from datetime import datetime
from flask import g, render_template, request, Blueprint, jsonify, session, redirect, url_for
from flask_cors import CORS
import sys


sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from sqlalchemy.orm import joinedload
from Chat import Chat
from Employee import Employee
from Channel import Channel
from Department import Department

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    if 'employee_id' not in session:
        return redirect(url_for('auth.login'))

    employee_id = session['employee_id']
    employee = Employee.query.get(employee_id)

    if employee.RoleName.lower() == 'hr administrator':
        departments = Department.query.all()
    else:
        departments = Department.query.filter_by(DepartmentName=employee.DepartmentName).all()
    
    departments_data = [department.to_json() for department in departments]

    return render_template('messages/chat.html', departments=departments_data, employee=employee)

@chat_bp.route('/chat/get_channels/<department_identifier>')
def get_channels(department_identifier):
    employee_id = session.get('employee_id')
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Unauthorized access'}), 401

    # Restrict access to channels based on role
    if employee.RoleName.lower() != 'hr administrator' and employee.DepartmentName != department_identifier:
        return jsonify({'error': 'Forbidden'}), 403

    # Determine if department_identifier is an ID or a name
    if department_identifier.isdigit():
        department_id = int(department_identifier)
        channels = Channel.query.filter_by(department_id=department_id).all()
    else:
        department = Department.query.filter_by(DepartmentName=department_identifier).first()
        if not department:
            return jsonify({'error': 'Department not found'}), 404
        channels = Channel.query.filter_by(department_id=department.DepartmentID).all()

    return jsonify([{'id': channel.id, 'name': channel.name} for channel in channels])


@chat_bp.route('/chat/get_messages/<int:channel_id>')
def get_messages(channel_id):
    messages = Chat.query.filter_by(channel_id=channel_id).order_by(Chat.timestamp).all()
    messages_data = [
        {
            'username': f"{message.sender.FirstName} {message.sender.LastName}",
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]
    return jsonify({'success': True, 'messages': messages_data})

@chat_bp.route('/chat/create_channel', methods=['POST'])
def create_channel():
    data = request.json
    channel_name = data.get('channelName')
    department_id = data.get('departmentId')
    if channel_name and department_id:
        new_channel = Channel(name=channel_name, department_id=department_id)
        db.session.add(new_channel)
        db.session.commit()
        return jsonify({'success': True, 'channel_id': new_channel.id})
    return jsonify({'success': False}), 400

