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
app.config['DEBUG'] = True# デバッグモードをTrueにする
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
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
  tweets = api.search_tweets(q="#スマブラ", count=10)
  return render_template("index.html", tweets=tweets)

@app.route("/inquery", methods=["GET", "POST"])
def inquery():
  if request.method == "POST":
    name = request.form.get('yourname')
    furigana = request.form.get('furigana')
    recipient = request.form.get('mail')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    choice = request.form.get('choice')
    contents = request.form.get('contents')
    msgr = Message('問い合わせ送信完了しました！', recipients=[recipient])
    msgr.body = ('お問合せ内容確認')
    message = ('<p>名前：{0}</p>'
              '<p>ふりがな：{1}</p>'
              '<p>メールアドレス：{2}</p>'
              '<p>電話番号：{3}</p>'
              '<p>性別：{4}</p>'
              '<p>問い合わせ項目：{5}</p>'
              '<p>問い合わせ内容：{6}</p>'
              .format(name, furigana, recipient, phone, gender, choice, contents))
    msgr.html = message
    flash('送信完了しました！')
    mail.send(msgr)
    msg_s = Message('問い合わせ到着', recipients=[os.environ.get('MAIL_DEFAULT_SENDER')])
    msg_s.body = ('お問合せ内容')
    msg_s.html = message
    mail.send(msg_s)
    return redirect("/")

  else:
    return render_template("inquery.html")  

@app.route("/company")
def company():
  return render_template("company.html")

@app.route("/recruit")
def recruit():
  return render_template("recruit.html")
