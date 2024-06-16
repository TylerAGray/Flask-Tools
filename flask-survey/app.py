from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# Key name for storing responses in the session
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"  # Secret key for session management and flash messages
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Allow redirects with the debug toolbar

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Display the survey start page with survey title and instructions."""
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses and start the survey."""
    session[RESPONSES_KEY] = []  # Initialize an empty list to store responses
    return redirect("/questions/0")  # Redirect to the first question

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to the next question."""
    choice = request.form['answer']  # Get the selected answer from the form
    responses = session[RESPONSES_KEY]  # Retrieve the current list of responses from the session
    responses.append(choice)  # Add the new response to the list
    session[RESPONSES_KEY] = responses  # Save the updated list back to the session

    if len(responses) == len(survey.questions):
        # If all questions are answered, redirect to the completion page
        return redirect("/complete")
    else:
        # Otherwise, redirect to the next question
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display the current question."""
    responses = session.get(RESPONSES_KEY)  # Get the current list of responses from the session

    if responses is None:
        # If no responses are found in the session, redirect to the start page
        return redirect("/")
    
    if len(responses) == len(survey.questions):
        # If all questions are answered, redirect to the completion page
        return redirect("/complete")

    if len(responses) != qid:
        # If the user tries to access a question out of order, show a flash message and redirect to the correct question
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]  # Get the current question based on the question id
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show the completion page."""
    return render_template("completion.html")

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
