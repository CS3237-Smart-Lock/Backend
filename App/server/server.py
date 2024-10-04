from flask import Flask, request
import os
from ..db.db import Database

app = Flask(__name__)

db = Database(os.path.join('db', 'database'))

@app.route("/health")
def health():
    return "<p>health check ok!</p>"

@app.route("/users", methods=['GET'])
def users():
    try:
        users = db.get_all_users()
        res = [dict(row) for row in users]
        return res
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/user/<name>", methods=['DELETE', 'POST'])
def user(name:str):
    if request.method == "POST":
        ...
    elif request.method == "DELETE":
        ...

    return ""

if __name__ == '__main__':
    app.run(debug=True)
