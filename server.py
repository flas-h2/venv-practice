import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    #return a simple string that is valid in HTML
    return render_template("home.html")

@app.route("/joke", methods=['GET', 'POST'])
def joke():
    joke = None

    jokeresp = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"} )
    #if request.method == 'POST':
    if jokeresp.status_code == 200:
        joke_json = jokeresp.json().get("joke")
        joke = joke_json
    else:
        joke = "Could not fetch you a joke right now. Please try again later."
        
    return render_template("joke.html", joke=joke)

if __name__ == "__main__":
    app.run(debug=True)