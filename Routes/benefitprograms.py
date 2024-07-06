from flask import Blueprint, jsonify, render_template, request
from flask_cors import CORS
from sqlalchemy.orm import joinedload
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from BenefitPrograms import BenefitPrograms
from BenefitSelection import BenefitSelection
from Employee import Employee
from Department import Department
# Creating a new blueprint for the benefit programs routes
benefits_bp = Blueprint('benefits', __name__)
# Enabling CORS for the benefit programs routes
CORS(benefits_bp)
# Defining the route to get all benefit programs
@benefits_bp.route('/benefits', methods=['GET'])
def get_all_benefit_programs():
    """
    This route returns a JSON response containing a list of all the benefit programs.
    """
    # Querying the database to get all benefit programs
    benefit_programs = BenefitPrograms.query.all()
    
    # Creating a list to store the serialized form of each benefit program
    result = []
    
    # Looping through all benefit programs and appending their serialized form to the list
    for program in benefit_programs:
        serialized_program = {
            'ProgramID': program.ProgramID,
            'ProgramName': program.ProgramName,
            'Description': program.Description
        }
        result.append(serialized_program)
    
    # Returning the serialized benefit programs as a JSON response
    return render_template('HR/benefit_programs.html', programs=result)

# Defining the route to get a specific benefit program
@benefits_bp.route('/benefits/<program_id>', methods=['GET'])
def get_benefit_program(program_id):
    """
    This route returns a JSON response containing the serialized form of a specific benefit program.
    If the benefit program is not found, it returns a JSON response with an error message.
    """
    # Querying the database to get a specific benefit program by its ID
    program = BenefitPrograms.query.get(program_id)
    
    # If the benefit program exists, return its serialized form as a JSON response
    if program:
        return jsonify(program.serialize())
    
    # If the benefit program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Benefit program not found'}), 404

# Defining the route to add a new benefit program
@benefits_bp.route('/benefits', methods=['POST'])
def add_benefit_program():
    """
    This route adds a new benefit program to the database and returns a JSON response containing the serialized form of the new benefit program.
    """
    # Getting the JSON data from the request body
    data = request.get_json()
    
    # Creating a new BenefitPrograms object using the data
    program = BenefitPrograms(**data)
    
    # Adding the new benefit program to the database session
    db.session.add(program)
    
    # Committing the changes to the database
    db.session.commit()
    
    # Returning the serialized new benefit program as a JSON response with a 201 status code
    return jsonify({"message": "Benefit program added"}), 201

# Defining the route to update an existing benefit program
@benefits_bp.route('/benefits/<program_id>', methods=['PUT'])
def update_benefit_program(program_id):
    """
    This route updates an existing benefit program with the data from the request body and returns a JSON response 
    containing the serialized form of the updated benefit program.
    If the benefit program is not found, it returns a JSON response with an error message.
    """
    # Querying the database to get a specific benefit program by its ID
    program = BenefitPrograms.query.get(program_id)
    
    # If the benefit program exists, update its attributes with the data from the request body
    if program:
        data = request.get_json()
        program.ProgramID = data.get('ProgramID', program.ProgramID)
        program.ProgramName = data.get('ProgramName', program.ProgramName)
        program.Description = data.get('Description', program.Description)
        db.session.commit()
        serialized_program = {
            'ProgramID': program.ProgramID,
            'ProgramName': program.ProgramName,
            'Description': program.Description
        }
        return jsonify(serialized_program)
    
    # If the benefit program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Benefit program not found'}), 404

# Defining the route to delete an existing benefit program
@benefits_bp.route('/benefits/<program_id>', methods=['DELETE'])
def delete_benefit_program(program_id):
    """
    This route deletes an existing benefit program from the database.
    If the benefit program is not found, it returns a JSON response with an error message.
    """
    # Querying the database to get a specific benefit program by its ID
    program = BenefitPrograms.query.get(program_id)
    
    # If the benefit program exists, delete it from the database
    if program:
        db.session.delete(program)
        db.session.commit()
        return jsonify({'message': 'Benefit program deleted'})
    
    # If the benefit program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Benefit program not found'}), 404



@benefits_bp.route('/benefits/<int:program_id>/enrolled_employees', methods=['GET'])
def get_enrolled_employees_benefits(program_id):
    # Query to get enrolled employees for the specified benefit program
    enrolled_employees = db.session.query(Employee, Department).\
        join(BenefitSelection).\
        join(Department, Employee.DepartmentName == Department.DepartmentName).\
        filter(BenefitSelection.ProgramID == program_id).\
        options(joinedload(Employee.department)).all()  

    # Serialize the data (similar to training program route)
    serialized_employees = [{
        'EmployeeID': employee.EmployeeID,
        'FirstName': employee.FirstName,
        'LastName': employee.LastName,
        'DepartmentName': department.DepartmentName if department else "No Department"
    } for employee, department in enrolled_employees]

    return jsonify(serialized_employees)

@benefits_bp.route('/benefits/<int:program_id>/enrolled_employees/count', methods=['GET'])
def get_enrolled_employees_count_benefits(program_id):
    # Query to get enrolled employees count for the specified benefit program
    enrolled_employees = db.session.query(BenefitSelection).filter_by(ProgramID=program_id).all()
    enrolled_count = len(enrolled_employees)

    return jsonify(enrolled_count)
