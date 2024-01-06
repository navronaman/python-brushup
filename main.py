# This is the Flask app
from flask import Flask

app = Flask(__name__)

@app.route("/")

def index():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="120.0.0.1", port=8080, debug=True)