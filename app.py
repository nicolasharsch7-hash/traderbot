from flask import Flask, render_template, request, redirect, session
from db import *
import requests
import os

app = Flask(__name__)
app.secret_key = "secret123"

init_db()

def precio():
    return float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"])

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]
        session["user"] = int(user_id)
        get_user(int(user_id))
        return redirect("/dashboard")

    return '''
    <form method="post">
    <input name="user_id" placeholder="8225742299">
    <button>Entrar</button>
    </form>
    '''

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = get_user(session["user"])
    btc = precio()

    return f"""
    <h2>💎 Dashboard</h2>
    <p>Balance: ${user[2]}</p>
    <p>BTC: ${btc}</p>
    """

app.run(host="0.0.0.0", port=10000)
