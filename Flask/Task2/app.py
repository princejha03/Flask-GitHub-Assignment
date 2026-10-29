from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load variables from .env file
load_dotenv()

# Read MongoDB connection details from .env
MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

# Check if MongoDB URL exists
if not MONGO_URL:
    raise ValueError("MongoDB connection URL is missing.")

# MongoDB Atlas connection
client = MongoClient(MONGO_URL)

# Select database
db = client[MONGODB_DATABASE or "student_database"]

# Select collection
collection = db["students"]


@app.route("/", methods=["GET", "POST"])
def form():

    error = None

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        grade = request.form.get("grade")

        try:

            data = {
                "name": name,
                "email": email,
                "grade": grade
            }

            collection.insert_one(data)

            return redirect(url_for("success"))

        except Exception as e:

            error = str(e)

    return render_template("form.html", error=error)


@app.route("/success")
def success():

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)