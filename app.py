import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

#DATABASE XD
db = SQL("sqlite:///mystery.db")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # get array of secret accoutns
    secretAccounts = ["moe", "soos"]
    if request.method == "POST":
        #get logs and save them
        logs = request.form.get("logs")
        #save logs
        db.execute("UPDATE users SET logs = ? WHERE id LIKE ?", logs, session["user_id"])
        # redirect
        return redirect("/")
    else:
        #load logs and name
        logs = db.execute("SELECT * FROM users WHERE id LIKE ?", session["user_id"])
        name = logs[0]["name"]
        logs = logs[0]["logs"]
        # render HTML
        return render_template("index.html",name=name, secretAccounts=secretAccounts, logs=logs)


@app.route("/richard", methods=["GET", "POST"])
@login_required
def buy():
    return render_template("richard.html")


@app.route("/ronaldo")
@login_required
def history():
    return render_template("ronaldo.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password was submitted
        name = request.form.get("name")
        # all names stored in LOWERCASE for the sake of easy comparision
        name = name.lower()
        if not name:
            return apology("make a name please, you can sneak into anyone's game if you know their name!", 403)

        if not request.form.get("password"):
            return apology("at least try a passsword!", 403)
        elif not request.form.get("password").lower() == "soos":
            return apology("Wrong password! What's my name??")

        # check if user exists, if they do, log them in
        user = db.execute("SELECT * FROM users WHERE name LIKE ?", name)

        if len(user) <= 0:
            #create a new guy
            db.execute("INSERT INTO users (name) VALUES (?)",name)
            #redefine user
            user = db.execute("SELECT * FROM users WHERE name LIKE ?", name)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]
        # Redirect user to home / logs page, pass in an array containing all of the SECRET names so that they ARENT ALLOWED TO SAVE!!!!
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/cartman", methods=["GET", "POST"])
@login_required
def cartman():
    return render_template("cartman.html")


@app.route("/broomstick", methods=["GET", "POST"])
def broomstick():
    return render_template("broomstick.html")


@app.route("/decryptor", methods=["GET", "POST"])
@login_required
def decryptor():

    if request.method == "POST":
            caesar = request.form.get("caesar")
            atbash = request.form.get("atbash")

            #alphabet reference
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            Ualphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if caesar == "" and atbash == "":
                return apology("please add input to at least one decryptor!")

            # after validating that we got some sort of input, begin decryption, first algo is caesar
            caesarOutput = []

            #check that some caesar input was given
            if caesar != "":
                for i in range(26):
                    currStr = ""
                    # for every char in string
                    for char in caesar:
                        # if char is alphabetical
                        if char in alphabet:
                            newIndex = alphabet.index(char) + i
                            # check if goes beyond alphabet limit, reset at A
                            if newIndex > 25:
                                newIndex -= 26
                            # add new char
                            currStr += alphabet[newIndex]

                        elif char in Ualphabet:
                            newIndex = Ualphabet.index(char) + i
                            # check if goes beyond alphabet limit, reset at A
                            if newIndex > 25:
                                newIndex -= 26
                            # add new char
                            currStr += Ualphabet[newIndex]

                        else:
                            # add char
                            currStr += char
                    # add "deciphered string to list"
                    caesarOutput.append(currStr)

            # next run the atbash algorithm, first check that this specific box hasnt been left empty
            if atbash != "":
                newStr = ""
                for char in atbash:
                    # reverse each char
                    if char in alphabet:
                        newIndex = 25-alphabet.index(char)
                        newStr += alphabet[newIndex]

                    elif char in Ualphabet:
                        newIndex = 25-Ualphabet.index(char)
                        newStr += Ualphabet[newIndex]
                    else:
                        newStr += char
                atbash = newStr

            return render_template("Doutput.html", caesarOut=caesarOutput, atb=atbash)
    else:
         return render_template("decryptor.html")

@app.route("/accusation", methods=["GET", "POST"])
@login_required
def acccuse():

    if request.method == "POST":
        criminal = request.form.get("crim")
        accomplice = request.form.get("accomplice")
        kennyStat= request.form.get("kenny")

        if criminal == "" or accomplice == "" or kennyStat == "":
            return apology("Not all fields filled out")

        if("cristiano" in criminal.lower() or "ronaldo" in criminal.lower()) and ("eric" in accomplice.lower() or "cartman" in accomplice.lower()) and "nothing" in kennyStat.lower():
                return render_template("accusationW.html")

        return render_template("accusationL.html")
    else:
        return render_template("accusation.html")