import email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import false
from. import db
from .models import Customer, User, Employee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user  = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
        else:
            flash('Wrong Email or Password, try again', category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        employ = check_employee(email)
        custom = check_customer(email)
        if user:
            flash('Email already exists.', category='error')
        elif employ:
            empol = Employee.query.filter_by(email=email).first()
            new_user = User(email=email, first_name=empol.first_name, last_name=empol.last_name,phone=empol.phone,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        elif custom:
            empol = Customer.query.filter_by(email=email).first()
            new_user = User(email=email, first_name=empol.first_name, last_name=empol.last_name,phone=empol.phone,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            c = Customer.query.filter_by(email=email).first()
            if c:
                c.phone = phone
                c.first_name = first_name
                c.last_name = last_name
            else:
                new_customer = Customer(email=email, first_name=first_name, last_name=last_name,phone=phone)
                db.session.add(new_customer)
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(
                    password1, method='sha256'),phone=phone)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user = current_user)


    
def check_employee(email):
    Euser = Employee.query.filter_by(email=email).first()
    if Euser:
        return True
    else:
        return False

def check_customer(email):
    Euser = Customer.query.filter_by(email=email).first()
    if Euser:
        return True
    else:
        return False