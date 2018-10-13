from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('api/sendText/', methods=['POST'])
def send_text():
    text = request.form['bodyOfText']
    # save to db with corresponding user
    username = request.form['username']
    # send results back to user