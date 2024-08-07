from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, PasswordField, SubmitField, BooleanField, RadioField, DateTimeField, TextAreaField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError, InputRequired, NumberRange
from constants import industries, role


class RegisterForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(
            message='Username is required'), Length(min=3, max=30)], 
        render_kw={"placeholder": "test username"}
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(message='Email is required'), Email()],
        render_kw={"placeholder": "testuser@gmail.com"}
    )
    role = SelectField(
        label='Role',
        choices=['Brand', 'Influencer'],
        validators=[DataRequired(
            message='Role is required')],
    )
    industry = SelectField(
        label='Industry',
        choices=industries,
        validators=[DataRequired(
            message='Industry is required')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(
            message='Password is required'), Length(min=6, max=20)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(message='Confirm Password is required'), Length(
            min=6, max=20), EqualTo(fieldname='password', message='passeord dont match')]
    )
    submit = SubmitField(
        'Register'
    )

class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(
            message='Username is required'), Length(min=3, max=30)],
        render_kw={"placeholder": "test username"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(
            message='Password is required'), Length(min=6, max=20)],
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(
        'Login'
    )

class CampaignForm(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired(
            message='name is required'), Length(min=3, max=30)],
        render_kw={"placeholder": "Type campaign name"}
    )
    description = TextAreaField(
        label='Description',
        validators=[DataRequired(
            message='name is required')],
        render_kw={"placeholder": "Tell something about the campaign"}
    )
    visibility = SelectField(
        label='Visibility',
        choices=['public', 'private'],
        validators=[DataRequired(
            message='visibility is required')],
    )
    start_date = DateField(
        label='Start Date',
        validators=[DataRequired(
            message='Start date is required')],
        render_kw={"placeholder": "Tell something about the campaign"}
    )
    end_date = DateField(
        label='End Date',
        validators=[DataRequired(
            message='End date is required')]
    )
    allocate_budget = IntegerField(
        label='Allocate Budget',
        validators=[DataRequired(
            message="allocate budget is required"), NumberRange(min=0)],
        render_kw={"placeholder": "$2999"}
    )

