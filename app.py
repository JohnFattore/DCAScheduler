import os
from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3
from flask_session import Session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/scheduler", methods=["GET","POST"])
def scheduler():
   if request.method == "POST":
      stock = request.form.get("stock")
      return render_template("schedulerpost.html", stock=stock)
   else:
      return render_template("scheduler.html")



if __name__ == '__main__':
   app.run(debug=True)