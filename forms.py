from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange



class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    mail = StringField('E-mail:', validators=[DataRequired(), Email('Not an email adress')])
    password = PasswordField('Password:', validators=[DataRequired()])
    check_password = PasswordField('Repeate password:',
                                   validators=[EqualTo(fieldname='password', message='Passwords don\'t match')])
    teacher = BooleanField('I\'m a teacher')
    my_classroom = StringField('My class (only for students)')
    submit = SubmitField('Go')


class LoginForm(FlaskForm):
    mail = StringField('E-mail:', validators=[DataRequired(), Email('Not an email adress')])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    teacher = BooleanField('I\'m a teacher')
    submit = SubmitField('Войти')
