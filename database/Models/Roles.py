import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db



class Role(db.Model):
    __tablename__ = 'Roles'

    RoleID = db.Column(db.Integer)
    RoleName = db.Column(db.String(100), primary_key=True)
    Description = db.Column(db.Text)
   
    def to_json(self):
        return {
            'RoleID': self.RoleID,
            'RoleName': self.RoleName,
            'Description': self.Description
        }

