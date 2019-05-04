from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request

from app.extension import db
from app.model import User
from app.form import FormLogin
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        name = form.userName.data
        user = User.query.filter(User.user_name == name).first()
        if not user:
            flash('No such user')
        elif not user.verify_password(form.password.data):
            flash('Wrong password')
        else:
            login_user(user, remember = form.remember.data)
            # flash('登录成功')
            return redirect(url_for('main.home'))
    return render_template('login.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
