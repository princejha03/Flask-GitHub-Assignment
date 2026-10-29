
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__, template_folder="templates")

# Read the MongoDB connection string from an environment variable.
mongo_url = os.environ.get("MONGODB_URI")

if not mongo_url:
    raise RuntimeError("Please set the MONGODB_URI environment variable.")

client = MongoClient(mongo_url)
db = client["todo_database"]
todo_collection = db["todo_items"]


@app.route("/")
def todo_page():
    return render_template("todo.html")


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    # Support the HTML form and JSON POST requests.
    data = request.get_json(silent=True) if request.is_json else request.form

    item_name = (data.get("itemName") or "").strip()
    item_description = (data.get("itemDescription") or "").strip()

    if not item_name or not item_description:
        return jsonify({
            "error": "Item Name and Item Description are required."
        }), 400

    todo_collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return jsonify({
        "message": "To-Do item submitted successfully."
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
