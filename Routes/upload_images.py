from fileinput import filename
import mimetypes
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from Employee import Employee
from database import db
from PIL import Image
import os
from flask import request, send_from_directory,Blueprint
from werkzeug.utils import secure_filename
upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload-image', methods=['POST'])
def upload_image(employee_name):
    pic = request.files['pic']
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Image(Employee.Image.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()
    return 'Image uploaded successfully', 200