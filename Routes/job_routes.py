import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Middleware')
from database import db
from Job import JobVacancy
from flask import jsonify, render_template,request, Blueprint
from flask_cors import CORS
from Authorization import auth_required, admin_required
job_bp = Blueprint('job', __name__)
CORS(job_bp)
# Endpoint to retrieve all job vacancies

@job_bp.route('/job-vacancies', methods=['GET'])
def get_all_job_vacancies():
    job_vacancies = JobVacancy.query.all()
    serialized_job_vacancies = [job_vacancy.serialize() for job_vacancy in job_vacancies]
    
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(serialized_job_vacancies)
    else:
        return render_template('HR/jobs.html', job_vacancies=serialized_job_vacancies)

# Endpoint to create a new job vacancy
@job_bp.route('/job-vacancies', methods=['POST'])
@auth_required  # Assuming you have an auth_required decorator for authentication
@admin_required # Assuming you have an admin_required decorator for authorization
def create_job_vacancy():
    data = request.json
    # Validate input data (e.g., using marshmallow)

    job_vacancy = JobVacancy(**data) 
    db.session.add(job_vacancy)
    db.session.commit()
    return jsonify(job_vacancy.serialize()), 201

# Endpoint to update an existing job vacancy
@job_bp.route('/job-vacancies/<int:id>', methods=['PUT'])
@auth_required
@admin_required
def update_job_vacancy(id):
    data = request.json
    # Validate input data

    job_vacancy = JobVacancy.query.get_or_404(id)
    # Update attributes from validated data
    for key, value in data.items():
        setattr(job_vacancy, key, value)

    db.session.commit()
    return jsonify(job_vacancy.serialize())

# Endpoint to delete a job vacancy
@job_bp.route('/job-vacancies/<int:id>', methods=['DELETE'])
@auth_required
@admin_required
def delete_job_vacancy(id):
    job_vacancy = JobVacancy.query.get_or_404(id)
    db.session.delete(job_vacancy)
    db.session.commit()
    return jsonify(None), 204


@job_bp.route('/job-vacancies/<int:id>', methods=['GET'])
def get_job_vacancy(id):
    job_vacancy = JobVacancy.query.get_or_404(id)
    return jsonify(job_vacancy.serialize())


@job_bp.route('/apply', methods=['GET'])
def get_all_job_vacancies_to_apply():
    job_vacancies = JobVacancy.query.all()
    serialized_job_vacancies = [job_vacancy.serialize() for job_vacancy in job_vacancies]
    
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(serialized_job_vacancies)
    else:
        return render_template('apply.html', job_vacancies=serialized_job_vacancies)
