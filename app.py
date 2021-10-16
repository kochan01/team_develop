import os
import tweepy
import tw_key
from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='./templates/images')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

#tweepyの設定
CONSUMER_KEY = tw_key.twdict['cons_key']
CONSUMER_SECRET = tw_key.twdict['cons_sec']
ACCESS_TOKEN_KEY = tw_key.twdict['accto_key']
ACCESS_TOKEN_SECRET = tw_key.twdict['accto_sec']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


@app.route("/")
def index():
  tweets = api.search_tweets(q="#デザイン", count=10)
  return render_template("index.html", tweets=tweets)

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
