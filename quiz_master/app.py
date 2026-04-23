from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Questions
questions = [
    {"question": "Capital of India?", "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "HighText Machine Language", "Hyper Tool Markup Language", "None"], "answer": "Hyper Text Markup Language"},
    {"question": "Python is?", "options": ["Language", "Snake", "Framework", "OS"], "answer": "Language"},
    {"question": "Flask is?", "options": ["Framework", "Database", "Language", "Library"], "answer": "Framework"}
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quiz')
def quiz():
    shuffled = questions.copy()
    random.shuffle(shuffled)
    session['questions'] = shuffled   # store in session
    return render_template("quiz.html", questions=shuffled)

@app.route('/result', methods=['POST'])
def result():
    user_answers = request.form
    questions = session.get('questions', [])

    score = 0
    negative = 0

    for i, q in enumerate(questions):
        selected = user_answers.get(f"q{i}")
        if selected == q['answer']:
            score += 1
        elif selected:
            negative -= 0.25

    final_score = round(score + negative, 2)

    if final_score >= 4:
        feedback = "🔥 Excellent!"
    elif final_score >= 2:
        feedback = "👍 Good Job!"
    else:
        feedback = "😅 Try Again!"

    return render_template("result.html", score=final_score, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)