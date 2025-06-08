from flask import Flask, render_template, session, redirect, url_for, request
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "demo_secret_key")

@app.route("/", methods=["GET", "POST"])
def index():
    if "coins" not in session:
        session["coins"] = 10
        session["message"] = ""

    if request.method == "POST":
        if "spin" in request.form:
            if session["coins"] > 0:
                session["coins"] -= 1
                symbols = ["🍒", "🍋", "🍇", "💎", "7️⃣"]
                result = [random.choice(symbols) for _ in range(3)]
                session["result"] = result

                if result[0] == result[1] == result[2]:
                    session["coins"] += 5
                    session["message"] = "🎉 JACKPOT! You win 5 coins!"
                elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
                    session["coins"] += 2
                    session["message"] = "✨ Nice! You win 2 coins!"
                else:
                    session["message"] = "💨 No match. Try again!"
            else:
                session["message"] = "You're out of coins! Click Restart to play again."

        elif "restart" in request.form:
            session["coins"] = 10
            session["result"] = []
            session["message"] = "🔁 Game restarted!"

    return render_template("index.html",
                           coins=session["coins"],
                           result=session.get("result", []),
                           message=session.get("message", ""))
