from flask import render_template,jsonify,Blueprint
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from database import db
from Employee import Employee
from flask_cors import CORS
count_bp = Blueprint('count', __name__)
CORS(count_bp)
@count_bp.route('/hr_dashboard')

def hr_dashboard():
    try:
        # Querying the database to get the total number of employees
        total_employees =db.session.query(Employee).count()
        # Render the HR dashboard template and pass the total employee count as a variable
        return render_template('hr-dashboard.html', total_employees=total_employees)
    except Exception as e:
        # Handle any exceptions that might occur during database query
        return jsonify({'message': 'An error occurred while fetching employee data.', 'error': str(e)}), 500