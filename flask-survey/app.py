from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
debug = DebugToolbarExtension(app)
RESPONSES_KEY = "responses"


app.config['SECRET_KEY'] = 'open-sesame'  # Replace with a strong secret key
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.template_folder = 'templates'



@app.route('/')
def survey_form():
    """Shows the first page of the survey."""
   
    return render_template("start-survey.html", survey = survey)

@app.route('/answer', methods = ["POST"])
def answer():
    """Saves user response to response list and redirect to next question"""

    

    choice = request.form('answer')

    session[RESPONSES_KEY] = []

    responses = session[RESPONSES_KEY]

    responses.append(choice)

    session[RESPONSES_KEY] = responses

    if len(survey.questions) == len(responses):
        return redirect('/completed-form')
    else: 
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:qnum>')
def question(qnum):
    """Shows the current question."""
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete_form")
    
    if (len(responses) != qnum):
        flash(f"Invalid question id: {qnum}.")
        return redirect(f"/questions/{len(responses)}")

    
    question = survey.questions[qnum]
    return render_template('question.html', question = question, question_num =qnum )

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completed_form.html")
