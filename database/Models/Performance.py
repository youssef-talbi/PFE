import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Department import Department
from Employee import Employee
class PerformanceGoal(db.Model):
    __tablename__ = 'PerformanceGoals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    kpi = db.Column(db.String(255), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.DepartmentID'), nullable=True)

    employee = db.relationship('Employee', backref='performance_goals')
    department = db.relationship('Department', backref='performance_goals')

    def to_dict(self):
        employee_name_department = None
        if self.employee:
            employee_name_department = f"{self.employee.FirstName} {self.employee.LastName} ({self.employee.DepartmentName})"
        elif self.department:
            employee_name_department = self.department.DepartmentName

        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'kpi': self.kpi,
            'target_date': self.target_date.strftime('%Y-%m-%d'),
            'employee_name_department': employee_name_department
        }


