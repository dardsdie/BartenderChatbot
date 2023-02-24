from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template("application.html")

@app.route('/chat', methods=['POST'])
def chat():
    # Handle chat functionality here
    message = request.form['message']
    response = chatbot_response(message)
    # Return a response to the chatbox
    return response

def chatbot_response(message):
    # Your chatbot logic goes here
    return "You said: " + message

if __name__ == '__main__':
    app.run(debug=True)
