from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "whatnow"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def show_homepage():
    """Title of survey, instructions, and start button"""
    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    
    return render_template('homepage.html', title=title, instructions=instructions)

@app.route("/questions/<num>")
def handle_questions(num):
    """Shows question depending on which and how many"""

    ques = satisfaction_survey.questions[int(num)].question
    number = num
    choices = satisfaction_survey.questions[int(num)].choices

    return render_template('questionnaire.html', ques=ques, num=number, choices=choices)

@app.route("/answer", methods=["POST"])
def handle_answers():
    """Append sent answer to responses list and redirect to next question"""

    answer = request.form["resp"]
    responses.append(answer)
    
    
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thankyou")

@app.route("/thankyou")
def show_thanks():
    """Thank you page"""

    return render_template("thanks.html", responses=responses)