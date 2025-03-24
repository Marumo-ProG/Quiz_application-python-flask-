import os
import sqlite3
from flask import Flask, request, render_template


folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template(
        "./test.html",
        question="What is the capital of France?",
        options=["France", "Paris", "London", "Berlin"],
    )


@app.route("/results", methods=["GET"])
def results():
    return render_template("./results.html", results=50.4)


if __name__ == "__main__":
    app.run(debug=True)
