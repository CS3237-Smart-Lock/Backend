from flask import Flask

app = Flask(__name__)

@app.route("/health")
def health():
    return "<p>health check ok!</p>"


