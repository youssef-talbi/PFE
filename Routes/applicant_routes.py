import os
import sys
from werkzeug.utils import secure_filename
from flask import render_template, jsonify, request, Blueprint, current_app
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
import Applicant
from Applicant import Applicant
from Job import JobVacancy
from flask import app, jsonify,request, Blueprint
from flask_cors import CORS


applicant_bp = Blueprint('applicant', __name__)
CORS(applicant_bp)

@applicant_bp.route('/apply', methods=['POST'])
def submit_application():
    name = request.form['name']
    email = request.form['email']
    resume = request.files['resume']
    
    if not resume:
        return jsonify({'message': 'Resume file is required.'}), 400

    filename = secure_filename(resume.filename)
    resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    resume.save(resume_path)

    new_applicant = Applicant(
        name=name,
        email=email,
        resume_path=filename  # Save only the filename
    )

    db.session.add(new_applicant)
    db.session.commit()
    return jsonify({'message': 'Application submitted successfully.'})

@applicant_bp.route('/apply')
def index():
    job_vacancies = JobVacancy.query.all()
    return render_template('apply.html', job_vacancies=job_vacancies)