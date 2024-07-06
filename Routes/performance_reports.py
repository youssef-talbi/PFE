from flask import Blueprint, jsonify, request,render_template
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from Performance import PerformanceGoal
from Performance_Review import PerformanceReview
reports_bp = Blueprint('report', __name__)
@reports_bp.route('/performance/reports', methods=['GET'])
def generate_report():
    goals = PerformanceGoal.query.all()
    reviews = PerformanceReview.query.all()

    return render_template('HR/performance_report.html', goals=goals, reviews=reviews)
