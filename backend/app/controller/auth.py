from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request

from app.extension import db
from app.model import User
from app.form import FormLogin
from app.form import FormProfile
from flask_login import login_user, logout_user, current_user, login_required

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

@auth.route('/profile')
@login_required
def profile():
    form = FormProfile()
    if form:
        if form.validate_on_submit():
            uid = form.uid.data
            userName = form.userName.data
            user = User.query.filter(User.uid == uid).first()
            user.user_name = userName
            if form.password.data and user.verify_password(form.oldPassword.data) and form.password.data == form.checkPassword.data:
                user.password = form.password.data
    return render_template('profile.html')
