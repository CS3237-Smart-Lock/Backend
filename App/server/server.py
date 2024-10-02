from flask import Flask, request

app = Flask(__name__)

@app.route("/health")
def health():
    return "<p>health check ok!</p>"

@app.route("/users", methods=['GET'])
def users():
    return ""

@app.route("/user/<name>", methods=['DELETE', 'POST'])
def user(name:str):
    if request.method == "POST":
        ...
    elif request.method == "DELETE":
        ...

    return ""
