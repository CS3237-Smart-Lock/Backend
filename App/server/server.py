import os

from ..db.db import Database 

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import filetype

app = Flask(__name__)
CORS(app)

db = Database(os.path.join('db', 'database'))

# Health check endpoint
@app.route("/health")
def health():
    return "<h1>Health check OK!</h1>"

# Retrieve all users endpoint
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

# Insert a new user endpoint
@app.route("/user", methods=['POST'])
def insert_user():
    try:
        name = request.form['name']
        description = request.form['description']
        image_file = request.files['face_image']
        image_blob = image_file.read()
        print(image_blob)
        
        db.insert_user(name, description, image_blob)
        
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
        
        # Identify the image type using `filetype`
        kind = filetype.guess(image_blob)
        if kind is None:
            raise ValueError("Unsupported image format")
        
        # Set the Content-Type header based on the identified mime type
        response = make_response(image_blob)
        response.headers.set('Content-Type', kind.mime)
        
        return response
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400
