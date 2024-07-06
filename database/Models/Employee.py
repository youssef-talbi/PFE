import json
import pickle
import numpy as np
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db


class Employee(db.Model):
    __tablename__ = 'employees'

    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), index=True, nullable=False)
    LastName = db.Column(db.String(50), index=True, nullable=False)
    Email = db.Column(db.String(100), index=True, nullable=False)
    Phone = db.Column(db.String(20), index=True, nullable=False)
    JobTitle = db.Column(db.String(100), index=True, nullable=False)
    DepartmentName = db.Column(db.String(100))
    RoleName = db.Column(db.String(100), db.ForeignKey('Roles.RoleName'))  # Foreign key relationship to Roles table
    LeaveBalance = db.Column(db.Integer, index=True, nullable=False)
    image_paths = db.Column(db.Text, nullable=True)
    face_encoding = db.Column(db.Text, nullable=True)

    attendances = db.relationship('Attendance', backref='employee', lazy=True)
    benefit_selections_ref = db.relationship('BenefitSelection', backref='employee', lazy=True)
    payroll = db.relationship('PayrollDetails', backref='employee', lazy=True, uselist=False)
    
    training_selection_ref = db.relationship('TrainingSelection', backref='employee', lazy=True)
    role = db.relationship('Role', backref='employee')  # Define the relationship
    leave_requests = db.relationship("LeaveRequests", backref="employee")  # Define the relationship    
    chats = db.relationship('Chat', backref='sender', lazy=True)
    audit_trial = db.relationship('AuditTrail', backref = 'employee', lazy = True)

    def to_json(self):
        """
        Convert the Employee object to a JSON-serializable dictionary.
        """
        return {
            'EmployeeID': self.EmployeeID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Phone': self.Phone,
            'JobTitle': self.JobTitle,
            'RoleName': self.RoleName,
            'DepartmentName': self.DepartmentName,
            'LeaveBalance': self.LeaveBalance,
            'image_paths': json.loads(self.image_paths) if self.image_paths else [],
            'face_encoding': json.loads(self.face_encoding)
        }
