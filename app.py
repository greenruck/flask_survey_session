from flask import Flask, render_template, request, redirect, flash, jsonify, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

RESPONSES_KEY= "responses"                  

@app.route('/',)
def home_page():
    session[RESPONSES_KEY] = []
    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route("/question/<int:qn>", methods=["POST", "GET"])
def question(qn):
    """Display current question."""
    question = satisfaction_survey.questions[qn]
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect("/")
   
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
   
    if (len(responses)!= qn):
        return redirect(f"/questions/{len(responses)}")
   
    else:
        return render_template('question.html', satisfaction_survey=satisfaction_survey, question = satisfaction_survey.questions[qn])


@app.route("/answer", methods=["POST", "GET"])
def handle_question():
   
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses


    if (len(responses) == len(satisfaction_survey.questions)):
 
        return redirect("/complete")

    else:
        print(session)
        print(len(responses))
        return redirect(f"/question/{len(responses)}")

@app.route("/complete")
def complete():
    return render_template("complete.html")