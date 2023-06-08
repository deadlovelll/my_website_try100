from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap
from datetime import date
from sqlalchemy import Table, Column, Integer, ForeignKey
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators, BooleanField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "wszsder5tfgvhuiolpo9i8765t4re3w2edrftgyhujIU&Y^%$E#WSAXDCFVGHJIKO(I*U7"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clients.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ContactForm(FlaskForm):
    fio = StringField("Фамилия и Имя", validators=[DataRequired()])
    number = StringField("Ваш Номер Телефона в формате : +7**********", validators=[DataRequired(), validators.Regexp(r'^\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')])
    email = StringField("Ваша Электронная Почта", validators=[DataRequired()])
    checkmark = BooleanField("Я согласен с обработкой моих персональных данных", validators=[DataRequired()])
    submit = SubmitField("Отправить Данные")


class UsersInfo(db.Model):
    __tablename__ = "clients_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/form", methods=["GET","POST"])
def form():
    contactform = ContactForm()
    if contactform.validate_on_submit():
        name = request.form.get("fio")
        tel_number = request.form.get("number")
        email = request.form.get("email")
        client = UsersInfo(name=name, number=tel_number, email=email)
        db.session.add(client)
        db.session.commit()
        time.sleep(3)
        return redirect(url_for("home"))
    return render_template("form_page.html", contactform=contactform)


@app.route("/faq_page")
def faq():
    return render_template("faq.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run()