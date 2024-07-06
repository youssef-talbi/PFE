from flask import Blueprint, jsonify, request,render_template
from flask_cors import CORS
import sys

from sqlalchemy import func
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Roles import Role

# Create a blueprint for the roles endpoint
roles_bp = Blueprint('roles', __name__)
CORS(roles_bp)


# Define a GET route for the '/roles' endpoint
@roles_bp.route('/roles', methods=['GET'])
def admin_get_all_roles():
    # Query all roles
    roles = db.session.query(Role).all()
    # Serialize the roles as JSON
    serialized_roles = []
    for role in roles:
        serialized_roles.append({
            'RoleID': role.RoleID,
            'RoleName': role.RoleName,
            'Description': role.Description
        })
    return render_template('admin/create_roles.html', roles=serialized_roles)  # Render the HTML template instead of returning JSON


# Define a GET route for the '/roles' endpoint
@roles_bp.route('/HR/roles', methods=['GET'])
def get_all_roles():
    # Query all roles
    roles = db.session.query(Role).all()
    # Serialize the roles as JSON
    serialized_roles = []
    for role in roles:
        serialized_roles.append({
            'RoleID': role.RoleID,
            'RoleName': role.RoleName,
            'Description': role.Description
        })
    return render_template('HR/create_roles.html', roles=serialized_roles)  # Render the HTML template instead of returning JSON
    

# Define a GET route for the '/roles/<role_id>' endpoint
@roles_bp.route('/roles/<role_id>', methods=['GET'])
def get_role_by_id(role_id):
    # Query a role by its ID
    role = db.session.query(Role).filter(Role.RoleID == role_id).first()
    if role is None:
        return jsonify({'message': 'Role not found'}), 404
    # Serialize the role as JSON
    serialized_role = {
        'RoleID': role.RoleID,
        'RoleName': role.RoleName,
        'Description': role.Description
    }
    return jsonify(serialized_role)

@roles_bp.route('/roles/<role_name>', methods=['GET'])
def get_role_by_name(role_name):
    # Query a role by its name
    role = db.session.query(Role).filter(Role.RoleName == role_name).first()
    if role is None:
        return jsonify({'message': 'Role not found'}), 404
    # Serialize the role as JSON
    serialized_role = {
        'RoleID': role.RoleID,
        'RoleName': role.RoleName,
        'Description': role.Description
    }
    return jsonify(serialized_role)

@roles_bp.route('/roles', methods=['POST'])
def add_role():
    valid_roles = [role_name.lower() for role_name in ["HR administrator", "department head", "regular employee"]]
    # Get the JSON data from the request
    roles_data = request.get_json()

    # Ensure that roles_data is a list
    if not isinstance(roles_data, list):
        return jsonify({'error': 'Invalid data format. Expected a list of role data.'}), 400

    try:
        # List to hold the newly created roles
        new_roles = []

        # Begin a transaction
        with db.session.begin_nested():
            # Iterate over each role data in the list
            for role_data in roles_data:
                # Convert the RoleName to lowercase for case-insensitive comparison
                role_name_lower = role_data['RoleName'].lower()
                # Check if the RoleName is valid
                if role_name_lower not in valid_roles:
                    return jsonify({'error': f'Invalid RoleName "{role_data["RoleName"]}". Allowed values: HR administrator, department head, regular employee'}), 400

                # Create a new Role instance with the provided RoleID and RoleName and Description
                role = Role(RoleID=role_data['RoleID'], RoleName=role_data['RoleName'], Description=role_data.get('Description'))
                # Add the role to the database session
                db.session.add(role)
                # Append the new role to the list
                new_roles.append(role)

        # Commit the changes
        db.session.commit()

        # Serialize the roles as JSON and return a 201 status code
        serialized_roles = [{
            'RoleID': role.RoleID,
            'RoleName': role.RoleName,
            'Description': role.Description
        } for role in new_roles]
        return jsonify(serialized_roles), 201

    except Exception as e:
        # Handle any exceptions that might occur during data processing
        db.session.rollback()
        return jsonify({'error': 'An error occurred while adding roles.', 'message': str(e)}), 500



# Define a PUT route for the '/roles/<role_name>' endpoint
@roles_bp.route('/roles/<role_name>', methods=['PUT'])
def update_role(role_name):
    # Query a role by its name
    role = db.session.query(Role).filter_by(RoleName=role_name.lower()).first()
    if role is None:
        return jsonify({'message': 'Role not found'}), 404
    # Get the JSON data from the request
    role_data = request.get_json()
    # Update the role attributes
    role.Description = role_data.get('Description')
    # Commit the changes
    db.session.commit()
    # Serialize the role as JSON and return it
    serialized_role = {
        'RoleID': role.RoleID,
        'RoleName': role.RoleName,
        'Description': role.Description
    }
    return jsonify(serialized_role)

# Define a DELETE route for the '/roles/<role_name>' endpoint
@roles_bp.route('/roles/<role_name>', methods=['DELETE'])
def delete_role(role_name):
    # Query a role by its name
    role = db.session.query(Role).filter_by(RoleName=role_name.lower()).first()
    if role is None:
        return jsonify({'message': 'Role not found'}), 404
    # Delete the role from the database session
    db.session.delete(role)
    # Commit the changes
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Role deleted successfully'})



