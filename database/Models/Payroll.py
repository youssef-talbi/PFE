import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db

class PayrollDetails(db.Model):
    __tablename__ = 'PayrollDetails'
    PayrollID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))
    Month = db.Column(db.Integer)
    Year = db.Column(db.Integer)
    SalaryDetails = db.Column(db.Numeric(10, 2))