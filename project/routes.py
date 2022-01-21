from flask import render_template, request, flash, url_for,session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from project.oauth_deco import login_is_required
from project import app, db
from .models import User
from project import oauth

@app.route('/')
def index():
    return render_template('index.html',session=session)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Вже зареєстровано користувача з такою адресою')
            return redirect(url_for('register'))

        newUser = User(email=email, password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(newUser)
            db.session.commit()
            flash("Користувача успішно зареєстровано")
            return redirect(url_for('login'))
        except:
            return "Error adding new User to DB"
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        remember = True if request.form.get('remember') else False

        if not user or not check_password_hash(user.password, password):
            flash("Перевірте правильність данних")
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('room'))


@app.route('/logout')
@login_is_required
def logout():
    logout_user()
    flash("Successfully loged out")
    return redirect('/')


@app.route('/room')
def room():
    if session.permanent:
        return redirect(url_for('room1'))
    else:
        return redirect(url_for('room2'))

@app.route('/meeting-room')
@login_is_required
def room1():
    return render_template('room.html')

#@app.route('/conference-room')
#@login_is_required
#def room2():
#    return render_template('room.html')