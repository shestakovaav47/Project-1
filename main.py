from flask import Flask, render_template, redirect, abort, request
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from orm.models import Student, Teacher, Classroom
import forms



from orm import db_session


app = Flask(__name__)
app.config['SEKRET_KEY'] = 'MYSECRETKEY'

db_session.global_init('database/db2.sqlite')
login_manager = LoginManager(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_student(id):
    ses = db_session.create_session()
    user = ses.query(Student).filter(Student.id == id).first()
    ses.close()
    return user


@login_manager.user_loader
def load_teacher(id):
    ses = db_session.create_session()
    user = ses.query(Teacher).filter(Teacher.id == id).first
    ses.close()
    return user


@app.route('/log_in', methods=['GET', 'POST'])
def login_page():
    log_out()
    mes = ''
    form = forms.Log_inForm()
    if form.validate_on_submitt():
        mail = form.mail.data
        teacher = form.if_teacher.data
        ses = db_session.create_session()
        if teacher:
            user = ses.query(Teacher).filter(Teacher.mail == mail).first()
        else:
            user = ses.query(Student).filter(Student.mail == mail).first()
        if not user:
            mes = 'No such user found'
        elif not user.check_password(form.password.data):
            mes = 'Wrong password'
        else:
            login_user(user)
            if teacher:
                resp = redirect('/main_page_teacher')
            else:
                resp = redirect('/main_page_student')
            ses.close()
            return resp
    resp = render_template('enter.html', title='Enter', form=form, message=mes)
    return resp


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        if form._if_teacher.data:
            user = Teacher(form.username.data,
                           form.mail.data,
                           form.password.data,
                           form.subject.data,
                           form.my_classrooms.data)
        else:
            user = Student(form.username.data,
                           form.mail.data,
                           form.password.data,
                           form.classroom.data)
        ses=db_session.create_session()
        try:
            ses.add(user)
            ses.commit()
        except IntegrityError:
            return render_template('registration.html', title='Registration', form=form, message='A user with that mail already exists')
        except Exception as e:
            print(e)
            return render_template('registration.html', title='Registration', form=form, message='An undefined error occured')
        finally:
            ses.close()
        return redirect('/log_in')
    return render_template('registration.html', title='Registration', form=form)



@app.route('/main_page_teacher')
@login_required
def main_page_teacher():
    ses = db_session.create_session()
    ses.add(current_user)
    ses.merge(current_user)
    resp = render_template('main_teacher.html', title='My homepage', len=len)
    ses.close()
    return resp


@app.route('/main_page_student')
@login_required
def main_page_student():
    ses = db_session.create_session()
    ses.add(current_user)
    ses.merge(current_user)
    resp = render_template('main_student.html', title='my homepage', len=len)
    ses.close()
    return resp


@app.route('/marks_student')
@login_required()
def student_marks_page():
    ses = db_session.create_session()
    ses.add(current_user)
    ses.merge(current_user)
    resp = render_template('marks_student.html', title='My marks', len=len)
    ses.close()
    return resp


@app.route('/marks_teacher/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def teacher_marks_page(classroom_id):
    ses = db_session.create_session()
    classroom = ses.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        ses.close()
        abort(404)
    resp = render_template('marks_teacher.html', title=classroom.name, classroom=classroom, len=len)
    ses.close()
    return resp

