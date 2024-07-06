from datetime import datetime
import sys

sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from BenefitPrograms import BenefitPrograms
from database import db
from sqlalchemy import DateTime
class BenefitSelection(db.Model):
    __tablename__ = 'BenefitSelections'
    SelectionID = db.Column(db.Integer, primary_key=True, autoincrement = True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))
    ProgramID = db.Column(db.Integer, db.ForeignKey('BenefitPrograms.ProgramID'))
    SelectDate = db.Column(DateTime, default=datetime.now)
    

    
    program = db.relationship('BenefitPrograms', backref='benefit_selections')

    def serialize(self):
        return {
            'SelectionID': self.SelectionID,
            'EmployeeID': self.EmployeeID,
            'ProgramID': self.ProgramID,
            'SelectDate': self.SelectDate,
            
        }