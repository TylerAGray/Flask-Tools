class Question:
    """A single question in a survey."""

    def __init__(self, text, choices=None, allow_text=False):
        """
        Initialize a question with text, optional list of choices, and whether text input is allowed.

        Parameters:
        - text (str): The question text.
        - choices (list, optional): List of answer choices. Defaults to ["Yes", "No"].
        - allow_text (bool, optional): If True, allows additional text input. Defaults to False.
        """
        if choices is None:
            choices = ["Yes", "No"]
        
        self.text = text
        self.choices = choices
        self.allow_text = allow_text

class Survey:
    """A survey containing multiple questions."""

    def __init__(self, title, instructions, questions):
        """
        Initialize a survey with a title, instructions, and a list of questions.

        Parameters:
        - title (str): The title of the survey.
        - instructions (str): Instructions for completing the survey.
        - questions (list): List of Question objects.
        """
        self.title = title
        self.instructions = instructions
        self.questions = questions

# Create an instance of Survey for customer satisfaction
satisfaction_survey = Survey(
    title="Customer Satisfaction Survey",
    instructions="Please fill out this survey about your experience with us.",
    questions=[
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 choices=["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?")
    ]
)

# Create an instance of Survey for a personality quiz
personality_quiz = Survey(
    title="Rithm Personality Test",
    instructions="Learn more about yourself with our personality quiz!",
    questions=[
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 choices=["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 choices=["do_stuff()", "run_me()", "wtf()"], allow_text=True)
    ]
)

# Dictionary to store the available surveys
surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz
}
