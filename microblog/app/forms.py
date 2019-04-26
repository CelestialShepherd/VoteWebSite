# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Offer, Feedback

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Surname', validators=[DataRequired()])
    midle_name = StringField('Patronymic', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')

class OfferForm(FlaskForm):
    title = StringField('Name your offer', validators=[DataRequired()])
    body = StringField('Describe your offer', validators=[DataRequired()])
    submit = SubmitField('Send offer')

    def validate_title(self, title):
        post = Offer.query.filter_by(title=title.data).first()
        if post is not None:
            raise ValidationError('Please rename your offer.')

class FeedbackForm(FlaskForm):
    feedemail = StringField('Your Email',validators=[DataRequired(), Email()])
    feedbody = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Send')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')