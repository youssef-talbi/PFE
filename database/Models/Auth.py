import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from passwordhash import hash_password, verify_password
class Auth(db.Model):
    __tablename__ = 'auth'

    UserID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'), primary_key=True)
    PasswordHash = db.Column(db.String(128))

    def set_password(self, password):
        """Hash the password and set the PasswordHash attribute."""
        self.PasswordHash = hash_password(password)

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return verify_password(password, self.PasswordHash)