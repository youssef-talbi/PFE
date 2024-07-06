import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')

from database import db




class Department(db.Model):
    __tablename__ = 'departments'

    DepartmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DepartmentName = db.Column(db.String(100))
    Description = db.Column(db.Text)
    DepartmentHeadID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))
    DepartmentHeadName = db.Column(db.String(100))  # New attribute for department head's name

    # Define the relationship between Department and Employee
    department_head = db.relationship('Employee', backref='department', lazy=True)
    

    def set_department_head(self, employee):
        """
        Set the department head for the department and update the department head's name.
        """
        self.DepartmentHeadID = employee.EmployeeID
        self.DepartmentHeadName = f"{employee.FirstName} {employee.LastName}"
        db.session.commit()

    def to_json(self):
        """
        Convert the Department object to a JSON-serializable dictionary.
        """
        return {
            'DepartmentID': self.DepartmentID,
            'DepartmentName': self.DepartmentName,
            'Description': self.Description,
            'DepartmentHeadID': self.DepartmentHeadID,
            'DepartmentHeadName': self.DepartmentHeadName
        }


