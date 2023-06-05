### IMPORT REQUIRED LIBRARIES ###
from flask import Flask, render_template, request  # flask framework
from werkzeug.exceptions import abort  # to get error messages on the browser
from waitress import serve  # start the local host server
from chatgpt_wrapper import ChatGPT
import webbrowser  # to open web browser automatically
import openai
#################################

############################ START OF FUNCTION DEFINITIONS ######################################


def setAPISecretKey():
    with open("/Users/pahchangarg/Desktop/react/chatgpt/apiKey.txt", "r") as file:
        key = file.read()
    openai.api_key = key


def setSystemPrompt(title, field):
    prompt = """
        Instructions: [
            1. Act as a software requirements engineer tasked to elicit 12 functional and 6 non functional requirements of an application.
            1. Generate only 5 additional questions first that would help more accurately answer the question 
            2. The questions should be in JSON format with a question ID
            3. Use the delimiter "SEP" after printing the additional questions.
        ]

        Task: [
            You have to generate at least 12 functional and 6 non-functional requirements in shall style for the ```{title}``` application which can be used in the field of ```{field}``` whose description is given below. You must display the additional questions first in JSON format, before generating the requirements. Generate an ID as well for the requirements. 
        ] 

        Output Format: [
            {'Q1': 'abc?', ..., 'Q5': 'xyz?'}
            SEP
            {'FR1': 'abc', ..., 'FR12': 'xyz'}
            SEP
            {'NFR1': 'abc', ..., 'NFR6': 'xyz'}
        ]
    """
    return prompt


def getCompletions(title, description, field):
    setAPISecretKey()
    prompt = setSystemPrompt(title, field)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": description}]
    )
    return completion['choices'][0]['message']['content']


def askGPT_BOT(title, description, field):
    bot = ChatGPT()
    bot.refresh_session()
    prompt = setSystemPrompt(title, field)
    response = bot.ask(str(prompt) + description)
    return response
############################# END OF FUNCTION DEFINITIONS #######################################


### DEFINING THE FLASK APP ###
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKeyForFlask'  # can be changed to anything
#############################################


### APP ROUTE FUNCTIONS ###

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':  # if the new product form is submitted then get the information and add the new product to database
        title = request.form['title']
        description = request.form['description']
        field = request.form['field']
        # response = getCompletions(title, description, field)
        # print(response)
        response = getCompletions(title, description, field)
        print(response)

        response = response.split('SEP')

        if len(response) == 3:
            questions = response[0]
            requirements = response[1:]
        elif len(response) == 2:
            questions = response[0]
            requirements = response[1]
        else:
            questions = response[:response.index('}')+1]
            requirements = response[response.index('}')+1:]

        print(requirements)
        return render_template('index.html', questions=questions, requirements=requirements)

    return render_template('index.html')


### END OF APP ROUTE FUNCTIONS ###

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/')
    serve(app, host="127.0.0.1", port=5000, threads=2)
