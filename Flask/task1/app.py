from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    # Get the folder where app.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the complete path to data.json
    file_path = os.path.join(base_dir, "data.json")

    # Read the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Return JSON response
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)