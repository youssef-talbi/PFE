import json
import sys
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\database\\Models')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\utils')
sys.path.append('C:\\Users\\youssef\\Desktop\\PFE\\demo2\\Routes')
import face_recognition
from database import db
from Employee import Employee

def update_face(employee_id, images_json):
    employee = Employee.query.get(employee_id)
    if employee:
        existing_encodings = json.loads(employee.face_encoding) if employee.face_encoding else []
        new_face_encodings = []

        try:
            images_list = json.loads(images_json)
            if not isinstance(images_list, list):
                raise ValueError("images_json must be a JSON string representing a list of image paths")
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format for images_json") from e

        for image_path in images_list:
            try:
                image = face_recognition.load_image_file(image_path)
                print(f"loaded {image_path} successfully")
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, face_locations)
                print(f"encoded {image_path} successfully")
                if len(face_encodings) == 1:
                    new_face_encodings.append(face_encodings[0].tolist()) #convert np.array to list
                elif len(face_encodings) > 1:
                    print("Warning: Multiple faces detected in an image. Skipping this image.")
                else:
                    print("No face detected in an image. Skipping this image.")
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")

        combined_encodings = existing_encodings + new_face_encodings
        return json.dumps(combined_encodings) #return list of lists, convert later to list of np.arrays to work with face_recognition