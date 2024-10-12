import os
from datetime import datetime

from App.models import face_detector

from ..db.db import Database 
from ..models.face_detector import FaceDetector

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import filetype

app = Flask(__name__)
CORS(app)

db = Database(os.path.join('db', 'database'))
detector = FaceDetector()

# Health check endpoint
@app.route("/health")
def health():
    return "<h1>Health check OK!</h1>"

# Retrieve all users 
@app.route("/users", methods=['GET'])
def users():
    try:
        users = db.get_all_users()
        res = [
            {
                "id": user["id"],
                "name": user["name"],
                "description": user["description"],
                "image_url": f"/user/{user['id']}/image"
            }
            for user in users
        ]
        return jsonify(res)
    except Exception as e:
        return {"error": str(e)}, 400

# Insert a new user 
@app.route("/user", methods=['POST'])
def insert_user():
    try:
        name = request.form['name']
        description = request.form['description']
        image_file = request.files['face_image']
        image_blob = image_file.read()

        faces = detector.get_faces(image_blob)
        if len(faces) == 0:
            return {"error": "No faces detected, please ensure that the image is clear and the face is not hidden."}, 401
        print(faces)

        if len(faces) > 1:
            return {"error": "More than one face detected. Please ensure that only one face is present in the image"}, 402

        image_with_face_highlighted = detector.get_image_with_face_circled(image_blob)
        db.insert_user(name, description, image_with_face_highlighted)
        
        return {'message':f"User {name} added successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# Delete user by ID endpoint
@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id: int):
    try:
        db.delete_user(id)
        
        return {'message':f"User {id} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/user/<int:user_id>/image", methods=['GET'])
def user_image(user_id):
    try:
        image_blob = db.get_user_image(user_id)
        
        kind = filetype.guess(image_blob)
        if kind is None:
            raise ValueError("Unsupported image format")
        
        response = make_response(image_blob)
        response.headers.set('Content-Type', kind.mime)
        
        return response
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400


@app.route("/attempts", methods=['GET'])
def attempts():
    """
    Endpoint to retrieve attempt logs from start date to end date.
    Date format: yyyy-mm-dd
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        if start_date:
            start_date = str(datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            end_date = str(datetime.strptime(end_date, '%Y-%m-%d').date())
    except ValueError:
        return jsonify({"message": "Invalid date format. Please use yyyy-mm-dd."}), 400
    
    logs = db.get_attempts(start_date, end_date)

    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
