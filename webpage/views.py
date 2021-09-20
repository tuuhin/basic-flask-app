from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User,Note
from . import db
views = Blueprint('views',__name__)


@views.route('/home')
@login_required
def home():
    note = Note.query.filter_by(notes=current_user.id)
    return render_template('home.html',user = current_user,note=note)


@views.route('/profile',methods=['GET','POST'])
@login_required
def change_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        oldPword = request.form.get('oldpword')
        newPword = request.form.get('pword') 
        if not oldPword:
            flash('Please enter the old password can\'t update a blank line',category='error')
        elif not name:
            flash('Name field have no value',category='error')
        elif not email:
            flash('Email field have no value',category='error')
        elif not newPword:
            flash('Please enter a password can\'t update a blank line',category='error')
        else :
            if not check_password_hash(current_user.pword,oldPword):
                flash('Old password don\'t match',category='error')
            else:
                print('Got')
                User.query.filter_by(name=current_user.name).update(dict(name=name,pword=generate_password_hash(newPword),email=email))          
                db.session.commit()
                return redirect(url_for('views.home'))
    return render_template('profile.html',user=current_user)


@views.route('/create-note',methods=['GET','POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        body =request.form.get('body')
        if not title:
            flash('provide a title to work',category='error')
        elif not body:
            flash('body is missing provide a body',category='error')
        else:
            note = Note(title=title,body=body,notes=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('note  added ',category='success')
            return redirect(url_for('views.home'))
    return render_template('createnote.html',user=current_user)

@views.route('/delete-note/<int:note_id>')
@login_required
def delete(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note and note.notes == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('note deleted successfully',category='success')
    else:
        flash('unauthorized',category='error')
    return redirect(url_for('views.home'))



@views.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    note = Note.query.filter_by(id=id).first()
    if note.notes == current_user.id:
        if request.method == 'POST':
            title = request.form.get('newtitle')
            body = request.form.get('newbody')
            if not title:
                flash('title missing',category='error')
            elif not body:
                flash('body not found',category="error")
            else:
                Note.query.filter_by(id=id).update(dict(title=title,body=body))
                db.session.commit()
                flash('data updated',category='success')
                return redirect(url_for('views.home'))
        return render_template('update_note.html',user=current_user,note=note)
    else:
        flash('unauthorized',category='error')
        return redirect(url_for('views.home'))