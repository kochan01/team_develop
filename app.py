from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/inquery")
def inquery():
  return render_template("inquery.html")

@app.route("/company")
def company():
  return render_template("company.html")

@app.route("/recruit")
def recruit():
  return render_template("recruit.html")