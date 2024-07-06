from flask import session
from flask import Blueprint, jsonify, redirect, request,render_template
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Training import TrainingPrograms

from TrainingSelection import TrainingSelection
from flask_cors import CORS
Tselection_bp = Blueprint('training-selection', __name__)
CORS(Tselection_bp)

@Tselection_bp.route('/view_trainings')
def view_trainings():
    training_programs = TrainingPrograms.query.all()
    return render_template('Regular-employee/view-trainings.html', training_programs=training_programs)


@Tselection_bp.route('/enroll_training/<int:program_id>', methods=['POST', 'DELETE'])
def enroll_training(program_id):
    if request.method == 'POST':
        employee_id = session.get('employee_id')
        selection = TrainingSelection(ProgramID=program_id, EmployeeID=employee_id)
        db.session.add(selection)
        # Increment EnrolledEmployeesCount when enrolling
        program = TrainingPrograms.query.get(program_id)
        if program:
            program.EnrolledEmployeesCount += 1
            db.session.commit()
    elif request.method == 'DELETE':
        employee_id = session.get('employee_id')
        TrainingSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program_id).delete()
        # Decrement EnrolledEmployeesCount when deselecting
        program = TrainingPrograms.query.get(program_id)
        if program and program.EnrolledEmployeesCount > 0:
            program.EnrolledEmployeesCount -= 1
            db.session.commit()
    return redirect('/view_trainings')



@Tselection_bp.route('/Tselection/enrollment_status')
def get_enrollment_status():
    employee_id = session.get('employee_id')
    if employee_id is None:
        return jsonify([])  # Return empty list if employee ID is not found in session

    programs = TrainingPrograms.query.all()
    enrollment_status = []

    for program in programs:
        enrolled = TrainingSelection.query.join(TrainingSelection.program).filter(
            TrainingSelection.EmployeeID == employee_id,
            TrainingPrograms.ProgramID == program.ProgramID
        ).first()

        # Get the count of enrolled employees for each program
        enrolled_count = program.EnrolledEmployeesCount

        # Check if the employee is enrolled in the current program
        enrollment_status.append({
            'ProgramID': program.ProgramID,
            'ProgramName': program.ProgramName,
            'EmployeeEnrolled': enrolled is not None,
            'EnrolledEmployeesCount': enrolled_count
        })

    return jsonify(enrollment_status)



@Tselection_bp.route('/deselect_training/<int:program_id>', methods=['DELETE'])
def deselect_training(program_id):
    if request.method == 'DELETE':
        employee_id = session.get('employee_id')
        # Get the program before deletion to ensure it exists
        program = TrainingPrograms.query.get(program_id)
        if program:
            # Check if the employee is enrolled in the program
            if TrainingSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program_id).first():
                # Remove the selection
                TrainingSelection.query.filter_by(EmployeeID=employee_id, ProgramID=program_id).delete()
                # Decrement EnrolledEmployeesCount
                program.EnrolledEmployeesCount -= 1
                db.session.commit()
    return render_template('Regular-employee/view-trainings.html')
