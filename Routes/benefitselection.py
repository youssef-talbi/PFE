from flask import session
from flask import Blueprint, jsonify, redirect, request,render_template
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from BenefitPrograms import BenefitPrograms
from flask_login import current_user
from BenefitSelection import BenefitSelection
from flask_cors import CORS
selection_bp = Blueprint('selection', __name__)
CORS(selection_bp)



@selection_bp.route('/view_benefits')
def view_benefits():
    benefit_programs = BenefitPrograms.query.all()
    return render_template('Regular-employee/view-benefits.html', benefit_programs=benefit_programs)

@selection_bp.route('/enroll/<int:program_id>', methods=['POST', 'DELETE'])

def enroll(program_id):
    if request.method == 'POST':
        employee_id = session['employee_id']  # Retrieve the employee ID from the session
        selection = BenefitSelection(EmployeeID=employee_id, ProgramID=program_id)
        db.session.add(selection)
        db.session.commit()
    elif request.method == 'DELETE':
        employee_id = session['employee_id']  # Retrieve the employee ID from the session
        BenefitSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program_id).delete()
        db.session.commit()
    return redirect('/view_benefits')


@selection_bp.route('/deselect/<int:program_id>', methods=['DELETE'])

def deselect(program_id):
    if request.method == 'DELETE':
        employee_id = session['employee_id']  # Retrieve the employee ID from the session
        BenefitSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program_id).delete()
        db.session.commit()
    return render_template('Regular-employee/view-benefits.html')




@selection_bp.route('/benefit_programs/enrollment_status')
def get_enrollment_status():
    employee_id = session.get('employee_id')  # Assuming you have stored the employee ID in the session
    if employee_id is None:
        return jsonify([])  # Return empty list if employee ID is not found in session

    programs = BenefitPrograms.query.all()
    enrollment_status = []

    for program in programs:
        # Check if the employee is enrolled in the current program
        enrolled = BenefitSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program.ProgramID).first() is not None
        enrollment_status.append({
            'ProgramID': program.ProgramID,
            'EmployeeEnrolled': enrolled
        })

    return jsonify(enrollment_status)