from flask import Flask, request, jsonify  
import os
from ..db.db import Database 

app = Flask(__name__)

# Initialize the database connection
db = Database(os.path.join('db', 'database'))

# Health check endpoint
@app.route("/health")
def health():
    return "<p>Health check OK!</p>"

# Retrieve all users endpoint
@app.route("/users", methods=['GET'])
def users():
    try:
        users = db.get_all_users()
        res = [dict(row) for row in users]
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
        
        db.insert_user(name, description, image_blob)
        
        return f"User {name} added successfully", 201
    except Exception as e:
        return {"error": str(e)}, 400

# Delete user by ID endpoint
@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id: int):
    try:
        db.delete_user(id)
        
        return f"User {id} deleted successfully", 200  
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
