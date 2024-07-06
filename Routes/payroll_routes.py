import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Payroll import PayrollDetails
from flask import jsonify,request, Blueprint
from flask_cors import CORS
payroll_bp = Blueprint('payroll_details', __name__)
CORS(payroll_bp)
# Define a GET route for the '/payrolls' endpoint
@payroll_bp.route('/payrolls', methods=['GET'])
def get_all_payrolls():
    # Query all payroll details
    payrolls = db.session.query(PayrollDetails).all()
    # Serialize the payroll details as JSON
    serialized_payrolls = []
    for payroll in payrolls:
        serialized_payrolls.append({
            'EmployeeID': payroll.EmployeeID,
            'Month': payroll.Month,
            'Year': payroll.Year,
            'SalaryDetails': float(payroll.SalaryDetails)  # Convert to float for JSON serialization
        })
    return jsonify(serialized_payrolls)

# Define a GET route for the '/payrolls/<employee_id>' endpoint
@payroll_bp.route('/payrolls/<employee_id>', methods=['GET'])
def get_payroll_by_employee_id(employee_id):
    # Query payroll details by employee ID
    payrolls = db.session.query(PayrollDetails).filter(PayrollDetails.EmployeeID == employee_id).all()
    if not payrolls:
        return jsonify({'message': 'Payroll details not found for employee'}), 404
    # Serialize the payroll details as JSON
    serialized_payrolls = []
    for payroll in payrolls:
        serialized_payrolls.append({
            'EmployeeID': payroll.EmployeeID,
            'Month': payroll.Month,
            'Year': payroll.Year,
            'SalaryDetails': float(payroll.SalaryDetails)  # Convert to float for JSON serialization
        })
    return jsonify(serialized_payrolls)

# Define a POST route for the '/payrolls' endpoint
@payroll_bp.route('/payrolls', methods=['POST'])
def add_payroll():
    # Get the JSON data from the request
    payroll_data = request.get_json()
    # Create a new payroll detail instance
    new_payroll = PayrollDetails(**payroll_data)
    # Add the new payroll detail to the database session
    db.session.add(new_payroll)
    # Commit the changes
    db.session.commit()
    # Serialize the new payroll detail as JSON and return it with a 201 status code
    serialized_payroll = {
        'EmployeeID': new_payroll.EmployeeID,
        'Month': new_payroll.Month,
        'Year': new_payroll.Year,
        'SalaryDetails': float(new_payroll.SalaryDetails)  # Convert to float for JSON serialization
    }
    return jsonify(serialized_payroll), 201

# Define a PUT route for the '/payrolls/<employee_id>' endpoint
@payroll_bp.route('/payrolls/<employee_id>', methods=['PUT'])
def update_payroll(employee_id):
    # Get the JSON data from the request
    payroll_data = request.get_json()
    # Query payroll details by employee ID
    payroll = db.session.query(PayrollDetails).filter(PayrollDetails.EmployeeID == employee_id).first()
    if not payroll:
        return jsonify({'message': 'Payroll details not found for employee'}), 404
    # Update the payroll detail attributes
    for key, value in payroll_data.items():
        setattr(payroll, key, value)
    # Commit the changes
    db.session.commit()
    # Serialize the updated payroll detail as JSON and return it
    serialized_payroll = {
        'EmployeeID': payroll.EmployeeID,
        'Month': payroll.Month,
        'Year': payroll.Year,
        'SalaryDetails': float(payroll.SalaryDetails)  # Convert to float for JSON serialization
    }
    return jsonify(serialized_payroll)

# Define a DELETE route for the '/payrolls/<employee_id>' endpoint
@payroll_bp.route('/payrolls/<employee_id>', methods=['DELETE'])
def delete_payroll(employee_id):
    # Query payroll details by employee ID
    payroll = db.session.query(PayrollDetails).filter(PayrollDetails.EmployeeID == employee_id).first()
    if not payroll:
        return jsonify({'message': 'Payroll details not found for employee'}), 404
    # Delete the payroll detail from the database session
    db.session.delete(payroll)
    # Commit the changes
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Payroll details deleted successfully'})
