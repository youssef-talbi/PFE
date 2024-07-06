import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.DepartmentID'))  

    chats = db.relationship('Chat', back_populates='channel')
    department = db.relationship('Department', backref=db.backref('channels', lazy=True))

    