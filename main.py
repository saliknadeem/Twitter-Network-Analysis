from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/twitter")
def twitter():
    return "Hello, Twitter"



if __name__ == "__main__":
    app.run(debug=True)
