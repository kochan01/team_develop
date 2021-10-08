import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)


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