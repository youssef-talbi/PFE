import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db

class LeaveRequests(db.Model):
    __tablename__ = 'LeaveRequests'
    RequestID = db.Column(db.Integer, primary_key=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))
    LeaveType = db.Column(db.String(100))
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    Description = db.Column(db.Text)
    Status = db.Column(db.String(50), default='Pending')
    
    
    def serialize(self):
        return {
            'RequestID': self.RequestID,
            'EmployeeID': self.EmployeeID,
            'LeaveType': self.LeaveType,
            'StartDate': self.StartDate.isoformat() if self.StartDate else None,
            'EndDate': self.EndDate.isoformat() if self.EndDate else None,
            'Description': self.Description,
            'Status': self.Status,
            'employee': {
                'FirstName': self.employee.FirstName,
                'LastName': self.employee.LastName
            }
        }