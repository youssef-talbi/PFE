from flask import Blueprint, jsonify, request,render_template
from sqlalchemy.orm import joinedload
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Training import TrainingPrograms
from TrainingSelection import TrainingSelection
from Employee import Employee
from Department import Department
from flask_cors import CORS
# Creating blueprint for our routes, named 'traininprog_routes'
traininprog_routes = Blueprint('traininprog_routes', __name__)
CORS(traininprog_routes)
# Route to get all training programs
@traininprog_routes.route('/Tprograms', methods=['GET'])
def get_all_training_programs():
    # Querying the database to get all training programs
    training_programs = TrainingPrograms.query.all()
    
    # Creating a list to store serialized training programs with count
    result = []
    
    # Looping through all training programs
    for training_program in training_programs:
        # Get the count of enrolled employees for the current program
        enrolled_count = training_program.EnrolledEmployeesCount
        # Serialize the training program including count
        serialized_program = training_program.serialize()
        serialized_program['EnrolledEmployeesCount'] = enrolled_count
        result.append(serialized_program)
    
    # Returning the serialized training programs as a JSON response
    return render_template('HR/trainings.html', programs=result)


# Route to get a specific training program by its ID
@traininprog_routes.route('/Tprograms/<program_id>', methods=['GET'])
def get_training_program(program_id):
    # Querying the database to get a specific training program by its ID
    training_program = TrainingPrograms.query.get(program_id)
    
    # If the training program exists, return its serialized form as a JSON response
    if training_program:
        return jsonify(training_program.serialize())
    
    # If the training program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Training program not found'}), 404

# Route to add a new training program
@traininprog_routes.route('/Tprograms', methods=['POST'])
def add_training_program():
    # Getting the JSON data from the request body
    data = request.get_json()
    
    # Creating a new TrainingPrograms object using the data
    training_program = TrainingPrograms(**data)
    
    # Adding the new training program to the database session
    db.session.add(training_program)
    
    # Committing the changes to the database
    db.session.commit()
    
    # Returning the serialized new training program as a JSON response with a 201 status code
    return jsonify(training_program.serialize()), 201

# Route to update a specific training program by its ID
@traininprog_routes.route('/Tprograms/<program_id>', methods=['PUT'])
def update_training_program(program_id):
    # Querying the database to get a specific training program by its ID
    training_program = TrainingPrograms.query.get(program_id)
    
    # If the training program exists, update its attributes with the data from the request body
    if training_program:
        data = request.get_json()
        training_program.ProgramID = data.get('ProgramID', training_program.ProgramID)
        training_program.ProgramName = data.get('ProgramName', training_program.ProgramName)
        training_program.Trainer = data.get('Trainer', training_program.Trainer)
        training_program.Schedule = data.get('Schedule', training_program.Schedule)
        training_program.Description = data.get('Description', training_program.Description)
        training_program.Status = data.get('Status', training_program.Status)
        training_program.StartDate = data.get('StartDate', training_program.StartDate)
        training_program.EndDate = data.get('EndDate', training_program.EndDate)
        training_program.TrainingType = data.get('TrainingType', training_program.TrainingType)
        training_program.Cost = data.get('Cost', training_program.Cost)
        
        # Committing the changes to the database
        db.session.commit()
        
        # Returning the serialized updated training program as a JSON response
        return jsonify(training_program.serialize())
    
    # If the training program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Training program not found'}), 404

# Route to delete a specific training program by its ID
@traininprog_routes.route('/Tprograms/<int:program_id>', methods=['DELETE'])
def delete_training_program(program_id):
    # Querying the database to get a specific training program by its ID
    training_program = TrainingPrograms.query.get(program_id)
    
    # If the training program exists, delete it from the database
    if training_program:
        try:
            db.session.delete(training_program)
            db.session.commit()
            # Returning a success message as a JSON response
            return jsonify({'message': 'Training program deleted'}), 200
        except Exception as e:
            # If there's an error during deletion, rollback changes and return an error message
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # If the training program does not exist, return an error message as a JSON response with a 404 status code
    return jsonify({'error': 'Training program not found'}), 404




#Route to get the training programs for the FullCalendar
@traininprog_routes.route('/Tprograms/calendar', methods=['GET'])
def get_training_programs_calendar():
    # Querying the database to get all training programs
    training_programs = TrainingPrograms.query.all()
    serialize_training_programs = [{
        'title': training_program.ProgramName,
        'start': training_program.StartDate,
        'end': training_program.EndDate,
    } for   training_program in training_programs ] 
    return jsonify(serialize_training_programs)



@traininprog_routes.route('/Tprograms/<int:program_id>/enrolled_employees', methods=['GET'])
def get_enrolled_employees(program_id):
    # Query the database to get enrolled employees for the specified training program
    enrolled_employees = db.session.query(Employee, Department).\
        join(TrainingSelection).\
        join(Department, Employee.DepartmentName == Department.DepartmentName).\
        filter(TrainingSelection.ProgramID == program_id).\
        options(joinedload(Employee.department)).all()
    
    # Serialize the enrolled employees' data
    serialized_employees = [{
        'EmployeeID': employee.EmployeeID,
        'FirstName': employee.FirstName,
        'LastName': employee.LastName,
        'DepartmentName': department.DepartmentName if department else "No Department"
    } for employee, department in enrolled_employees]
    
    # Return the serialized enrolled employees as a JSON response
    return jsonify(serialized_employees)




