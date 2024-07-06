
from datetime import datetime
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
# Define Applicant model
class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    resume_path = db.Column(db.String(200), nullable=False)  # Store the file path
    status = db.Column(db.String(100), default="submitted", nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'resume_path': self.resume_path,  # Return the file path
            'status': self.status,
            'submission_date': self.submission_date,
        }