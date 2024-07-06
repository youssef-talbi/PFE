import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
class PerformanceReview(db.Model):
    
    __tablename__ = 'performancereview'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'manager_id': self.manager_id,
            'scheduled_date': self.scheduled_date,
            'feedback': self.feedback,
            'rating': self.rating
        }
