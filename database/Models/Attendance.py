from email.policy import default
import sys
from sqlalchemy import DateTime
from datetime import datetime
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
class Attendance(db.Model):
    __tablename__ = 'Attendance'

    AttendanceID = db.Column(db.String(30), primary_key=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))
    ClockInTime = db.Column(db.DateTime)
    ClockOutTime = db.Column(db.DateTime, nullable=True)
    #ShiftStart = db.Column(db.Time, nullable = False)
    #ShiftEnd = db.Column(db.Time, nullable = False)
    
    def serialize (self):
        return {
            'AttendanceID': self.AttendanceID,
            'EmployeeID': self.EmployeeID,
            'ClockInTime': self.ClockInTime,
            'ClockOutTime': self.ClockOutTime
            #'ShiftStart' : self.ShiftStart,
            #'ShiftEnd' : self.ShiftEnd,
        }
        