import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style
from flask import Flask, request, render_template, session
from datetime import timedelta


app = Flask(__name__)
load_dotenv()

app.secret_key = 'topsecret'
openai.api_key = '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'

INSTRUCTIONS = """
    You are an AI assistant that is an expert in alcoholic beverages
    You know about cocktails, wines, spirtis and beers.
    You can provide advice on drink menus, cocktail ingredients, how to make cocktails, and anything else related to alcoholic drinks.
    If you are unable to provide an answer to a question, please respond with the phrase "I'm just a simple AI bartender, I can't help with that."
    Do not use any external URLs in your answers. Do not refer to any blogs in you answers.
    Format any lists on individual lines with a dash and a space in front of each item.
"""

ANSWER_SEQUENCE = "\nAI:"
QUESTION_SEQUENCE = "\nHuman: "
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10


def get_response(prompt):
    """
    Get a response from the model using the prompt
    Parameters:
        prompt (str): The prompt to use to generate the response
    Returns the response from the model
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return response.choices[0].text

def get_moderation(question):
    """
    Check the question is safe to ask the model
    Parameters:
        question (str): The question to check
    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None

@app.route("/", methods=["GET", "POST"])
def handle_request():
    # Check if session is still alive
    if "conversation" in session:
        # Session is still alive, retrieve conversation history
        conversation = session["conversation"]
    else:
        # Session has ended, clear session and start a new conversation
        session.clear()
        conversation = []

    if request.method == "POST":
        message = request.form.get("message")
        previous_questions_and_answers = session.get("previous_questions_and_answers", [])

        context = ""
        messages = []
        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            context += QUESTION_SEQUENCE + question + ANSWER_SEQUENCE + answer
            messages.append({'from': 'user', 'text': question})
            messages.append({'from': '', 'text': answer})

        context += QUESTION_SEQUENCE + message

        response = get_response(INSTRUCTIONS + context)

        previous_questions_and_answers.append((message, response))

        messages.append({'from': 'user', 'text': message})
        messages.append({'from': '', 'text': response})
        response_text = render_template('index.html', messages=messages)

        conversation.append({'user': message, 'ai': response})

        session["previous_questions_and_answers"] = previous_questions_and_answers
        session["conversation"] = conversation

        return response_text
    else:
        session.clear()
        return render_template('index.html')
    


if __name__ == "__main__":
    app.run(debug=True, port=5000)
