from flask import Blueprint, render_template,request,flash,url_for,redirect
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from . import db
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/auth/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pword = request.form.get('pword')

        user_exists = User.query.filter_by(name = name ,email = email).first()
        print(user_exists)
        if not name:
            flash('Name field is blank',category='error')
        elif len(email) < 6:
            flash('email is invalid',category='error')
        elif len(pword) < 5:
            flash('pword is too short',category='error')
        elif user_exists:
            flash('Those credentials are already accquired',category='error')
        else:
            new_user = User(name= name,email=email,pword = generate_password_hash(pword))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created successfully!!',category='success')
            return redirect(url_for('views.home'))




    return render_template('sign_up.html',user = current_user)

@auth.route('/auth/sign-in',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pword = request.form.get('pword')
        user_exists = User.query.filter_by(email = email).first()
        
        if  user_exists:
            if check_password_hash(user_exists.pword,pword):
                    flash('Logged In !!!!',category='success')
                    login_user(user_exists,remember=True)
                    return redirect(url_for('views.home'))
            else:
                flash('password is incorrect',category='error')
            
        else:
            flash('Seems like you dont have a account as the credentials dont match',category='error')
           



    return render_template('sign_in.html',user = current_user)


@auth.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))