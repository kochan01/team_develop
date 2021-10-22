from datetime import datetime
import os
import tweepy
import tw_key
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='./templates/images')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
app.config['DEBUG'] = True# デバッグモードをTrueにする
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

#tweepyの設定
CONSUMER_KEY = tw_key.twdict['cons_key']
CONSUMER_SECRET = tw_key.twdict['cons_sec']
ACCESS_TOKEN_KEY = tw_key.twdict['accto_key']
ACCESS_TOKEN_SECRET = tw_key.twdict['accto_sec']

callback_url="https://mighty-thicket-70693.herokuapp.com/auth"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback_url)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
redirect_url = auth.get_authorization_url()



@app.route("/")
def index():
  tweets = api.search_tweets(q="#デザイン", count=10)
  return render_template("index.html", tweets=tweets, redirect_url=redirect_url)

@app.route("/auth")
def tweet():
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback_url)
  oauth_token = request.args.get('oauth_token',default=' ',type=str)
  oauth_verifier = request.args.get('oauth_verifier',default=' ',type=str)
  auth.request_token['oauth_token'] = oauth_token
  auth.request_token['oauth_token_secret'] = oauth_verifier
  auth.get_access_token(oauth_verifier)
  auth.set_access_token(auth.access_token,auth.access_token_secret)
  api = tweepy.API(auth)
  api.update_status("最高のページだね！ #デザイン")

  return redirect("/")



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

@app.route("/home", methods=["GET","POST"])
def home():
  if request.method == "POST":
    title = request.form.get("title")
    detail = request.form.get("detail")
    due = request.form.get("due")

    due = datetime.strptime(due, '%Y-%m-%d')
    new_post = Post(title=title, detail=detail, due=due)

    db.session.add(new_post)
    db.session.commit()

    return redirect("/home")
  else:
    posts = Post.query.order_by(Post.due).all()
    return render_template('home.html', posts=posts)

@app.route("/todo")
def todo():
  return render_template('todo.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/home')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/home')



 