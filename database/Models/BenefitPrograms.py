import sys

sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db


class BenefitPrograms(db.Model):
    __tablename__ = 'BenefitPrograms'
    ProgramID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProgramName = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.Text)
    EnrolledEmployeesCount = db.Column(db.Integer, default=0)  # Add this field

    def serialize(self):
        return {
            'ProgramID': self.ProgramID,
            'ProgramName': self.ProgramName,
            'Description': self.Description,
            'EnrolledEmployeesCount': self.EnrolledEmployeesCount  # Include enrolled employees count
            # Add more attributes if needed
        }
