from flask import Blueprint, jsonify, request,render_template
import json
import sys
from werkzeug.utils import secure_filename
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from Performance_Review import PerformanceReview
from database import db

review_bp = Blueprint('review', __name__)
@review_bp.route('/performance/reviews', methods=['POST'])
def schedule_review():
    data = request.json
    review = PerformanceReview(
        employee_id=data['employee_id'],
        manager_id=data['manager_id'],
        scheduled_date=data['scheduled_date']
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Performance review scheduled successfully'}), 201

@review_bp.route('/performance/reviews', methods=['GET'])
def get_reviews():
    reviews = PerformanceReview.query.all()
    for review in reviews:
        review.to_dict()
    return render_template('Manager/performance_review.html',reviews=reviews)

# @review_bp.route('/performance/reviews/<int:review_id>/feedback', methods=['POST'])
# def provide_feedback(review_id):
#     data = request.json
#     review = PerformanceReview.query.get(review_id)
#     review.feedback = data['feedback']
#     review.rating = data['rating']
#     db.session.commit()
#     return jsonify({'message': 'Feedback provided successfully'})


