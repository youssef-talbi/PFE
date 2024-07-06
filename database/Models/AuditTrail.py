from datetime import datetime
from sqlalchemy import event
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db


class AuditTrail(db.Model):
    __tablename__ = 'audit_trail'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    role_name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(200), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'role_name': self.role_name,
            'details': self.details,
            'target_id': self.target_id
        }