import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from datetime import datetime
class TrainingPrograms(db.Model):
    __tablename__ = 'TrainingPrograms'

    ProgramID = db.Column(db.Integer, primary_key=True)
    ProgramName = db.Column(db.String(100))
    Trainer = db.Column(db.String(100))
    Schedule = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Status = db.Column(db.String(20))
    StartDate = db.Column(db.DateTime)
    EndDate = db.Column(db.DateTime)
    TrainingType = db.Column(db.String(30))
    Cost = db.Column(db.Numeric(10, 2))
    EnrolledEmployeesCount = db.Column(db.Integer, default=0)
    
    # Define relationship with TrainingSelection and enable cascading deletions
    training_selections = db.relationship(
        'TrainingSelection', 
        backref='training_program', 
        cascade="all, delete-orphan",
        overlaps="training_program"
    )
    
    def serialize(self):
        serialized_data = {
            'ProgramID': self.ProgramID,
            'ProgramName': self.ProgramName,
            'Trainer': self.Trainer,
            'Schedule': self.Schedule,
            'Description': self.Description,
            'Status': self.Status,
            'TrainingType': self.TrainingType,
            'Cost': self.Cost,
            'EnrolledEmployeesCount': self.EnrolledEmployeesCount
        }
        if self.StartDate:
            serialized_data['StartDate'] = self.StartDate.isoformat() if isinstance(self.StartDate, datetime) else self.StartDate
        if self.EndDate:
            serialized_data['EndDate'] = self.EndDate.isoformat() if isinstance(self.EndDate, datetime) else self.EndDate
        return serialized_data