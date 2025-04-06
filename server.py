import os
import sqlite3
from flask import Flask, request, render_template, redirect

# storing the vars in a session variable
session = {"question_int_tracker": 0, "max_questions": 3, "score": 0}


# creating the database connection
def db_connection():
    conn = sqlite3.connect("quiz_app_database.db")
    cursor = conn.cursor()
    return cursor, conn


# creating the questions table
def create_table():
    cursor, conn = db_connection()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer TEXT
        )"""
    )
    conn.commit()
    conn.close()


def populate_question():
    cursor, conn = db_connection()

    # populate the questions table
    cursor.execute(
        """INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES ("What is the capital of France?", "France", "Paris", "London", "Berlin", "Paris")"""
    )

    cursor.execute(
        """INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES ("Who won the 2020 FIFA World Cup?", "Brazil", "Germany", "Spain", "Italy", "Germany")"""
    )

    cursor.execute(
        """INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES ("Who is the current Prime Minister of France?", "Nicolas Sarkozy", "Marine Le Pen", "Emmanuel Macron", "Frédéric Chirac", "Marine Le Pen")"""
    )

    conn.commit()  # saving the changes from memory to the database


folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    # getting the questions from the database
    cursor, conn = db_connection()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()  # [ ("question", "option1" ...), () ]
    print(questions[session["question_int_tracker"]])
    return render_template(
        "./test.html",
        question=questions[session["question_int_tracker"]],
    )


@app.route("/results", methods=["GET"])
def results():
    choice = request.args.get("choice")
    cursor, conn = db_connection()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    if choice == questions[session["question_int_tracker"]][6]:
        session["score"] += 1

    if session["question_int_tracker"] == session["max_questions"] - 1:
        session["question_int_tracker"] = 0  # reset
        return render_template(
            "./results.html",
            results=round(session["score"] / session["max_questions"] * 100),
        )
    else:
        if choice:
            session["question_int_tracker"] += 1
        return redirect("/test")


if __name__ == "__main__":
    app.run(debug=True)
