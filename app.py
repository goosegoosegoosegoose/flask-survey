from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "whatnow"
debug = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():
    """Title of survey, instructions, and start button"""
    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    
    return render_template('homepage.html', title=title, instructions=instructions)

@app.route("/questions/<num>")
def handle_questions(num):
    """Shows question depending on which and how many"""

    responses = session['responses']

    try:
        ques = satisfaction_survey.questions[int(num)].question
        number = f"{int(num) + 1}"
        choices = satisfaction_survey.questions[int(num)].choices
    except:
        flash("Invalid Question")
        return redirect(f"/questions/{len(responses)}")
    
    if int(num) == len(responses):
        return render_template('questionnaire.html', ques=ques, num=number, choices=choices)
    elif len(responses) >= len(satisfaction_survey.questions):
        flash("Invalid Question")
        return redirect("/thankyou")
    else:
        flash("Invalid Question")
        return redirect(f"/questions/{len(responses)}")

    #last question keeps redirecting to itself and not /thankyou

@app.route("/answer", methods=["POST"])
def handle_answers():
    """Append sent answer to responses list and redirect to next question"""

    answer = request.form["resp"]
    
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")


@app.route("/thankyou")
def show_thanks():
    """Thank you page"""

    return render_template("thanks.html")

@app.route("/session", methods=["POST"])
def manage_session():
    """Save answers in session as cookies, reset both session and responses list"""

    responses = []
    session['responses'] = responses
    
    return redirect('/questions/0')