from flask import Flask, session, request, render_template, redirect, make_response, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

# Constants for session keys to ensure consistency
CURRENT_SURVEY_KEY = 'current_survey'
RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"  # Secret key for session management
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Disable toolbar interception of redirects

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_selection():
    """Render a form to select a survey from the available options."""
    return render_template("pick-survey.html", surveys=surveys)

@app.route("/", methods=["POST"])
def select_survey():
    """Handle survey selection and initialize the session."""
    survey_id = request.form['survey_code']

    # Prevent re-taking the survey by checking for a completion cookie
    if request.cookies.get(f"completed_{survey_id}"):
        return render_template("already-done.html")

    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Start the survey by clearing any existing responses in the session."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def save_response():
    """Save the current response and redirect to the next question."""
    choice = request.form['answer']
    text = request.form.get("text", "")  # Get optional text response

    # Append the response to the session-stored list
    responses = session.get(RESPONSES_KEY, [])
    responses.append({"choice": choice, "text": text})
    session[RESPONSES_KEY] = responses

    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if len(responses) == len(survey.questions):
        # All questions answered, redirect to the completion page
        return redirect("/complete")
    else:
        # Redirect to the next question
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def display_question(qid):
    """Show the current question to the user."""
    responses = session.get(RESPONSES_KEY)
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if responses is None:
        # If no responses yet, redirect to the start page
        return redirect("/")

    if len(responses) == len(survey.questions):
        # All questions answered, redirect to the completion page
        return redirect("/complete")

    if len(responses) != qid:
        # If the user tries to access questions out of order, redirect to the correct question
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete_survey():
    """Thank the user for completing the survey and show their responses."""
    survey_id = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_id]
    responses = session[RESPONSES_KEY]

    # Render the completion page with survey and responses data
    html = render_template("completion.html", survey=survey, responses=responses)

    # Set a cookie to prevent re-taking the survey
    response = make_response(html)
    response.set_cookie(f"completed_{survey_id}", "yes", max_age=60)
    return response

if __name__ == '__main__':
    app.run(debug=True)
