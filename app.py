from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'lets_keep_it_a_secret'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"




@app.route('/')
def welcome_page():
    """Greeting page with a button to start satisfaction survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start-satisfaction-survey.html",title=title,instructions=instructions)






@app.route('/session', methods = ['POST'])
def start_survey()
"""Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')






@app.route('/questions/<int:qid>') 
def question_page(qid):
    """Uses length of submitted responses to define 
    to which question the user should be directed to""" 
    
    responses = session.get(RESPONSES_KEY)

    if (qid != len(responses)):
        # Trying to access questions out of order.
        flash("Please answer the question and stop messing with my URL!", "error")
        return redirect(f'/questions/{len(responses)}')
    
    if (responses is None):
        #Trying to acces question page too soon
        return redirect('/')
    
    current_question = satisfaction_survey.questions[qid].question
    choices = satisfaction_survey.questions[qid].choices

    return render_template("question-page.html", resp_length = qid, current_question=current_question, choices=choices)





@app.route('/thank-you-page')
def thanks():
    """thanking the user for completing the survey"""

    return render_template('thank-you-page.html')




@app.route('/questions/answer', methods = ["POST"])
def handle_answer():
    """Accepting user's input and saving it in global
     RESPONSE variable, then redirecting the user to the next 
     question"""

    answer = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(answer)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thank-you-page")

    return redirect(f'/questions/{len(responses)}')
