### IMPORT REQUIRED LIBRARIES ###
from flask import Flask, render_template, request #flask framework
from werkzeug.exceptions import abort #to get error messages on the browser
from waitress import serve #start the local host server
from chatgpt_wrapper import ChatGPT
import webbrowser #to open web browser automatically
import openai
#################################

############################ START OF FUNCTION DEFINITIONS ######################################
def setAPISecretKey():
    with open ("api_key.txt", "r") as file:
        key = file.read()
    openai.api_key = key

def getCompletions(title, description, field):
    setAPISecretKey()
    prompt = title + description + field
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}]
        )
    return completion['choices'][0]['message']['content']

def askGPT_BOT(title, description, field):
    bot = ChatGPT()
    bot.refresh_session()
    prompt = title + description + field
    response = bot.ask(str(prompt))
    return response
############################# END OF FUNCTION DEFINITIONS #######################################


### DEFINING THE FLASK APP ###
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKeyForFlask' #can be changed to anything
#############################################


### APP ROUTE FUNCTIONS ###

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST': #if the new product form is submitted then get the information and add the new product to database
        title = request.form['title']
        description = request.form['description']
        field = request.form['field']
        # response = getCompletions(title, description, field)
        # print(response)
        response = askGPT_BOT(title, description, field)
        print(response)
        return render_template('index.html', response = response) 
    return render_template('index.html') 


### END OF APP ROUTE FUNCTIONS ###

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/')
    serve(app, host="127.0.0.1", port=5000, threads=2)