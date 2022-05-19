from datetime import datetime
from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
from ..models import User
from ..forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        find_user = User.query.filter_by(email=request.form.get('email')).first()
        if find_user is None:
            new_user = User(
                name = request.form.get('name'),
                email = request.form.get('email'),
                password = generate_password_hash(
                    request.form.get('password'),
                    method='pbkdf2:sha256',
                    salt_length=13,
                ),
                dob = datetime.strptime(request.form.get('dob'),'%Y-%m-%d'),
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration completed! Login now!')
        else:
            flash('User already exists, Please login!')
        return redirect(url_for('auth.login'))
    return render_template('auth.html', form=form, purpose='register')

@auth.route('/login', methods=['GET','POST'])
@auth.route('/login/<prompt>', methods=['GET','POST'])
def login(prompt=False):
    form = LoginForm()
    if form.validate_on_submit():
        find_user = User.query.filter_by(email=request.form.get('email')).first()
        if find_user is None:
            flash("User doesn't exist! Please register!")
            return redirect(url_for('auth.register'))
        elif check_password_hash(find_user.password, request.form.get('password')):
            login_user(find_user)
            return redirect(url_for('views.home'))
        else:
            flash('Wrong email or password!')
    elif prompt:
        flash('You need to login to add products to cart!')
    return render_template('auth.html', form=form, purpose='login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
    