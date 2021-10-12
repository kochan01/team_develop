import os
import re
from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/inquery", methods=["GET", "POST"])
def inquery():
  if request.method == "POST":
    recipient = request.form.get('mail')
    msgr = Message('問い合わせ送信完了しました！', recipients=[recipient])
    msgr.body = ('お問合せ内容確認')
    msgr.html = ('<h1>問い合わせ送信完了しました！</h1>')
    mail.send(msgr)
    return redirect("/")

  else:
    return render_template("inquery.html")  

@app.route("/company")
def company():
  return render_template("company.html")

@app.route("/recruit")
def recruit():
  return render_template("recruit.html")
