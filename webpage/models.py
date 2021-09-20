from flask_login import UserMixin
from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.Text,nullable=False)
	email = db.Column(db.Text,nullable=False)
	pword = db.Column(db.String,nullable=False)
	notes = db.relationship('Note',backref='user',passive_deletes=True)

class Note(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.Text,nullable=False)
	body = db.Column(db.Text,nullable=False)
	date_created = db.Column(db.DateTime(timezone=True),default=func.now())
	notes = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
	