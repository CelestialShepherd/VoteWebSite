# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, flash, redirect, request, url_for
from app.forms import LoginForm, RegistrationForm, OfferForm, FeedbackForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Offer, Feedback
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Вадим Пикалов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        },
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():#собирает все данные, запускает все валидаторы,
#прикрепленные к полям, и если все в порядке, вернет True
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,  midle_name=form.midle_name.data, phone=form.phone.data, address=form.address.data,  )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    if user: 
        return render_template('user.html', user=user)
    else:
        return render_template('404.html')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()    

@app.route('/feedback',  methods=['GET', 'POST'])
def feedback():
    form=FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(feedemail=form.feedemail.data, feedbody=form.feedbody.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Congratulations, we will help you soon!')
        return redirect(url_for('index'))
    return render_template('feedback.html', title='Feedback', form=FeedbackForm())

    

@app.route('/offer', methods=['GET', 'POST'])
def offer():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form=OfferForm()
    if form.validate_on_submit():
        offer = Offer(title=form.title.data, body=form.body.data)
        db.session.add(offer)
        db.session.commit()
        flash('Thanks for your offer, we will moderate it soon!')
        return redirect(url_for('index'))
    return render_template('offer.html', title='Offer', form=OfferForm())
