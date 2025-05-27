import requests
from flask import Flask, render_template, request

app = Flask(__name__)

MOOD_MESSAGES = {
    "Happy": "You're glowing! Here's a joke to keep the smiles going!",
    "Sad": "Cheer up, buddy.",
    "Stressed": "Deep breath. Here's a joke to lighten your mood.",
    "Bored": "Need a laugh?",
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/joke", methods=['GET', 'POST'])
def joke():
    joke = None
    mood = None
    message = None

    if request.method == 'POST':
        mood = request.form.get('mood')
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})

        if response.status_code == 200:
            joke = response.json().get("joke")
            message = MOOD_MESSAGES.get(mood, "Here's a joke for you!")
        else:
            joke = "Sorry, couldn't fetch a joke right now. Try again later."

    return render_template("joke.html", joke=joke, mood=mood, message=message)


@app.route("/search", methods=['GET', 'POST'])
def search():
    term = None
    jokes = []
    error = None

    if request.method == 'POST':
        term = request.form.get('term')
        response = requests.get(f"https://icanhazdadjoke.com/search?term={term}", headers={"Accept": "application/json"})

        if response.status_code == 200:
            results = response.json().get("results")
            if results:
                for joke in results:
                    jokes.append(joke["joke"])
            else:
                error = "No jokes found, please try another term."
        else:
            error = "Error connecting to the joke API."

    return render_template("search.html", jokes=jokes, term=term, error=error)

if __name__ == "__main__":
    app.run(debug=True)