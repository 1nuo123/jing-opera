from flask import Flask

app = Flask(__name__)

@app.route("/")
def try_0():
    return "Hallo world!"