# Import the necessary modules
from flask import jsonify, request,Blueprint    
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
from flask_jwt_extended import jwt_required, get_jwt_identity,JWTManager
from database import db
from CommunicationLogs import CommunicationLogs
from flask_cors import CORS

# Creating a blueprint for the employee module
messages_bp = Blueprint('messages', __name__)
# Enabling CORS for the benefit programs routes
CORS (messages_bp)
# Route to send a message
@messages_bp.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():
    # Get the sender's ID from the JWT claim
    sender_id = get_jwt_identity()

    # Get the receiver's ID from the request body
    receiver_id = request.json['receiver_id']

    # Get the message content from the request body
    message_content = request.json['message_content']

    # Create a new CommunicationLogs entry
    log = CommunicationLogs(SenderID=sender_id, ReceiverID=receiver_id,
                            MessageContent=message_content, MessageType='message')
    db.session.add(log)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Message sent successfully'}), 200


# Route to retrieve message history for a specific employee
@messages_bp.route('/api/messages/<employee_id>', methods=['GET'])
@jwt_required()
def get_message_history(employee_id):
    # Get the employee's ID from the URL parameters
    employee_id = int(employee_id)

    # Query the database for the message history
    logs = db.session.query(CommunicationLogs).filter(
        (CommunicationLogs.SenderID == employee_id) | (CommunicationLogs.ReceiverID == employee_id)).all()

    # Serialize the logs and return them in the response
    data = [log.serialize() for log in logs]
    return jsonify({'logs': data}), 200


# Route to retrieve unread messages for a specific employee
@messages_bp.route('/api/messages/unread/<employee_id>', methods=['GET'])
@jwt_required()
def get_unread_messages(employee_id):
    # Get the employee's ID from the URL parameters
    employee_id = int(employee_id)

    # Query the database for unread messages
    logs = db.session.query(CommunicationLogs).filter(CommunicationLogs.ReceiverID == employee_id,
                                                   CommunicationLogs.Read == False).all()

    # Serialize the logs and return them in the response
    data = [log.serialize() for log in logs]
    return jsonify({'logs': data}), 200


# Define a function to mark messages as read
def mark_messages_as_read(logs):
    for log in logs:
        log.Read = True
    db.session.commit()

# Implement the notification system using a task queue or a background job
