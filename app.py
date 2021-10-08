import os
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
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/inquery", methods=["GET", "POST"])
def inquery():
  if request.method == "POST":
    yourname = request.form.get('yourname')
    furigana = request.form.get('furigana')
    recipient = request.form.get('mail')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    choice = request.form.get('choice')
    contents = request.form.get('contents')
    
    serv_mail = Message('問い合わせがきました。', recipients=[os.environ.get('MAIL_DEFAULT_SENDER')])
    serv_mail.body = ('お問合せ内容確認')
    serv_mail.html = ('<h1>問い合わせ</h1>'
                '<br>'
                '<p>名前： {{ yourname }} </p>'
                '<p>ふりがな： {{ furigana }} </p>'
                '<p>メールアドレス： {{ recipient }} </p>'
                '<p>電話番号： {{ phone }} </p>'
                '<p>性別： {{ gender }} </p>'
                '<p>問い合わせ項目： {{ choice }} </p>'
                '<p>問い合わせ内容： {{ contents }} </p>'
                , yourname, furigana, recipient, phone, gender, choice, contents)
    mail.send(serv_mail)

    msgr = Message('問い合わせ送信完了しました！', recipients=[recipient])
    msgr.body = ('お問合せ内容確認')
    msgr.html = ('<h1>問い合わせ送信完了しました！</h1>'
                '<br>'
                '<p>名前： {{ yourname }} </p>'
                '<p>ふりがな： {{ furigana }} </p>'
                '<p>メールアドレス： {{ recipient }} </p>'
                '<p>電話番号： {{ phone }} </p>'
                '<p>性別： {{ gender }} </p>'
                '<p>問い合わせ項目： {{ choice }} </p>'
                '<p>問い合わせ内容： {{ contents }} </p>'
                , yourname, furigana, recipient, phone, gender, choice, contents)
    mail.send(msgr)
    flash('送信完了しました')
    return redirect("/")

  else:
    return render_template("inquery.html")

  

@app.route("/company")
def company():
  return render_template("company.html")

@app.route("/recruit")
def recruit():
  return render_template("recruit.html")