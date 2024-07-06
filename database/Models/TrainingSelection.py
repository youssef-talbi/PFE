from datetime import datetime
import sys

sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from Training import TrainingPrograms
from Employee import Employee
from database import db
from datetime import datetime
class TrainingSelection(db.Model):
    __tablename__ = 'TrainingSelection'

    SelectionID = db.Column(db.Integer, primary_key=True)
    ProgramID = db.Column(db.Integer, db.ForeignKey('TrainingPrograms.ProgramID'), nullable=False)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), nullable=False)
    SelectionDate = db.Column(db.DateTime, default=datetime.utcnow)

    # Define back reference to TrainingPrograms
    program = db.relationship('TrainingPrograms', back_populates='training_selections', overlaps="training_program")


    
    def serialize(self):
        return {
            'SelectionID': self.SelectionID,
            'ProgramName': self.ProgramID,
            'EmployeeID': self.EmployeeID,
            'SelectionDate': self.SelectionDate,
        }